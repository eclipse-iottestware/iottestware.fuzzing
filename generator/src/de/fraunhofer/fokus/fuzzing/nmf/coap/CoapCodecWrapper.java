package de.fraunhofer.fokus.fuzzing.nmf.coap;

import de.fraunhofer.fokus.fuzzing.nmf.pcap.CodecWrapper;
import org.eclipse.californium.core.coap.*;
import org.eclipse.californium.core.network.serialization.UdpDataParser;
import org.eclipse.californium.core.network.serialization.UdpDataSerializer;
import org.eclipse.californium.elements.AddressEndpointContext;
import org.eclipse.californium.elements.EndpointContext;
import org.eclipse.californium.elements.RawData;

import java.net.InetSocketAddress;

public class CoapCodecWrapper implements CodecWrapper<Message> {

    private final UdpDataParser parser = new UdpDataParser();
    private final UdpDataSerializer serializer = new UdpDataSerializer();

    /*
    Proxy Data
     */

    private InetSocketAddress address = new InetSocketAddress("localhost", 1337);
    private EndpointContext destinationContext = new AddressEndpointContext(address);

    @Override
    public byte[] serialize(Message message) {
        byte[] encBytes = null;
        RawData rawData = null;
        int rawCode = message.getRawCode();
        message.setDestinationContext(destinationContext);
        try {
            if (CoAP.isRequest(rawCode)) {
                Request request = (Request) message;
                rawData = serializer.serializeRequest(request);
            } else if (CoAP.isResponse(rawCode)) {
                Response response = (Response) message;
                rawData = serializer.serializeResponse(response);
            } else if (CoAP.isEmptyMessage(rawCode)) {
                EmptyMessage emptyMessage = (EmptyMessage) message;
                rawData = serializer.serializeEmptyMessage(emptyMessage);
            }
            encBytes = rawData.getBytes();
        } catch (MessageFormatException e) {

        }
        return encBytes;
    }

    @Override
    public Message parse(byte[] pdu) {
        try {
            return parser.parseMessage(pdu);
        } catch (MessageFormatException | IllegalArgumentException e) {
            return null;
        }
    }
}
