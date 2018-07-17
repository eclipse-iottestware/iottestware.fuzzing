# iottestware.fuzzing
Contains two pieces. First, the generator compiles a set of fuzzdata (test cases) using a network dump. Second, there is a ttcn3 project that's utilizing the generated dataset and makes the fuzzdata available as octetstrings for further sending.
## Agenda ##
- [ ] on-the-fly fuzz data generation
- [ ] control generation via ttcn3 functions
- [ ] filter doublets in data
- [ ] generate data for more types of fields