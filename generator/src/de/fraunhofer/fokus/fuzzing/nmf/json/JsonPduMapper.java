package de.fraunhofer.fokus.fuzzing.nmf.json;

import com.google.gson.*;
import com.google.gson.stream.JsonReader;
import de.fraunhofer.fokus.fuzzing.nmf.FieldDescription;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.TypeIdentificator;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class JsonPduMapper {

    private List<PduDescription> pdus;

    public JsonPduMapper() {
        this.pdus = new ArrayList<>();
    }


    public void mapPdusFromFile(String fileName, String protocolPrefix) {
        try (JsonReader jsonReader = new JsonReader(new InputStreamReader(new FileInputStream(fileName), "UTF-8"))) {
            Gson gson = new GsonBuilder().create();
            jsonReader.beginArray();
            int posInFrame = 0;
            while (jsonReader.hasNext()) {
                List<FieldDescription> fields = new ArrayList<>();
                String raw = null;
                JsonObject packet = gson.fromJson(jsonReader, JsonObject.class);
                JsonObject frame = packet.getAsJsonObject("_source").getAsJsonObject("layers");
                JsonArray pdu_raw = frame.getAsJsonArray(protocolPrefix + "_raw");
                //"coap_raw": ["hex", start, length, bitmask, type]
                JsonObject pdu = frame.getAsJsonObject(protocolPrefix);
                raw = pdu_raw.get(0).getAsString();
                posInFrame = pdu_raw.get(1).getAsInt();
                fields.addAll(getFieldsFromObject(posInFrame, pdu));
                if (!fields.isEmpty()) {
                    PduDescription description = new PduDescription();
                    description.setFields(fields);
                    description.setPduStr(raw);
                    pdus.add(description);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return;
    }

    private List<FieldDescription> getFieldsFromObject(int offset, JsonObject obj) {
        List<FieldDescription> fields = new ArrayList<>();
        for (Map.Entry<String, JsonElement> entry : obj.entrySet()) {
            if (entry.getKey().endsWith("_tree")) {
                fields.addAll(getFieldsFromObject(offset, entry.getValue().getAsJsonObject()));
            }
            if (entry.getKey().endsWith("_raw")) {
                JsonArray array = entry.getValue().getAsJsonArray();
                FieldDescription description = new FieldDescription();
                description.setName(entry.getKey().replace("_raw", ""));
                int start = array.get(1).getAsInt() - offset;
                description.setStart(start);
                description.setEnd(start + array.get(2).getAsInt()-1);
                description.setBitmask(array.get(3).getAsInt());
                description.setType(TypeIdentificator.identfyType(array.get(0).getAsString()));
                fields.add(description);
            }
        }
        return fields;
    }

    public List<PduDescription> getPduList() {
        return pdus;
    }


}
