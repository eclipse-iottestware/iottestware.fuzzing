package de.fraunhofer.fokus.fuzzing.nmf.traverser.number;

import de.fraunhofer.fokus.fuzzing.nmf.pcap.UpdateTrigger;

import java.lang.reflect.Method;

public abstract class NumberExplorer<T extends Number> {

    protected abstract T inc(T n);
    protected abstract T dec(T n);
    protected abstract boolean compMax(T max);
    protected abstract boolean compMin(T min);
    protected abstract T[] rtnValue(T min,T max);

    public T[] exploreNumber(UpdateTrigger trigger, Object obj, Method setter, Object currentValue) {
        T currentT = (T) currentValue;
        T max = currentT;
        T min = currentT;
        do {
            try {
                setter.invoke(obj, max);
                max = inc(max);
            } catch (Exception e) {
                break;
            }
        } while (compMax(max));
        trigger.update(obj);
        do {
            try {
                setter.invoke(obj, min);
                min = dec(min);
            } catch (Exception e) {
                break;
            }
        } while (compMin(min));
        trigger.update(obj);
        return rtnValue(min,max);
    }

}
