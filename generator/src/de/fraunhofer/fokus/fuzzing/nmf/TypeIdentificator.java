package de.fraunhofer.fokus.fuzzing.nmf;

import de.fraunhofer.fokus.fuzzing.nmf.util.BitsAndByteHelper;

public class TypeIdentificator {

    private static final String NUMBERS = "\\d+";

    public static FieldType identfyType(String data){
        if(data.matches(NUMBERS)){
            return FieldType.INTEGER;
        }else{
            String s = BitsAndByteHelper.hexStringToString(data);
            return FieldType.STRING;
        }

    }
}
