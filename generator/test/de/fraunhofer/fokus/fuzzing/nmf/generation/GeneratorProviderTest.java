package de.fraunhofer.fokus.fuzzing.nmf.generation;

import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.ComputableFuzzingHeuristic;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestPduProvider;
import org.junit.jupiter.api.Test;

import java.util.Iterator;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class GeneratorProviderTest {

    @Test
    void getFieldGeneratorMap() {
        Map<String, List<ComputableFuzzingHeuristic>> map =
                GeneratorProvider.getFieldGeneratorMap(TestPduProvider.getSinglePdu());
        boolean has3 = false;
        boolean has0 = false;
        boolean has_1 = false;
        boolean has4 = false;
        int count=0;
        for (String key : map.keySet()) {
            int countKey=0;
            for (ComputableFuzzingHeuristic gen : map.get(key)) {
                Iterator<FuzzedValue> it = gen.iterator();
                while (it.hasNext()) {
                    long value = (Long) it.next().getValue();
                    has3 = has3 ? true : value == 3;
                    has0 = has0 ? true : value == 0;
                    has_1 = has_1 ? true : value == -1;
                    has4 = has4 ? true : value == 4;
                    count++;
                    countKey++;
                }
            }
            System.out.println(key+":"+countKey);
        }
        assertEquals(true,has3);
        assertEquals(true,has0);
        assertEquals(true,has_1);
        assertEquals(true,has4);
        System.out.println(count);

    }
}