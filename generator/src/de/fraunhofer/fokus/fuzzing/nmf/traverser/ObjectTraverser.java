package de.fraunhofer.fokus.fuzzing.nmf.traverser;

import de.fraunhofer.fokus.fuzzing.nmf.pcap.CodecWrapper;
import de.fraunhofer.fokus.fuzzing.nmf.FieldDescription;
import de.fraunhofer.fokus.fuzzing.nmf.pcap.UpdateTrigger;
import de.fraunhofer.fokus.fuzzing.nmf.traverser.array.ArrayExplorer;
import de.fraunhofer.fokus.fuzzing.nmf.traverser.number.IntegerExplorer;
import de.fraunhofer.fokus.fuzzing.nmf.traverser.number.LongExplorer;
import de.fraunhofer.fokus.fuzzing.nmf.traverser.number.NumberExplorer;
import org.etsi.common.ByteHelper;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.*;

public class ObjectTraverser {

    private final CodecWrapper codec;

    public ObjectTraverser(CodecWrapper codec) {
        this.codec = codec;
    }

//    public List<FieldDescription> traverse(byte[] pdu) {
//        currentOriginalPdu = pdu;
//        Object obj = codec.parse(pdu);
//        return traverseObject(obj);
//    }


    public List<FieldDescription> traverse(Object obj) {
        byte[] currentOriginalPdu = codec.serialize(obj);
        String currentOriginalPduStr = ByteHelper.byteArrayToHexString(currentOriginalPdu);
        Object currentObject = codec.parse(currentOriginalPdu);
        return traverse(obj, currentObject, currentOriginalPduStr);

    }

    public List<FieldDescription> traverse(Object obj, Object currentObject, String currentOriginalPduStr) {
        List<FieldDescription> currentFields = new ArrayList<>();
        Object currentValue;
        Method setter, getter;

        for (Method[] m : getSetterGetter(currentObject)) {
            setter = m[0];
            getter = m[1];
            currentValue = getGetterValue(currentObject, getter);
            if (currentValue == null) {
                continue;
            }
            List<FieldDescription> descriptions = exploreBoundaries(currentObject, setter, currentValue, currentOriginalPduStr);
            currentFields.addAll(descriptions);
        }
        Set<Map.Entry<Method, Object>> set = getSetterNewObjects(currentObject).entrySet();
        for (Map.Entry<Method, Object> pair : set) {
            //List<FieldDescription> descriptions = exploreBoundaries(currentObject, pair.getKey(), pair.getValue(), currentOriginalPduStr);
            //currentFields.addAll(descriptions);
        }


        return currentFields;
    }

    /**
     * Returns a array of relevant setter and getter pairs.
     * A pair of methods is considered a getter, setter pair if
     * they share the same suffix, despite of "set" and "get" and
     * if the getter returns value that is not null.
     * Relevant means that the getter does not return null
     *
     * @param obj
     * @return returns Pair(Method[]{setter,getter})
     */
    private static Method[][] getSetterGetter(Object obj) {
        List<Method[]> methodsList = new ArrayList<>();
        Class c = obj.getClass();
        Method[] methods = c.getMethods();
        for (Method setter : methods) {
            String name = setter.getName();
            if (name.startsWith("set")) {
                Method getter = getCorrespondingGetter(methods, setter);
                if (getter != null && getGetterValue(obj, getter) != null) {
                    methodsList.add(new Method[]{setter, getter});
                }
            }
        }
        return methodsList.toArray(new Method[methodsList.size()][]);
    }

    private static Map<Method, Object> getSetterNewObjects(Object obj) {
        Map<Method, Object> map = new LinkedHashMap<>();
        Class c = obj.getClass();
        Method[] methods = c.getMethods();
        for (Method setter : methods) {
            if (setter.getName().startsWith("set")
                    && setter.getParameterCount() == 1) {
                Class setterArg = setter.getParameterTypes()[0];
                Object argument = getEmptyPrimitive(setterArg);
                if (argument == null) argument = getEmptyObject(setterArg);
                if (argument != null) map.put(setter, argument);
            }
        }
        return map;
    }

    private static Object getEmptyObject(Class setterArgument) {
        Constructor[] constructors = setterArgument.getConstructors();
        for (Constructor ctor : constructors) {
            try {

                if (ctor.getParameterCount() == 0) {
                    return ctor.newInstance(new Object[]{});
                }
                if (ctor.getParameterCount() == 1) {
                    Class ctorArg = ctor.getParameterTypes()[0];
                    Object arg = getEmptyPrimitive(ctorArg);
                    if (arg != null) {
                        return ctor.newInstance(new Object[]{arg});
                    }
                }
            } catch (InstantiationException | IllegalAccessException | InvocationTargetException e) {
                e.printStackTrace();
            }

        }
        return null;
    }

