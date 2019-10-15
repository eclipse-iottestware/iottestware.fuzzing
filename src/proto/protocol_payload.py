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
from enum import Enum, auto

# TODO: any faster json implementations out there? cjson, ujason, rapidjson?
# import json


class PayloadType(Enum):
    """
    Enumerates the supported payload types
    """
    JSON = auto(),
    XML = auto(),
    RAW = auto()  # Raw is used for unknown or unspecified types

    def __str__(self):
        if self is PayloadType.JSON:
            return 'JSON'
        elif self is PayloadType.XML:
            return 'XML'
        else:
            return 'RAW'

    @staticmethod
    def from_str(pl_type):
        pl_type = pl_type.upper()
        if pl_type == str(PayloadType.JSON):
            return PayloadType.JSON
        elif pl_type == str(PayloadType.XML):
            return PayloadType.XML
        else:
            return PayloadType.RAW
