package de.fraunhofer.fokus.fuzzing.nmf.generation;

import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.SingleFieldStrategy;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.Strategy;
import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestPduProvider;
import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestValueProvider;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class FuzzedValueProviderTest {

    @Test
    void generateByStrategy() {
        List<FuzzedValue> singlePduValues = TestValueProvider.getSinglePduValues();
        Strategy strategy = new SingleFieldStrategy();
        strategy.init(TestPduProvider.getSinglePdu());
        FuzzedValueProvider valueProvider = new FuzzedValueProvider();
        valueProvider.generateByStrategy(strategy);
        Map<String,Integer> countKey = new HashMap<>();
        int count=0;
        while (valueProvider.hasNext()){
            Map<String, FuzzedValue> values = valueProvider.nextSetValues();
            String key = values.keySet().iterator().next();
            if(countKey.containsKey(key)){
               countKey.put(key,countKey.get(key)+1);
            }else {
                countKey.put(key,1);
            }
            //System.out.println(count+":"+values);
            count++;
        }
        for(String key:countKey.keySet()){
            //System.out.println(key+":"+countKey.get(key));
        }
        assertEquals(singlePduValues.size(),count);
    }

    @Test
    void hasNextSetValues() {
    }

    @Test
    void nextSetValues() {
    }

    @Test
    void hasNext() {
    }

    @Test
    void getIterator() {
    }
}