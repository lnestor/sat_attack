
c1355-NR1550
_______________________________________

DESCRIPTION:
Original Circuit: ISCAS85 benchmark c1355 [1]
Number of Gates: 747
Number of Input: 196( 41 original inputs, 155 key ports)
Number of Output: 32
Key size = 155
          (32 keys to obfuscate original circuit,
           82 key AntiSAT block,
           41 keys to obfuscate AntiSAT block)
Key input naming: 'keyinput[input number]'
Synthesis Library: SAED90nm_typ Library (version 2013)


OBFUSCATION TECHNIQUE(S) IMPLEMENTED:
Obfuscation method: Random key gate insertion
SAT-Attack defense: AntiSAT [3]


TAXONOMY:
Obfuscation Method: Combinational -> Combinational Hybrid -> SAT Defense -> AntiSAT -> Random
Physical Characteristics -> Obfuscated Netlist Size -> #gates<1000
                            Key Size -> Other


CONTACT:
          Sarah Amir
          Florida Institute of Cyber Security (FICS)
          University of Florida
          sarah.amir@ufl.edu, prema_buet@gmail.com


REFERENCES:
[1] ISCAS85 benchmarks http://www.pld.ttu.ee/~maksim/benchmarks/iscas85/verilog/
[3]	Xie, Yang, and Ankur Srivastava. "Mitigating sat attack on logic locking." International Conference on Cryptographic Hardware and Embedded Systems. Springer Berlin Heidelberg, 2016.
