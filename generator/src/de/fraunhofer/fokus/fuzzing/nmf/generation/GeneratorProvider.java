package de.fraunhofer.fokus.fuzzing.nmf.generation;

import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.ComputableFuzzingHeuristic;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.IntegerGenerator;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.IntegerGeneratorFactory;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.StringGenerator;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.StringGeneratorFactory;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.IntegerSpecification;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.RequestFactory;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.StringSpecification;
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
        List<ComputableFuzzingHeuristic> newGeneratorList;
        for (FieldDescription field : description.getFields()) {
            newGeneratorList = null;
            switch (field.getType()) {
                case INTEGER:
                    map.put(field.getName(), getIntegerGenerators(field));
                    break;
                case STRING:
                    map.put(field.getName(), getStringGenerators(field));
                default:
                    break;
            }
            if (newGeneratorList != null && newGeneratorList.size() == 0) {
                System.out.println("Can't provide data for " + field.getName());
            }
        }
        return map;
    }


    private static List<ComputableFuzzingHeuristic> getIntegerGenerators(FieldDescription field) {
        List<ComputableFuzzingHeuristic> generators = new ArrayList<>();
        List<IntegerGenerator> allIntegerGenerators =
                IntegerGeneratorFactory.INSTANCE.createAll(getIntegerSpecification(field), SEED);
        for (IntegerGenerator gen : allIntegerGenerators) {
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

}
