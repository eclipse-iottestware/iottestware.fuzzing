package de.fraunhofer.fokus.fuzzing.nmf.pcap;


import de.fraunhofer.fokus.fuzzing.nmf.coap.CoapTypeHandler;
import de.fraunhofer.fokus.fuzzing.nmf.pcap.PduTypeHandler;
import org.jnetpcap.Pcap;
import org.jnetpcap.packet.JPacket;
import org.jnetpcap.packet.JPacketHandler;
import org.jnetpcap.protocol.tcpip.Udp;

class PduTypeHandlerTest {

    final String FILENAME = "testdata/coap.xml.pcap";
    final StringBuilder errbuf = new StringBuilder();
    final PduTypeHandler coapType = new CoapTypeHandler();
    final Pcap pcap = Pcap.openOffline(FILENAME, errbuf);

    @org.junit.jupiter.api.BeforeEach
    void setUp() {
        if (pcap == null) {
            System.err.println(errbuf);
            return;
        }
    }

    @org.junit.jupiter.api.AfterEach
    void tearDown() {
    }

    @org.junit.jupiter.api.Test
    void getList() {
    }

    @org.junit.jupiter.api.Test
    void isPduType() {

        pcap.loop(1000, new JPacketHandler<StringBuilder>() {
            final Udp udp = new Udp();

            public void nextPacket(JPacket packet, StringBuilder errbuf) {
                if (packet.hasHeader(Udp.ID)) {
                    packet.getHeader(udp);
                    if(coapType.isPduType(udp.getPayload())){
//                        System.out.printf("frame #%d%n", packet.getFrameNumber());
//                        byte[] data = packet.getByteArray(0, packet.size());
//                        ByteHelper.dump("Packet", data);
//                        System.out.printf("udp.dst_port=%d%n", udp.destination());
//                        System.out.printf("udp.src_port=%d%n", udp.source());
                    }
                }

            }
        }, errbuf);

    }
}