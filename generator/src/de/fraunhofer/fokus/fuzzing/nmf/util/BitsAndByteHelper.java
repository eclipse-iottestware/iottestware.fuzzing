package de.fraunhofer.fokus.fuzzing.nmf.util;

public class BitsAndByteHelper {

    /**
     * Bytes
     */

<<<<<<< HEAD
    private static final char[] HEX_CHARS = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
=======
    private static final char[] HEX_CHARS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64

    public static String byteArrayToHexString(byte[] bytes) {
        char[] chars = new char[bytes.length * 2];
        for (int i = 0; i < bytes.length; i++) {
            chars[i * 2] = HEX_CHARS[(bytes[i] & 0xFF) >>> 4];
            chars[i * 2 + 1] = HEX_CHARS[(bytes[i] & 0xFF) & 0x0F];
        }
        return new String(chars);
    }

    public static byte[] hexStringToByteArray(String hex) {
        int len = hex.length();
        byte[] bytes = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            bytes[i / 2] = (byte) ((Character.digit(hex.charAt(i), 16) << 4)
<<<<<<< HEAD
                    + Character.digit(hex.charAt(i+1), 16));
=======
                    + Character.digit(hex.charAt(i + 1), 16));
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
        }
        return bytes;
    }

<<<<<<< HEAD
=======
    public static String hexStringToString(String hex) {
        StringBuilder sb = new StringBuilder();
        StringBuilder temp = new StringBuilder();

        for (int i = 0; i < hex.length() - 1; i += 2) {
            String output = hex.substring(i, (i + 2));
            int decimal = Integer.parseInt(output, 16);
            sb.append((char) decimal);
            temp.append(decimal);
        }
        return sb.toString();
    }

>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
    public static byte[] extract(byte[] array, int offset, int length) {
        byte[] res = new byte[length];
        System.arraycopy(array, offset, res, 0, length);
        return res;
    }

    public static byte[] intToByteArray(final int value, final int length) {
        byte[] bytes = new byte[length];
        for (int i = length - 1; i >= 0; i--) {
            bytes[i] = (byte) ((value >>> ((bytes.length - 1 - i) * 8)) & 0xFF);
        }
        return bytes;
    }

    /**
<<<<<<< HEAD
     *  Bits
     */

    public static int shiftOffset(byte mask){
        int offset = 0;
        for(;offset<8;offset++){
            if ((mask & 1) != 0)break;
            mask >>>=1;
=======
     * Bits
     */

    public static int shiftOffset(byte mask) {
        int offset = 0;
        for (; offset < 8; offset++) {
            if ((mask & 1) != 0) break;
            mask >>>= 1;
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
        }
        return offset;
    }

<<<<<<< HEAD
    public static byte getByteIntByMask(int num, byte mask){
        return (byte) (num<< shiftOffset(mask));
    }

    public static byte setByteIntByMask(byte b, int num, byte mask){
        return (byte) (getByteIntByMask(num,mask)| b);
    }

    public static int numOfBits(int bitmask,int pduLen){
        if(bitmask ==0){
            return pduLen * 8;
        }
        int numBits = Integer.toBinaryString(bitmask).length()
                -Integer.toBinaryString(bitmask).replaceAll("1","").length();
=======
    public static byte getByteIntByMask(int num, byte mask) {
        return (byte) (num << shiftOffset(mask));
    }

    public static byte setByteIntByMask(byte b, int num, byte mask) {
        return (byte) (getByteIntByMask(num, mask) | b);
    }

    public static int numOfBits(int bitmask, int pduLen) {
        if (bitmask == 0) {
            return pduLen * 8;
        }
        int numBits = Integer.toBinaryString(bitmask).length()
                - Integer.toBinaryString(bitmask).replaceAll("1", "").length();
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
        return numBits;
    }

}
