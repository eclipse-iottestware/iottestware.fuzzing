package de.fraunhofer.fokus.fuzzing.nmf;

<<<<<<< HEAD
=======
import de.fraunhofer.fokus.fuzzing.nmf.util.BitsAndByteHelper;

>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
public class TypeIdentificator {

    private static final String NUMBERS = "\\d+";

    public static FieldType identfyType(String data){
        if(data.matches(NUMBERS)){
            return FieldType.INTEGER;
        }else{
<<<<<<< HEAD
=======
            String s = BitsAndByteHelper.hexStringToString(data);
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
            return FieldType.STRING;
        }

    }
}
