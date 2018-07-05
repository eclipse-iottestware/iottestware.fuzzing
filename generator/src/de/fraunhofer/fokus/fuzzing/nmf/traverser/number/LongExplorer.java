package de.fraunhofer.fokus.fuzzing.nmf.traverser.number;

public class LongExplorer extends NumberExplorer<Long> {
    private int runningInc = 0;
    private int runningDec = 0;

    @Override
    protected Long inc(Long n) {
        runningInc++;
        return n+1000000000;
    }

    @Override
    protected Long dec(Long n) {
        runningDec++;
        return n-1000000000;
    }

    @Override
    protected boolean compMax(Long max) {
        if (runningInc>1000) return false;
        return max <= Long.MAX_VALUE;
    }

    @Override
    protected boolean compMin(Long min) {
        if (runningDec>1000) return false;
        return min >= Long.MIN_VALUE;
    }

    @Override
    protected Long[] rtnValue(Long min, Long max) {
        runningInc = 0;
        runningDec = 0;
        return new Long[]{min,max};
    }
}
