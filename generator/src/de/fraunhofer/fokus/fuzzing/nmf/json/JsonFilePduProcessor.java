package de.fraunhofer.fokus.fuzzing.nmf.json;

import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.compilation.PduProcessor;
import de.fraunhofer.fokus.fuzzing.nmf.util.TextFileWriter;

import java.util.List;

public class JsonFilePduProcessor implements PduProcessor {

    private List<PduDescription> originalPdus;
    private TextFileWriter hexFileWriter;

    public JsonFilePduProcessor(String inputPath, String outputPath, String protocol) {
        JsonPduMapper mapper = new JsonPduMapper();
        mapper.mapPdusFromFile(inputPath, protocol);
        this.originalPdus = mapper.getPduList();
        this.hexFileWriter = new TextFileWriter(outputPath);
    }


    @Override
    public void onNewPdu(String pdu) {
        hexFileWriter.addHexLine(pdu);
    }

    @Override
    public List<PduDescription> getPduList() {
        return originalPdus;
    }

    @Override
    public void done() {
        hexFileWriter.close();
    }
}
