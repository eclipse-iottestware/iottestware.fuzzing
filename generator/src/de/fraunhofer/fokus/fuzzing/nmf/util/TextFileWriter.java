package de.fraunhofer.fokus.fuzzing.nmf.util;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;

public class TextFileWriter {

    private Writer output;

    public TextFileWriter(String filename){
        try {
            output = new BufferedWriter(new FileWriter(filename));
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public void addHexLine(String line){
        try {
            output.append(line+"\n");
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public void close(){
        try {
            output.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
