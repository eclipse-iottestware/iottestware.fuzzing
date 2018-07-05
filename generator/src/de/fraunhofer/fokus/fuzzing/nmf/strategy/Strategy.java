package de.fraunhofer.fokus.fuzzing.nmf.strategy;

import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.ComputableFuzzingHeuristic;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;

import java.util.List;
import java.util.Map;

public interface Strategy {

    public List<List<String>> getFieldCombinationList();

    public Map<String, List<ComputableFuzzingHeuristic>> getGeneratorMap();

    public PduDescription getDescription();
}
