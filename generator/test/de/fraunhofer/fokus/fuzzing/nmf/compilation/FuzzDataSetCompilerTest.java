package de.fraunhofer.fokus.fuzzing.nmf.compilation;

import de.fraunhofer.fokus.fuzzing.nmf.json.JsonFilePduProcessor;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.SingleFieldStrategy;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.Strategy;
import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestPduProvider;
import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestValueProvider;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FuzzDataSetCompilerTest {

    @Test
    void compileJson() {
        Strategy strategy = new SingleFieldStrategy();
        PduProcessor processor = new JsonFilePduProcessor(
                TestPduProvider.fileNameAll,
                TestPduProvider.fileResult,
                TestPduProvider.protocolPrefix
        );
        FuzzDataSetCompiler compiler = new FuzzDataSetCompiler(processor,strategy);
        compiler.compile();
    }
}