# ********************************************************************************
# Copyright (c) 2019 Alexander Kaiser
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0.
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors:
#   Alexander Kaiser - initial API and implementation
# ********************************************************************************

from abc import ABC, abstractmethod
from src.proto.protocol_description import ProtocolDescription
from src.proto.protocol_payload import PayloadType
from src.logger import get_default_logger

# TODO: any faster json implementations out there? cjson, ujason, rapidjson?
import json


class AbstractMessage(ABC):

    id_counter = 0

    def __init__(self, protocol: ProtocolDescription, message):
        self._identifier = 'msg_' + str(AbstractMessage.id_counter)
        self._logger = get_default_logger()
        self._protocol = protocol
        self._message = message

        self._payload = None
        self._payload_changed = None  # saves encoding cycle if nothing changed

        # static counter for numbering messages
        AbstractMessage.id_counter += 1

    @property
    def identifier(self):
        return self._identifier

    @property
    def protocol_description(self):
        return self._protocol

    @property
    def protocol_type(self):
        return self.protocol_description.protocol_type

    @property
    def logger(self):
        return self._logger

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, payload):
        if self.has_payload:
            # set payload only possible if the underlying transport message is able to carry a payload
            if self._payload_changed is None:
                self._payload_changed = False  # first set is marked as NOT CHANGED
            elif self._payload_changed is False:
                self._payload_changed = True  # second set is counted as a real change

            self._payload = payload

    @property
    def has_payload(self):
        if self._payload is not None:
            return True

        # otherwise check if payload might be accessible but not yet loaded
        payload_field = self.protocol_description.payload_field
        if self.message_has_field(payload_field):
            return True  # the transport message has a payload, but still not decoded
        else:
            return False  # the transport message does not carry any payloads

    def __decode_payload(self):
        if self.protocol_description.payload_type is PayloadType.JSON:
            payload_field = self.protocol_description.payload_field
            raw_payload = self.message_get_field(payload_field)
            if raw_payload is not None:
                dec_payload = self.__decode_json_payload(raw_payload)
                if dec_payload is not None:
                    self.payload = dec_payload
        elif self.protocol_description.payload_type is PayloadType.RAW:
            pass  # nothing to do here?
        else:
            raise NotImplementedError('Decoding PayloadType={} not implemented'
                                      .format(self.protocol_description.payload_type))

    # TODO: move payload codec to a separate class: -> decode and encode the concrete format by given payload_type
    def __decode_json_payload(self, payload):
        try:
            json_payload = json.loads(payload)
        except json.decoder.JSONDecodeError:
            self._logger.warn('Cannot decode given payload as JSON: {}'.format(payload))
            return None
        return json_payload

    def payload_freeze(self):
        """
        Encodes the payload if it was manipulated and writes it to the payload field within the transport message
        :return:
        """
        if self.has_payload and self.payload_changed:
            if self.protocol_description.payload_type is PayloadType.JSON:
                raw_payload = self.__encode_json_payload(self.message.payload)
                if raw_payload is not None:
                    payload_field = self.protocol_description.payload_field
                    self.message.message_set_field(payload_field, raw_payload)
            elif self.protocol_description.payload_type is PayloadType.RAW:
                pass  # nothing to do here?
            else:
                raise NotImplementedError('Decoding PayloadType={} not implemented'
                                          .format(self.protocol_description.payload_type))

            """
            the payload is 'unchanged' again and written to the transport message,
            the whole transport message can be now safely encoded
            if additional changes are needed after this step, one needs again to decode
            """
            self._payload_changed = False

    # TODO: outsource
    def __encode_json_payload(self, payload):
        try:
            raw_payload = json.dumps(payload)
        except json.decoder.JSONDecodeError:
            self._logger.warn('Cannot encode given payload as JSON: {}'.format(payload))
            return None
        return raw_payload

    @property
    def payload_changed(self):
        """
        Did the payload change? If not, no need the encode
        :return: True if payload was manipulated, False otherwise
        """
        if self._payload_changed is True:
            return True
        else:
            return False

    # TODO: implement multi-level fields like a.b.c ?
    def payload_has_field(self, field_name):
        """
        Does the payload has a field specified by the field_name, e.g.,
        JSON: {'a': 1, 'b': 2, 'c': {'name': 'value'}}
        c.name should return value

        :param field_name: dot notation to access fields from key-value structures
        :return: True if payload exists and the requested field is present within the payload
        """
        if not self.has_payload:
            return False
        elif hasattr(self._payload, field_name):
            return True
        else:
            return False

    # TODO: these needs to be tested, once mutators for payload are available
    # TODO: what about multi-level fields like a.b.c ?
    def payload_get_field(self, field_name):
        if self.payload_has_field(field_name):
            return getattr(self._payload, field_name)
        else:
            self.logger.warn('{} Payload (read) has no attribute named "{}"'
                             .format(self.protocol_description.payload_type, field_name))
            return None

    def payload_set_field(self, field_name, field_value):
        if self.payload_has_field(field_name):
            setattr(self._payload, field_name, field_value)
            return True
        else:
            self.logger.warn('{} Payload (write) has no attribute named "{}"'
                             .format(self.protocol_description.payload_type, field_name))
            return False

    @property
    def message(self):
        return self._message

    @abstractmethod
    def message_has_field(self, field_name):
        pass

    @abstractmethod
    def message_get_field(self, field_name):
        pass

    @abstractmethod
    def message_set_field(self, field_name, field_value):
        pass


class ScapyMessage(AbstractMessage):

    def __init__(self, protocol: ProtocolDescription, message):
        super().__init__(protocol, message)

    def __str__(self):
        return 'ScapyMessage: desc=({})'.format(self.protocol_description)

    def message_has_field(self, field_name):
        if hasattr(self.message, field_name):
            return True
        else:
            return False

    def message_get_field(self, field_name):
        if self.message_has_field(field_name):
            return getattr(self.message, field_name)
        else:
            self.logger.warn('{} Message (read) has no attribute named "{}"'.format(self.protocol_type, field_name))
            return None

    def message_set_field(self, field_name, field_value):
        if self.message_has_field(field_name):
            setattr(self.message, field_name, field_value)
            return True
        else:
            self.logger.warn('{} Message (write) has no attribute named "{}"'.format(self.protocol_type, field_name))
            return False
