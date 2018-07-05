package de.fraunhofer.fokus.fuzzing.nmf.pcap;

public interface CodecWrapper<T> {

    public byte[] serialize(T obj);
    public T parse(byte[] pdu);
}
