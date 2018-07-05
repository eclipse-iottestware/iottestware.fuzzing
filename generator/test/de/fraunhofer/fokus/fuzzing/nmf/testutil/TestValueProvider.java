package de.fraunhofer.fokus.fuzzing.nmf.testutil;

import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.ComputableFuzzingHeuristic;
import de.fraunhofer.fokus.fuzzing.nmf.generation.GeneratorProvider;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class TestValueProvider {

    public static List<FuzzedValue> getSinglePduValues() {
        List<FuzzedValue> values = new ArrayList<>();
        Map<String, List<ComputableFuzzingHeuristic>> map =
                GeneratorProvider.getFieldGeneratorMap(TestPduProvider.getSinglePdu());
        for (String key : map.keySet()) {
            for (ComputableFuzzingHeuristic gen : map.get(key)) {
                Iterator<FuzzedValue> it = gen.iterator();
                while (it.hasNext()) {
                    values.add(it.next());
                }
            }
        }
        return values;
    }

}
