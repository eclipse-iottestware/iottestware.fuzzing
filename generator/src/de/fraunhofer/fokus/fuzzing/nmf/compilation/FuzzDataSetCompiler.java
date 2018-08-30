package de.fraunhofer.fokus.fuzzing.nmf.compilation;

import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.generation.FuzzedPduGenerator;
import de.fraunhofer.fokus.fuzzing.nmf.generation.FuzzedValueProvider;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.Strategy;

import java.util.Map;

public class FuzzDataSetCompiler {

    private final PduProcessor pduProcessor;
    private final Strategy strategy;


    public FuzzDataSetCompiler(PduProcessor pduProcessor, Strategy strategy) {
<<<<<<< HEAD

=======
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
        this.pduProcessor = pduProcessor;
        this.strategy = strategy;
    }

    public void compile() {
        for (PduDescription pdu : pduProcessor.getPduList()) {
            generateFuzzedPdus(pdu);
        }
    }


    private void generateFuzzedPdus(PduDescription pdu) {
        strategy.init(pdu);
        FuzzedValueProvider valueProvider = new FuzzedValueProvider();
        valueProvider.generateByStrategy(strategy);
        while (valueProvider.hasNext()) {
            Map<String, FuzzedValue> values = valueProvider.nextSetValues();
            String s = FuzzedPduGenerator.generateFuzzedPdu(strategy.getDescription(), values);
            pduProcessor.onNewPdu(s);
        }
    }
}
