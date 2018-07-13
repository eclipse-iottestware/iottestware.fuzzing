package de.fraunhofer.fokus.fuzzing.nmf;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class MainTest {

    @Test
    void main() {
        String args[] ={"-m","json","-p","coap","-i","./testdata/coap_bytes.json","-o","./testdata/out.txt"};
        Main.main(args);
    }
}