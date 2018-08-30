# Network Mutation Fuzzer

To run, please execute the following:

```
<<<<<<< HEAD
mvn scm:checkout package
=======
mvn clean package
>>>>>>> 3cbe68524d67fff6ee5e5e341bb721eb5bf88a64
cd target
java -jar nmf-0.1.jar -m json -p coap -i ../testdata/coap_bytes.json -o ../../ttcn3_execution/fuzzing-integration/fuzzdata/coap.txt
```