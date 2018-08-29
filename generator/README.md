# Network Mutation Fuzzer

To run, please execute the following:

```
mvn clean package
cd target
java -jar nmf-0.1.jar -m json -p coap -i ../testdata/coap_bytes.json -o ../../ttcn3_execution/fuzzing-integration/fuzzdata/coap.txt
```