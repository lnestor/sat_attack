#!/bin/bash

# Runs all benchmark 32 key input files for timing

echo -e "\n------------- c1355 -------------\n"
python3 sat_attack/run.py benchmarks/c1355/c1355-RN320/c1355-RN320.v benchmarks/c1355/c1355-oracle.v -t 600 -d
echo -e "------------- c1908 -------------\n"
python3 sat_attack/run.py benchmarks/c1908/c1908-RN320/c1908-RN320.v benchmarks/c1908/c1908-oracle.v -t 600 -d
echo -e "------------- c2670 -------------\n"
python3 sat_attack/run.py benchmarks/c2670/c2670-RN320/c2670-RN320.v benchmarks/c2670/c2670-oracle.v -t 600 -d
echo -e "------------- c3540 -------------\n"
python3 sat_attack/run.py benchmarks/c3540/c3540-RN320/c3540-RN320.v benchmarks/c3540/c3540-oracle.v -t 600 -d
echo -e "------------- c432 -------------\n"
python3 sat_attack/run.py benchmarks/c432/c432-RN320/c432-RN320.v benchmarks/c432/c432-oracle.v -t 600 -d
echo -e "------------- c499 -------------\n"
python3 sat_attack/run.py benchmarks/c499/c499-RN320/c499-RN320.v benchmarks/c499/c499-oracle.v -t 600 -d
echo -e "------------- c5315 -------------\n"
python3 sat_attack/run.py benchmarks/c5315/c5315-RN320/c5315-RN320.v benchmarks/c5315/c5315-oracle.v -t 600 -d
echo -e "------------- c6288 -------------\n"
# python3 sat_attack/run.py benchmarks/c6288/c6288-RN320/c6288-RN320.v benchmarks/c6288/c6288-oracle.v -t 600 -d
echo -e "------------- c7552 -------------\n"
python3 sat_attack/run.py benchmarks/c7552/c7552-RN320/c7552-RN320.v benchmarks/c7552/c7552-oracle.v -t 600 -d

