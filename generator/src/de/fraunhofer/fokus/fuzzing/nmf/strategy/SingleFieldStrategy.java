package de.fraunhofer.fokus.fuzzing.nmf.strategy;

import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.ComputableFuzzingHeuristic;
import de.fraunhofer.fokus.fuzzing.nmf.FieldDescription;
import de.fraunhofer.fokus.fuzzing.nmf.PduDescription;
import de.fraunhofer.fokus.fuzzing.nmf.generation.GeneratorProvider;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class SingleFieldStrategy implements Strategy {

    private PduDescription description;
    private Map<String, List<ComputableFuzzingHeuristic>> generator;
    private List<List<String>> strategy;

    public SingleFieldStrategy(PduDescription description) {
        this.description = description;
    }

    @Override
    public List<List<String>> getFieldCombinationList() {
        if (strategy == null) {
            Map<String, List<ComputableFuzzingHeuristic>> generatorMap = getGeneratorMap();
            strategy = new ArrayList<>();
            for (FieldDescription field : description.getFields()) {
                if(generatorMap.containsKey(field.getName())) {
                    List<String> activeFields = new ArrayList<>();
                    activeFields.add(field.getName());
                    strategy.add(activeFields);
                }
            }
        }
        return strategy;
    }

    @Override
    public Map<String, List<ComputableFuzzingHeuristic>> getGeneratorMap() {
        if (generator == null) generator = GeneratorProvider.getFieldGeneratorMap(description);
        return generator;
    }

    @Override
    public PduDescription getDescription() {
        return description;
    }
}
