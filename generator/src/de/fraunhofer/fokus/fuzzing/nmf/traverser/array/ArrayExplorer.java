package de.fraunhofer.fokus.fuzzing.nmf.traverser.array;

import de.fraunhofer.fokus.fuzzing.nmf.pcap.UpdateTrigger;

import java.lang.reflect.Array;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class ArrayExplorer<T, E> {

    final Class<T> arrayClass;
    final Class<E> typeClass;

    public ArrayExplorer(Class<T> typeParameterClass, Class<E> typeClass) {
        this.arrayClass = typeParameterClass;
        this.typeClass = typeClass;
    }

    public void exploreArray(UpdateTrigger trigger, Object obj, Method setter, Object currentValue) {
        //add new Elements
        if (!currentValue.getClass().isArray()) return;
        Object[] tmp;
        E t;
        int len = Array.getLength(currentValue);
        while (len < 10000) {
            tmp = new Object[len];
            //tmp = (E[]) Array.newInstance(typeClass,len);
            for (int i = 0; i < len; i++) {
                Object o = Array.get(currentValue, 0);
                //setValue(tmp, i, o);
                tmp[i]= o;
                //Array.setByte(tmp,i, (Byte) o);
            }
            try {
                setter.invoke(obj, new byte[]{77,77,77,77,77,77,77});
                trigger.update(obj);
            } catch (IllegalAccessException | InvocationTargetException e) {
                e.printStackTrace();
                break;
            }
            len *= len;
        }
    }


    private byte[] copy(Object[] array){
        byte[] rtn = (byte[]) Array.newInstance(typeClass,array.length);
        return rtn;
    }

//    private void invokeValue(Object obj, Method setter, Object array) {
//        int len = Array.getLength(array);
//        if(len==0){
//            return;
//        }
//        Object first = Array.get(array,0);
//        if (first instanceof Byte) {
//            byte[] byteArray = new byte[len];
//            Arrays.copyOf()
//            Array.setByte(array, index, (byte) value);
//            return;
//        }
//        //array[index]= (E) value;
//
//    }

}
