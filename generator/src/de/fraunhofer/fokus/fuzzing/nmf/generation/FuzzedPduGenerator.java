package de.fraunhofer.fokus.fuzzing.nmf.generation;

import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.nmf.FieldDescription;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.util.BitsAndByteHelper;

import java.util.Map;

import static java.lang.Math.toIntExact;

public class FuzzedPduGenerator {

    public static String generateFuzzedPdu(PduDescription description, Map<String, FuzzedValue> values) {
        String pduStr = description.getPduStr();
        byte[] pdu = BitsAndByteHelper.hexStringToByteArray(pduStr);
        for (FieldDescription field : description.getFields()) {
            if (values.containsKey(field.getName())) {
<<<<<<< HEAD
=======
                //TODO pump up instead in insert
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
                int length = field.getEnd() - field.getStart() + 1;
                byte[] extract = BitsAndByteHelper.extract(pdu, field.getStart(), length);
                setFuzzedValue(extract, field, values.get(field.getName()));
                for (int i = 0; i < length; i++) {
                    pdu[field.getStart() + i] = extract[i];
                }
                String s = BitsAndByteHelper.byteArrayToHexString(extract);
                //System.out.println(field.getName() + ":" + s);
            }
        }
        return BitsAndByteHelper.byteArrayToHexString(pdu);
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
<<<<<<< HEAD

                setFuzzedValue(extract, field, num);
                break;
=======
                setFuzzedValue(extract, field, num);
                break;
            case STRING:
                String s = (String) value.getValue();
                setFuzzedValue(extract, field, s);
                break;
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
        }
    }

    private static void setFuzzedValue(byte[] extract, FieldDescription field, int num) {
        byte[] bytes;
        if (field.getBitmask() != 0 && extract.length == 1) {
            byte b = BitsAndByteHelper.setByteIntByMask(extract[0], num, (byte) field.getBitmask());
            bytes = new byte[]{b};
        } else {
            bytes = BitsAndByteHelper.intToByteArray(num, extract.length);
        }
        if (bytes.length != extract.length) {
            System.err.println("TODO fix me!");
        }
        for (int i = 0; i < bytes.length; i++) {
            extract[i] = bytes[i];
        }
    }

<<<<<<< HEAD
=======
    private static void setFuzzedValue(byte[] extract, FieldDescription field, String val) {
        byte[] bytes = val.getBytes();
        for (int i = 0; i < extract.length && i < bytes.length; i++) {
            extract[i] = bytes[i];
        }
    }

>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
}
