package de.fraunhofer.fokus.fuzzing.nmf.generation;

import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.ComputableFuzzingHeuristic;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.IntegerGenerator;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.IntegerGeneratorFactory;
<<<<<<< HEAD
import de.fraunhofer.fokus.fuzzing.fuzzino.request.IntegerSpecification;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.RequestFactory;
=======
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.StringGenerator;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.StringGeneratorFactory;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.IntegerSpecification;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.RequestFactory;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.StringSpecification;
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
import de.fraunhofer.fokus.fuzzing.nmf.FieldDescription;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.util.BitsAndByteHelper;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class GeneratorProvider {

    private final static int SEED = 1337;

    /**
     * @param description
     * @return Map of FieldId to Generator
     */
    public static Map<String, List<ComputableFuzzingHeuristic>> getFieldGeneratorMap(PduDescription description) {
        Map<String, List<ComputableFuzzingHeuristic>> map = new HashMap<>();
        for (FieldDescription field : description.getFields()) {
            switch (field.getType()) {
                case INTEGER:
<<<<<<< HEAD
                    map.put(field.getName(),getIntegerGenerators(field));
                    break;
=======
                    map.put(field.getName(), getIntegerGenerators(field));
                    break;
                case STRING:
                    map.put(field.getName(), getStringGenerators(field));
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
            }
        }
        return map;
    }


    private static List<ComputableFuzzingHeuristic> getIntegerGenerators(FieldDescription field) {
        List<ComputableFuzzingHeuristic> generators = new ArrayList<>();
        List<IntegerGenerator> allIntegerGenerators =
                IntegerGeneratorFactory.INSTANCE.createAll(getIntegerSpecification(field), SEED);
<<<<<<< HEAD
        for(IntegerGenerator gen:allIntegerGenerators){
=======
        for (IntegerGenerator gen : allIntegerGenerators) {
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
            generators.add(gen);
        }
        return generators;
    }

    private static IntegerSpecification getIntegerSpecification(FieldDescription field) {
        IntegerSpecification specification = RequestFactory.INSTANCE.createNumberSpecification();
        int bits = BitsAndByteHelper.numOfBits(field.getBitmask(), field.getEnd() - field.getStart());
        specification.setBits(bits);
        specification.setIsSigned(false);
        //TODO implement boundaries
        specification.setMinValue(BigInteger.valueOf(0));
        specification.setMaxValue(BigInteger.valueOf((long) Math.pow(2, bits) - 1));
        return specification;
    }

<<<<<<< HEAD
=======
    private static List<ComputableFuzzingHeuristic> getStringGenerators(FieldDescription field) {
        List<ComputableFuzzingHeuristic> generators = new ArrayList<>();
        StringSpecification stringSpecification = RequestFactory.INSTANCE.createStringSpecification();
        stringSpecification.setMaxLength(field.getEnd() - field.getStart());
        //TODO string types parse
        List<StringGenerator> all = StringGeneratorFactory.INSTANCE.createAll(stringSpecification, SEED);
        for (StringGenerator gen : all) {
            generators.add(gen);
        }
        return generators;
    }

>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
}
