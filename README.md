# atpg-podem

Improved and modular ATPG using PODEM algorithm

EL5201-01 Digital System Testing and Testable Design | Institute of Technology Bandung

The project folder contains the following:

1. Document
	Problem Statement
	Assumptions
	I/O description
	Algorithm[1][3]
	Worked out example[5]

2. Code and Demo
	Matlab code- podem.m
	Python code- podem.py
	netlist.txt
	netlist2.txt
	netlist3.txt
	netlist4.txt

How to get started:

1. The folder contains multiple netlist files representing different circutis. It is a spice netlist of nodes of the circuit.

2.Go to the “podem.m” file and type in values for the variables “FaultLocation” and “FaultValue” where 
   FaultLocation is the node where fault is to be checked ,values should be taken from the netlist file 
   e.g. n1,n4. FaultValue is the complementary value of the stuck at fault.

3. Run for different combination of Fault Location and Fault Value.

References:

1.Sachin Dhingra : Implementation of ATPG Using PODEM Algorithm
2. Inbuilt MATLAB help
3. Logic Synthesis and Verification Algorithms - Gary Hachtel and Fabio Somenzi
4. tutorialspoint.com   (Python reference)
5. One example of PODEM implementation: ecs.csun.edu/rroosta/documents/podem.pdf
