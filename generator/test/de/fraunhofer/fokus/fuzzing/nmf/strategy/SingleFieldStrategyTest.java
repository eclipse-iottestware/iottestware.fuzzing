package de.fraunhofer.fokus.fuzzing.nmf.strategy;

import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestPduProvider;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class SingleFieldStrategyTest {

    @Test
    void getFieldCombinationList() {
        boolean hasCoapVersion = false;
        Strategy strategy = new SingleFieldStrategy();
        strategy.init(TestPduProvider.getSinglePdu());
        strategy.init(TestPduProvider.getSinglePdu());
        List<List<String>> set = strategy.getFieldCombinationList();
        for(List<String> activeFields:set){
            System.out.println(activeFields.get(0));
            hasCoapVersion=hasCoapVersion?true:activeFields.get(0).contains("version");
        }
        assertEquals(true,hasCoapVersion);
        assertEquals(6,set.size());

    }
}