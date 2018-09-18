package de.fraunhofer.fokus.fuzzing.nmf.util;

import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestPduProvider;
import org.junit.jupiter.api.Test;

class TextFileWriterTest {

    @Test
    void testHexFileWriter() {
        TextFileWriter hexFileWriter = new TextFileWriter(TestPduProvider.fileResultCoap);
        hexFileWriter.addHexLine("60453039C0FF49276D20616C697665202E2E2E");
        hexFileWriter.close();
    }

}