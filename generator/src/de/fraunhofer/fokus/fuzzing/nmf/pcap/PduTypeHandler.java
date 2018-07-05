package de.fraunhofer.fokus.fuzzing.nmf.pcap;

import de.fraunhofer.fokus.fuzzing.nmf.FieldDescription;

import java.util.List;

public interface PduTypeHandler {
    public List<FieldDescription> getList();

    public boolean isPduType(byte[] pdu);
}
