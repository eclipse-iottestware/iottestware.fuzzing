package de.fraunhofer.fokus.fuzzing.nmf.strategy;

import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestPduProvider;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class SingleFieldStrategyTest {

    @Test
    void getFieldCombinationList() {
        boolean hasCoapVersion = false;
        boolean hasCoapPayload = false;
        Strategy strategy = new SingleFieldStrategy(TestPduProvider.getSinglePdu());
        List<List<String>> set = strategy.getFieldCombinationList();
        for(List<String> activeFields:set){
            System.out.println(activeFields.get(0));
            hasCoapVersion=hasCoapVersion?true:activeFields.get(0).contains("version");
            hasCoapPayload=hasCoapPayload?true:activeFields.get(0).contains("payload");
        }
        assertEquals(true,hasCoapVersion);
        assertEquals(true,hasCoapPayload);
        assertEquals(11,set.size());

    }
}