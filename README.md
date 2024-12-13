# Network-Routing-Simulation
Python simulation model using distance vector routing and shortest path first (SPF) algorithms for dynamic network routing.

Requirements : 
1. Python Environment
Ensure Python 3.x is  installed on your system. This script makes use of Python 3 features like dictionary comprehensions and modern standard libraries.
2. Required Python Modules
    • The code uses the following modules from the Python standard library:
        ◦ heapq
        ◦ os
        ◦ copy
        ◦ defaultdict from collections
        ◦ No additional third-party libraries are required.
3. Input File
    • File Name: By default, the code expects a file named topology.txt in the same directory as the script.
    • File Format:
        ◦ Each line should follow the format:
time: u, v, cost
        ◦ Example:
0: A, B, 4
1: A, C, 2
        ◦ Lines that don't conform to this format are skipped with a warning.
        ◦ Time 0 represents the initial graph, and other times represent changes.
    • The file that Has S at the end of the name accepts standard inputs with no spaces such as
    •           0:A,B,4
          1:A,C,2
4. File Write Permissions
    • The script writes output files based on the input file name (SPF and DVA files for each node). Ensure the script has write permissions in the directory where it is executed.

The programme uses graph based updates when network changes occur and calculates the optimal routing paths based on the new graph.
The programme also stops executing when the shortest path remains the same for 5 iterations or if the no of iterations reach 100 (This is to make sure that the programme isnt infinitly recursive)

For example for an input topology-1
0:A,B,4
0:A,C,6
0:B,C,1
0:C,D,8
0:C,E,4
0:D,E,10
0:D,F,15
0:B,D,5
0:E,G,2
0:E,G,2
0:F,G,6
6:E,D,5
6:B,C,4

It produces files

![1](https://github.com/user-attachments/assets/2033b3e5-7737-4b50-b7b5-954f1a2e3169)

The output of SPF_A
Steps	Destination	Cost	Path
0	A	0	A
0	B	4	A -> B
0	C	5	A -> B -> C
0	D	9	A -> B -> D
0	E	9	A -> B -> C -> E
0	F	17	A -> B -> C -> E -> G -> F
0	G	11	A -> B -> C -> E -> G
6	A	0	A  (Here the programme accounts for changes in topology and updates the shortest path based on it)
6	B	4	A -> B
6	C	6	A -> C
6	D	9	A -> B -> D
6	E	10	A -> C -> E
6	F	18	A -> C -> E -> G -> F
6	G	12	A -> C -> E -> G


AND output of DVA-A.txt being 

TimeStep	Step	Destination	NextHop	Cost
0	1	A	-	0
0	1	B	B	4
0	1	C	C	6
0	1	D	B	inf
0	1	E	C	inf
0	1	F	C	inf
0	1	G	C	inf
0	2	A	-	0
0	2	B	B	4
0	2	C	C	5
0	2	D	B	9
0	2	E	C	10
0	2	F	C	inf
0	2	G	C	inf
0	3	A	-	0
0	3	B	B	4
0	3	C	C	5
0	3	D	B	9
0	3	E	C	9
0	3	F	C	24
0	3	G	C	12
0	4	A	-	0
0	4	B	B	4
0	4	C	C	5
0	4	D	B	9
0	4	E	C	9
0	4	F	C	18
0	4	G	C	11
0	5	A	-	0
0	5	B	B	4
0	5	C	C	5
0	5	D	B	9
0	5	E	C	9
0	5	F	C	17
0	5	G	C	11
0	6	A	-	0
0	6	B	B	4
0	6	C	C	5
0	6	D	B	9
0	6	E	C	9
0	6	F	C	17
0	6	G	C	11
0	7	A	-	0
0	7	B	B	4
0	7	C	C	5
0	7	D	B	9
0	7	E	C	9
0	7	F	C	17
0	7	G	C	11
0	8	A	-	0
0	8	B	B	4
0	8	C	C	5
0	8	D	B	9
0	8	E	C	9
0	8	F	C	17
0	8	G	C	11
0	9	A	-	0
0	9	B	B	4
0	9	C	C	5
0	9	D	B	9
0	9	E	C	9
0	9	F	C	17
0	9	G	C	11 (Stops after the pathe reamains the same for 5 iterations and moves on to the next graph which is created based on the changes to previous topology graph)
6	10	A	-	0
6	10	B	B	4
6	10	C	C	6
6	10	D	B	inf
6	10	E	C	inf
6	10	F	C	inf
6	10	G	C	inf
6	11	A	-	0
6	11	B	B	4
6	11	C	C	6
6	11	D	B	9
6	11	E	C	10
6	11	F	C	inf
6	11	G	C	inf
6	12	A	-	0
6	12	B	B	4
6	12	C	C	6
6	12	D	B	9
6	12	E	C	10
6	12	F	C	24
6	12	G	C	12
6	13	A	-	0
6	13	B	B	4
6	13	C	C	6
6	13	D	B	9
6	13	E	C	10
6	13	F	C	18
6	13	G	C	12
6	14	A	-	0
6	14	B	B	4
6	14	C	C	6
6	14	D	B	9
6	14	E	C	10
6	14	F	C	18
6	14	G	C	12
6	15	A	-	0
6	15	B	B	4
6	15	C	C	6
6	15	D	B	9
6	15	E	C	10
6	15	F	C	18
6	15	G	C	12
6	16	A	-	0
6	16	B	B	4
6	16	C	C	6
6	16	D	B	9
6	16	E	C	10
6	16	F	C	18
6	16	G	C	12
6	17	A	-	0
6	17	B	B	4
6	17	C	C	6
6	17	D	B	9
6	17	E	C	10
6	17	F	C	18
6	17	G	C	12


