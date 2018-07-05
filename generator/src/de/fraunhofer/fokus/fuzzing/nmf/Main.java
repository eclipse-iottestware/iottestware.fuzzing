package de.fraunhofer.fokus.fuzzing.nmf;


import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.ComputableFuzzingHeuristic;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.IntegerGenerator;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.IntegerGeneratorFactory;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.IntegerSpecification;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.RequestFactory;

import java.math.BigInteger;
import java.util.Iterator;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        long seed = 1337;
        IntegerSpecification specification = RequestFactory.INSTANCE.createNumberSpecification();
        specification.setBits(2);
        specification.setMaxValue(BigInteger.valueOf(0));
        specification.setMaxValue(BigInteger.valueOf(3));
        List<IntegerGenerator> allIntegerGenerators =
                IntegerGeneratorFactory.INSTANCE.createAll(specification, seed);
        for(IntegerGenerator gen:allIntegerGenerators){
            ComputableFuzzingHeuristic g = (ComputableFuzzingHeuristic) gen;
            Iterator<FuzzedValue<Long>> iterator = g.iterator();
            while (iterator.hasNext()){
                System.out.println(iterator.next().getValue());
            }
        }

    }
}
