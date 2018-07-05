package de.fraunhofer.fokus.fuzzing.nmf.testutil;

import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.json.JsonPduMapper;

import java.util.List;

public class TestPduProvider {

    private final static String fileNameAll = "testdata/coap_bytes.json";
    private final static String fileNameSingle = "testdata/singlePdu.json";
    private final static String protocolPrefix = "coap";


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
