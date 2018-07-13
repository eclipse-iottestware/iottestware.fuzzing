package de.fraunhofer.fokus.fuzzing.nmf;


import de.fraunhofer.fokus.fuzzing.fuzzino.FuzzedValue;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.ComputableFuzzingHeuristic;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.IntegerGenerator;
import de.fraunhofer.fokus.fuzzing.fuzzino.heuristics.generators.IntegerGeneratorFactory;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.IntegerSpecification;
import de.fraunhofer.fokus.fuzzing.fuzzino.request.RequestFactory;
import de.fraunhofer.fokus.fuzzing.nmf.compilation.FuzzDataSetCompiler;
import de.fraunhofer.fokus.fuzzing.nmf.compilation.PduProcessor;
import de.fraunhofer.fokus.fuzzing.nmf.generation.FuzzedPduGenerator;
import de.fraunhofer.fokus.fuzzing.nmf.generation.FuzzedValueProvider;
import de.fraunhofer.fokus.fuzzing.nmf.json.JsonFilePduProcessor;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.SingleFieldStrategy;
import de.fraunhofer.fokus.fuzzing.nmf.strategy.Strategy;

import java.math.BigInteger;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class Main {

    public static void main(String[] args) {
        boolean jsonFile = false;
        String inputFilePath = null;
        String outputFilepath = null;
        String protocol = null;
        String errorMessage = null;
        PduProcessor processor = null;
        Strategy strategy = null;

        if (args.length > 0) {
            for (int i = 0; i < args.length; i++) {
                if (args[i].equals("-m") && args.length >= i + 1) {
                    switch (args[i + 1]) {
                        case "json":
                            jsonFile = true;
                            break;
                        default:
                            errorMessage = "Invalid mode. Use e.g. json";
                            break;
                    }
                }
                if (args[i].equals("-p") && args.length >= i + 1) {
                    protocol = args[i + 1];
                }
                if (args[i].equals("-o") && args.length >= i + 1) {
                    outputFilepath = args[i + 1];
                }
                if (args[i].equals("-i") && args.length >= i + 1) {
                    inputFilePath = args[i + 1];
                }
            }
        } else {
            errorMessage = "No arguments. Usage: -m <mode> -p <protocol> -i <inputfile> -o <outputfile>";
        }
        if (jsonFile) {
            if (inputFilePath == null || outputFilepath == null) {
                errorMessage = "This mode requires an input and an output file";
            }
        }
        if (errorMessage != null) {
            System.out.println(errorMessage);
            return;
        }
        if (jsonFile) {
            processor = new JsonFilePduProcessor(inputFilePath, outputFilepath, protocol);
            strategy = new SingleFieldStrategy();
        }
        if (processor != null && strategy != null) {
            FuzzDataSetCompiler compiler = new FuzzDataSetCompiler(processor, strategy);
            compiler.compile();
        }

    }


}
