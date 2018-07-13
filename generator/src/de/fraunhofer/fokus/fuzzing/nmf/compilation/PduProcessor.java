package de.fraunhofer.fokus.fuzzing.nmf.compilation;

import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;

import java.util.List;

public interface PduProcessor {

    public void onNewPdu(String pdu);

    public List<PduDescription> getPduList();

    public void done();
}
