package de.fraunhofer.fokus.fuzzing.nmf;

import java.util.List;

public class PduDescription {

    private List<FieldDescription> fields;
    private String pduStr;


    public List<FieldDescription> getFields() {
        return fields;
    }

    public void setFields(List<FieldDescription> fields) {
        this.fields = fields;
    }

    public String getPduStr() {
        return pduStr;
    }

    public void setPduStr(String pduStr) {
        this.pduStr = pduStr;
    }
}
