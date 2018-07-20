package de.fraunhofer.fokus.fuzzing.nmf;

public class TypeIdentificator {

    private static final String NUMBERS = "\\d+";

    public static FieldType identfyType(String data){
        if(data.matches(NUMBERS)){
            return FieldType.INTEGER;
        }else{
            return FieldType.STRING;
        }

    }
}