    private static Object getEmptyPrimitive(Class argument) {
        String name = argument.getName();
        switch (name) {
            case "[B":
                return new byte[]{0};
            case "[C":
                return new char[]{'a'};
            case "java.lang.String":
                return "";
            default:
                return null;
        }
    }

    private List<FieldDescription> exploreBoundaries(Object obj,Method setter, Object currentValue, String originalPduStr) {
        List<FieldDescription> descriptions = new ArrayList<>();
        String name = currentValue.getClass().getName();
        NumberExplorer number = null;
        ArrayExplorer array = null;
        //TODO Explorer Factory
        final FieldDescription description = new FieldDescription();
        switch (name) {
            case "java.lang.Byte":
                break;
            case "java.lang.Long":
                number = new LongExplorer();
                break;
            case "java.lang.Integer":
                number = new IntegerExplorer();
                break;
            case "[B":
            case "[C":
                array = new ArrayExplorer(byte[].class,byte.class);
                break;
            default:
                //recursive call.
                //return traverse(obj, currentValue, originalPduStr);

            break;
        }
        UpdateTrigger ut = new UpdateTrigger() {
            @Override
            public void update(Object subObj) {
                //TODO subObj in altes root einbauen
                // clone -> List <Setter,value> -> foreach pair -1 set value
                updateFieldDescription(subObj, description, originalPduStr);
            }
        };
        //byte[] pdu = codec.serialize(obj);
        Object o = codec.parse(ByteHelper.hexStringToByteArray(originalPduStr));
        if (number != null) {
            number.exploreNumber(ut, o, setter, currentValue);
        }
        if( array != null){
            array.exploreArray(ut,o,setter,currentValue);
        }
        try {
            setter.invoke(obj, currentValue);
        } catch (IllegalAccessException | InvocationTargetException e) {
            //e.printStackTrace();
        }
        if (description.getStart() != Integer.MAX_VALUE || description.getEnd() != Integer.MIN_VALUE) {
            //description.setType(currentValue.getClass());
            description.setName(setter.getName().replaceFirst("set", ""));
            descriptions.add(description);
        }
        return descriptions;
    }

    private static Object getGetterValue(Object obj, Method getter) {
        try {
            return getter.invoke(obj);
        } catch (InvocationTargetException | IllegalAccessException e) {
            e.printStackTrace();
        }
        return null;
    }


    private static Method getCorrespondingGetter(Method[] methods, Method method) {
        String filterName = method.getName()
                .replaceFirst("set", "");
        String targetName;
        Class[] parameterTypes = method.getParameterTypes();
        for (Method m : methods) {
            targetName = m.getName().replaceFirst("get", "");
            Class returnType = m.getReturnType();
            for (Class p : parameterTypes) {
                if (targetName.toLowerCase().equals(filterName.toLowerCase())
                        && p.equals(returnType)) {
                    return m;
                }
            }
        }
        return null;
    }

    /**
     *
     * @param obj root Object with changed value
     * @param description
     * @param originalPduStr
     * @return
     */
    private boolean updateFieldDescription(Object obj, FieldDescription description, String originalPduStr) {
        Integer[] changed = positionsChanged(obj, originalPduStr);
        return updateFieldDescription(description, changed);

    }

    private boolean updateFieldDescription(FieldDescription description, Integer[] changedPositions) {
        if (changedPositions.length == 0) return false;
        boolean update = false;
        if (changedPositions[0] < description.getStart()) {
            description.setStart(changedPositions[0]);
            update = true;
        }
        if (changedPositions[changedPositions.length - 1] > description.getEnd()) {
            description.setEnd(changedPositions[changedPositions.length - 1]);
            update = true;
        }
        return update;
    }

    private Integer[] positionsChanged(Object changedRootObj, String originalHex) {
        List<Integer> poss = new ArrayList<>();
        byte[] serialized = codec.serialize(changedRootObj);
        String newPdu = ByteHelper.byteArrayToHexString(serialized);
        int pos = 0;
        while (pos < newPdu.length()
                && pos < originalHex.length()) {
            if (newPdu.charAt(pos) != originalHex.charAt(pos)) {
                poss.add(pos);
            }
            pos++;
        }
        while (pos < originalHex.length()) {
            poss.add(pos);
            pos++;
        }
        Integer[] rtn = new Integer[poss.size()];
        return poss.toArray(rtn);
    }

}
