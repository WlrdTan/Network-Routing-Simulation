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

![4](https://github.com/user-attachments/assets/9b4d43fd-6861-4f03-95e3-d684476d47ec)


It produces files

![1](https://github.com/user-attachments/assets/2033b3e5-7737-4b50-b7b5-954f1a2e3169)

The output of SPF_A
Steps	Destination	Cost	Path

![2](https://github.com/user-attachments/assets/0066ffd6-c835-47c8-a80c-82b309dfce81)


AND output of DVA-A.txt being 


![3](https://github.com/user-attachments/assets/a9f1fe62-d831-4d0c-b73c-bc0d983b3f9f)


