package de.fraunhofer.fokus.fuzzing.nmf.generation;

import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.ComputableFuzzingHeuristic;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.Strategy;

import java.util.*;

public class FuzzedValueProvider {

    private Map<String, List<ComputableFuzzingHeuristic>> fieldGeneratorMap;
    private List<List<String>> fieldListSet;
    private int currentSetPos;
    private int currentFieldListPos;
    private Map<String, List<Iterator<FuzzedValue>>> currentIterators;
    private Map<String, Integer> currentPositionMap; // position in iterator list of  currentIterators.
    private Map<String, FuzzedValue> currentValues;


    public void generateByStrategy(Strategy strategy) {
        init(strategy);
    }

    private void init(Strategy strategy) {
        fieldGeneratorMap = strategy.getGeneratorMap();
        fieldListSet = strategy.getFieldCombinationList();
        currentSetPos = 0;
        initCurrentSet();
    }

    private void initCurrentSet() {
        List<String> fieldIds = fieldListSet.get(currentSetPos);
        currentIterators = new HashMap<>();
        currentPositionMap = new HashMap<>();
        currentValues = new HashMap<>();
        for (String fieldId : fieldIds) {
            resetCurrentField(fieldId);
        }
        currentFieldListPos = 0;
    }

    private Iterator<FuzzedValue> getCurrentIteratorById(String currentFieldId) {
        int posIterator = currentPositionMap.get(currentFieldId);
        List<Iterator<FuzzedValue>> iterators = currentIterators.get(currentFieldId);
        return iterators.get(posIterator);
    }

    private String getCurrentFieldId() {
        return fieldListSet.get(currentSetPos).get(currentFieldListPos);
    }

    private void resetCurrentField(String fieldId) {
        List<Iterator<FuzzedValue>> iterators = new ArrayList<>();
        for (ComputableFuzzingHeuristic generator : fieldGeneratorMap.get(fieldId)) {
            iterators.add(generator.iterator());
        }
        currentIterators.put(fieldId, iterators);
        currentPositionMap.put(fieldId, 0);
        currentValues.put(fieldId, getCurrentIteratorById(fieldId).next());
    }

    public boolean hasNextSetValues() {
        List<String> set = fieldListSet.get(currentSetPos);
        String lastFieldId = set.get(set.size() - 1);
        Iterator<FuzzedValue> iterator = getCurrentIteratorById(lastFieldId);
        boolean b = iterator.hasNext();
        if (!b) {
            return false;
        }
        return b;
    }

    /**
     * Reset the field pointer to the foremost postion in the grid.
     * After the usage of the net field iterator.
     */
    private void setForemostFieldId() {
        if (currentFieldListPos == 0) return;
        //prev field iterator;
        String prevFieldId = fieldListSet.get(currentSetPos).get(currentFieldListPos - 1);
        if (currentIterators.get(prevFieldId).get(0).hasNext()) {
            currentFieldListPos--;
            setForemostFieldId();
        }
    }

    public Map<String, FuzzedValue> nextSetValues() {
        Map<String, FuzzedValue> rtn = new HashMap<>(currentValues);
        prepareNextSetValues();
        return rtn;
    }

    public void prepareNextSetValues() {
        if (!hasNextSetValues()) {
            //end of field set
            currentSetPos++;
            if (currentSetPos < fieldListSet.size()) {
                initCurrentSet();
            } else {
                currentValues = null;
            }
            return;
        }
        //get current iterator by field and position
        String currentFieldId = getCurrentFieldId();
        int pos = currentPositionMap.get(currentFieldId);
        Iterator<FuzzedValue> iterator = currentIterators.get(currentFieldId).get(pos);
        if (iterator.hasNext()) {
            //save value
            currentValues.put(currentFieldId, iterator.next());
        } else {
            //TODO Untested code
            //switch to next iterator
            pos++;
            if (pos < currentIterators.get(currentFieldId).size()) {
                //iterators left in the field list.
                currentPositionMap.put(currentFieldId, pos);
            }
            if (pos == currentIterators.get(currentFieldId).size()
                //&& currentFieldListPos != fieldListSet.get(currentSetPos).size() - 1
                    ) {
                //reset iterators
                resetCurrentField(currentFieldId);
                //next field
                currentFieldListPos++;
            }
            prepareNextSetValues();
        }
        if (hasNextSetValues()) {
            //reset after single use of previous one
            currentFieldListPos = 0;
        }
    }

    public boolean hasNext() {
        return currentValues != null;
    }

    public Iterator<String> getIterator() {
        return new Iterator<String>() {
            @Override
            public boolean hasNext() {
                return false;
            }

            @Override
            public String next() {
                return null;
            }
        };
    }

}
