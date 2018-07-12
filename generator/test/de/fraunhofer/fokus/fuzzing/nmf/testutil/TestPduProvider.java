package de.fraunhofer.fokus.fuzzing.nmf.testutil;

import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.compilation.FuzzDataSetCompiler;
import de.fraunhofer.fokus.fuzzing.nmf.json.JsonPduMapper;

import java.util.List;

public class TestPduProvider {

    public final static String fileNameAll = "testdata/coap_bytes.json";
    public final static String fileNameSingle = "testdata/singlePdu.json";
    public final static String protocolPrefix = "coap";
    public final static String fileResult = "./testdata/coap_hex.txt";



    public static PduDescription getSinglePdu(){
        JsonPduMapper mapper = new JsonPduMapper();
        mapper.mapPdusFromFile(fileNameSingle,protocolPrefix);
        return mapper.getPduList().get(0);
    }

    public static List<PduDescription> getPduList(){
        JsonPduMapper mapper = new JsonPduMapper();
        mapper.mapPdusFromFile(fileNameAll,protocolPrefix);
        return mapper.getPduList();
    }


}
