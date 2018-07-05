package de.fraunhofer.fokus.fuzzing.nmf.generation;

import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.ComputableFuzzingHeuristic;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.IntegerGenerator;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.IntegerGeneratorFactory;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.IntegerSpecification;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.RequestFactory;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.TypeSpecification;
import de.fraunhofer.fokus.fuzzing.nmf.FieldDescription;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.util.BitHelper;

import java.math.BigInteger;
import java.util.*;

public class GeneratorProvider {

    private final static int SEED = 1337;

    /**
     * @param description
     * @return Map of FildId to Generator
     */
    public static Map<String, List<ComputableFuzzingHeuristic>> getFieldGeneratorMap(PduDescription description) {
        Map<String, List<ComputableFuzzingHeuristic>> map = new HashMap<>();
        for (FieldDescription field : description.getFields()) {
            switch (field.getType()) {
                case INTEGER:
                    map.put(field.getName(),getIntegerGenerators(field));
                    break;
            }
        }
        return map;
    }


    private static List<ComputableFuzzingHeuristic> getIntegerGenerators(FieldDescription field) {
        List<ComputableFuzzingHeuristic> generators = new ArrayList<>();
        List<IntegerGenerator> allIntegerGenerators =
                IntegerGeneratorFactory.INSTANCE.createAll(getIntegerSpecification(field), SEED);
        for(IntegerGenerator gen:allIntegerGenerators){
            generators.add(gen);
        }
        return generators;
    }

    private static IntegerSpecification getIntegerSpecification(FieldDescription field) {
        IntegerSpecification specification = RequestFactory.INSTANCE.createNumberSpecification();
        int bits = BitHelper.numOfBits(field.getBitmask(), field.getEnd() - field.getStart());
        specification.setBits(bits);
        specification.setIsSigned(false);
        //TODO implement boundaries
        specification.setMinValue(BigInteger.valueOf(0));
        specification.setMaxValue(BigInteger.valueOf((long) Math.pow(2, bits) - 1));
        return specification;
    }

}
