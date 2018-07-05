package de.fraunhofer.fokus.fuzzing.nmf.coap;

import de.fraunhofer.fokus.fuzzing.nmf.pcap.CodecWrapper;
import de.fraunhofer.fokus.fuzzing.nmf.FieldDescription;
import de.fraunhofer.fokus.fuzzing.nmf.traverser.ObjectTraverser;
import de.fraunhofer.fokus.fuzzing.nmf.pcap.PduTypeHandler;
import org.eclipse.californium.core.coap.Message;

import java.util.List;

public class CoapTypeHandler implements PduTypeHandler {

    private final CodecWrapper codec = new CoapCodecWrapper();

    private final ObjectTraverser traverser = new ObjectTraverser(codec);

    @Override
    public List<FieldDescription> getList() {
        return null;
    }

    @Override
    public boolean isPduType(byte[] pdu) {
        Message message = (Message) codec.parse(pdu);
        if (message == null) {
            return false;
        }
//        ByteHelper.dump("Packet", pdu);
        List<FieldDescription> traverse = traverser.traverse(message);
        for (FieldDescription description:traverse){
            System.out.println(description);
        }
//        try {
//            message.setMID(0);
//            Token token = message.getToken();
//            String asString = token.getAsString();
//            Token t = new Token(new byte[]{1});
//            message.setToken(t);
//            message.setPayload(new byte[]{77,1,2,3,77,77,77,77,77,77});
//
//        } catch (IllegalArgumentException e) {
//
//        }
//        ByteHelper.dump("Changed Packet", codec.serialize(message));

        return true;
    }




}
