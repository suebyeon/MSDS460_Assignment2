# MSDS460_Assignment2 - Network Models -- Project Management
This repository contains the implementation of a linear programming (LP) model to solve a 15 steps software developement project management problem and finding the critical path analysis, designed for MSDS 460: Decision Analytics. The project aims to minimize the time taken to complete each tasks. 

### Includes:
- assignment2paper.pdf
- assignment2.py
- output2.txt
- project-plan-v003.csv
- Chatgpt_log.txt

### assignment2paper.pdf
Discusses the method of setting up the problem and any uncertainities from it and also discusses the result of the formulated problem to find the critical path for best-cse, expected, and worst-cse scenarios. 

### assignment2.py
Includes Python code of the linear programming formulation with decision variables, objective function, and constraints of the problem and identifies the critical path and creates Gantt charts.

### output2.txt
Includes the output of the problem which shows the optimal solution found through PuLP.

### project-plan-v003.csv
Includes a list of tasks for this project plan with their immediate predecessors, number of hours to complete a task for best-case, expected, and worst-case, and number of contributors for each type of role.

## GenAI Tools
I used ChatGPT to help generate estimates of duration of each tasks for the 3 cases, the generalized hourly rate for the workers, and assignment for number of workers for each role. Chatgpt_log.txt includes prompts I used and respnses I got to complete these 3 parameters. 
