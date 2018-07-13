package de.fraunhofer.fokus.fuzzing.nmf.generation;

import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.nmf.FieldDescription;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.util.BitHelper;
import org.etsi.common.ByteHelper;

import java.util.Map;

import static java.lang.Math.toIntExact;

public class FuzzedPduGenerator {

    public static String generateFuzzedPdu(PduDescription description, Map<String, FuzzedValue> values) {
        String pduStr = description.getPduStr();
        byte[] pdu = ByteHelper.hexStringToByteArray(pduStr);
        for (FieldDescription field : description.getFields()) {
            if (values.containsKey(field.getName())) {
                int length = field.getEnd() - field.getStart() + 1;
                byte[] extract = ByteHelper.extract(pdu, field.getStart(), length);

                setFuzzedValue(extract, field, values.get(field.getName()));

                for (int i = 0; i < length; i++) {
                    pdu[field.getStart() + i] = extract[i];
                }

                String s = ByteHelper.byteArrayToHexString(extract);
                //System.out.println(field.getName() + ":" + s);
            }
        }
        return ByteHelper.byteArrayToHexString(pdu);
    }

    private static void setFuzzedValue(byte[] extract, FieldDescription field, FuzzedValue value) {
        switch (field.getType()) {
            case INTEGER:
                Long l = (long) value.getValue();
                int num = -1;
                try {
                    num = toIntExact(l);
                } catch (ArithmeticException e) {
                    //e.printStackTrace();
                }

                setFuzzedValue(extract, field, num);
                break;
        }
    }

    private static void setFuzzedValue(byte[] extract, FieldDescription field, int num) {
        byte[] bytes;
        if (field.getBitmask() != 0 && extract.length == 1) {
            byte b = BitHelper.setByteIntByMask(extract[0], num, (byte) field.getBitmask());
            bytes = new byte[]{b};
        } else {
            bytes = ByteHelper.intToByteArray(num, extract.length);
        }
        if (bytes.length != extract.length) {
            System.err.println("TODO fix me!");
        }
        for (int i = 0; i < bytes.length; i++) {
            extract[i] = bytes[i];
        }
    }

}
