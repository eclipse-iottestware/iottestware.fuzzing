package de.fraunhofer.fokus.fuzzing.nmf.generation;

import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.SingleFieldStrategy;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.Strategy;
import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestPduProvider;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

class FuzzedPduGeneratorTest {

    @Test
    void generateFuzzedCoapPdu() {
        generateFuzzedPdu(TestPduProvider.getCoapPduList());
    }

    @Test
    void generateFuzzedMqttPdu() {
        generateFuzzedPdu(TestPduProvider.getMqttPduList());
    }

    private void generateFuzzedPdu(List<PduDescription> list) {
        for (PduDescription pdu : list) {
            singlePdu(pdu);
        }
    }

    private void singlePdu(PduDescription pdu) {
        Strategy strategy = new SingleFieldStrategy();
        strategy.init(pdu);
        FuzzedValueProvider valueProvider = new FuzzedValueProvider();
        valueProvider.generateByStrategy(strategy);
        while (valueProvider.hasNext()) {
            Map<String, FuzzedValue> values = valueProvider.nextSetValues();
            String s = FuzzedPduGenerator.generateFuzzedPdu(strategy.getDescription(), values);
            System.out.println(s);
        }
    }
}