package de.fraunhofer.fokus.fuzzing.nmf.traverser.number;

import de.fraunhofer.fokus.fuzzing.nmf.traverser.number.NumberExplorer;

public class IntegerExplorer extends NumberExplorer<Integer> {
    private int runningInc = 0;
    private int runningDec = 0;

    @Override
    protected Integer inc(Integer n) {
        runningInc++;
        return n+1;
    }

    @Override
    protected Integer dec(Integer n) {
        runningDec++;
        return n-1;
    }

    @Override
    protected boolean compMax(Integer max) {
        if (runningInc>(1<<16)) return false;
        return max <= Integer.MAX_VALUE;
    }

    @Override
    protected boolean compMin(Integer min) {
        if (runningDec>(1<<16)) return false;
        return min >= Integer.MIN_VALUE;
    }

    @Override
    protected Integer[] rtnValue(Integer min, Integer max) {
        runningInc = 0;
        runningDec = 0;
        return new Integer[]{min,max};
    }
}
