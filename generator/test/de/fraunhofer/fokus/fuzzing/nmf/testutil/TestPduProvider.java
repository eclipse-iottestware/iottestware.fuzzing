package de.fraunhofer.fokus.fuzzing.nmf.testutil;

import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.json.JsonPduMapper;

import java.util.List;

public class TestPduProvider {

    public final static String fileCoapAll = "testdata/coap_bytes.json";
    public final static String fileMqttAll = "testdata/mqtt_bytes.json";
    public final static String fileCoapSingle = "testdata/singlePdu.json";
    public final static String fileResultCoap = "./testdata/coap_hex.txt";


    public static PduDescription getSinglePdu() {
        JsonPduMapper mapper = new JsonPduMapper();
        mapper.mapPdusFromFile(fileCoapSingle, "coap");
        return mapper.getPduList().get(0);
    }

    public static List<PduDescription> getPduList(String fileName, String prefix) {
        JsonPduMapper mapper = new JsonPduMapper();
        mapper.mapPdusFromFile(fileName, prefix);
        return mapper.getPduList();
    }

    public static List<PduDescription> getCoapPduList() {
        return getPduList(fileCoapAll, "coap");
    }

    public static List<PduDescription> getMqttPduList() {
        return getPduList(fileMqttAll, "mqtt");
    }


}
