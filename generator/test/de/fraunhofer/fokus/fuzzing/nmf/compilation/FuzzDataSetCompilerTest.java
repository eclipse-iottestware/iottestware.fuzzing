package de.fraunhofer.fokus.fuzzing.nmf.compilation;

import de.fraunhofer.fokus.fuzzing.nmf.json.JsonFilePduProcessor;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.SingleFieldStrategy;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.Strategy;
import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestPduProvider;
import org.junit.jupiter.api.Test;

class FuzzDataSetCompilerTest {

    @Test
    void compileJson() {
        Strategy strategy = new SingleFieldStrategy();
        PduProcessor processor = new JsonFilePduProcessor(
                TestPduProvider.fileCoapAll,
                TestPduProvider.fileResultCoap,
                "coap"
        );
        FuzzDataSetCompiler compiler = new FuzzDataSetCompiler(processor,strategy);
        compiler.compile();
    }
}