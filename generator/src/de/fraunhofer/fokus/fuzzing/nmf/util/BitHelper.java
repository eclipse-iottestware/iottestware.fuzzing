package de.fraunhofer.fokus.fuzzing.nmf.util;

public class BitHelper {

    public static int shiftOffset(byte mask){
        int offset = 0;
        for(;offset<8;offset++){
            if ((mask & 1) != 0)break;
            mask >>>=1;
        }
        return offset;
    }

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
        return numBits;
    }

}
