package de.fraunhofer.fokus.fuzzing.nmf;

public class FieldDescription {

    private int start = Integer.MAX_VALUE;
    private int end = Integer.MIN_VALUE;
    private FieldType type;
    private Object boundaries;
    private int bitmask;
    private String name;


    public int getStart() {
        return start;
    }

    public void setStart(int start) {
        this.start = start;
    }

    public int getEnd() {
        return end;
    }

    public void setEnd(int end) {
        this.end = end;
    }

    public FieldType getType() {
        return type;
    }

    public void setType(FieldType type) {
        this.type = type;
    }

    public Object getBoundaries() {
        return boundaries;
    }

    public void setBoundaries(Object boundaries) {
        this.boundaries = boundaries;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String toString() {
        return name
                + (type != null ? " is " + type.toString() : "")
                + ": " + start + " - " + end;
    }

    public int getBitmask() {
        return bitmask;
    }

    public void setBitmask(int bitmask) {
        this.bitmask = bitmask;
    }
}
