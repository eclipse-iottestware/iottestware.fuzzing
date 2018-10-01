package de.fraunhofer.fokus.fuzzing.nmf.json;

import de.fraunhofer.fokus.fuzzing.nmf.FieldDescription;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.testutil.TestPduProvider;
import org.junit.jupiter.api.Test;

class JsonPduMapperTest {

    private final String fileName = "testdata/coap_bytes.json";
    private final String protocolPrefix = "coap";

    @Test
    void mapPdusFromFile() {
        for(PduDescription pdu: TestPduProvider.getCoapPduList()){
            System.out.println(pdu.getPduStr());
            for(FieldDescription field:pdu.getFields()){
                System.out.println(field);
            }
            System.out.println("###");
        }

    }

    @Test
    void getPduList() {
    }
}