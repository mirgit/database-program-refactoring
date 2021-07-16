# database-program-refactoring

This project is an effort to implement the 2019 paper of Wang et al. for migrating database programs after schema refactoring. you can find the paper in https://dl.acm.org/doi/10.1145/3314221.3314588

 The method introduced in this paper receives a database program P which is compatible with schema S. It also receives a new schema S' as the target schema and automatically generates a program P' such that P and P' produce the same result on the same input.


to run the project and examinate benchmarks, run the synthsizer.py 

the output for each benchmark is the target program, which you can find in /path/to/the/benchmark/tgt-prog.txt
