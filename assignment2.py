import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value

# Define tasks with (best-case, expected, worst-case) durations
tasks = {
    "DescribeProduct": (8,12,20),
    "DevelopMarketingStrategy": (12,18,30),
    "DesignBrochure": (10,15,25),
    "RequirementsAnalysis": (16,24,40),
    "SoftwareDesign": (20,30,50),
    "SystemDesign": (20,30,50),
    "Coding": (40,60,100),
    "WriteDocumentation": (12,18,30),
    "UnitTesting": (16,24,40),
    "SystemTesting": (24,36,60),
    "PackageDeliverables": (10,15,25),
    "SurveyPotentialMarket": (16,24,40),
    "DevelopPricingPlan": (12,18,30),
    "DevelopImplementationPlan": (20,30,50),
    "WriteClientProposal": (10,15,25),
}

# Create a list of the activities
tasks_list = list(tasks.keys())

# Task dependencies (task B cannot start until task A is completed)
dependencies = {
    "DescribeProduct": [],
    "DevelopMarketingStrategy": [],
    "DesignBrochure": ["DescribeProduct"],
    "RequirementsAnalysis": ["DescribeProduct"],
    "SoftwareDesign": ["RequirementsAnalysis"],
    "SystemDesign": ["RequirementsAnalysis"],
    "Coding": ["SoftwareDesign", "SystemDesign"],
    "WriteDocumentation": ["Coding"],
    "UnitTesting": ["Coding"],
    "SystemTesting": ["UnitTesting"],
    "PackageDeliverables": ["WriteDocumentation", "SystemTesting"],
    "SurveyPotentialMarket": ["DevelopMarketingStrategy", "DesignBrochure"],
    "DevelopPricingPlan": ["PackageDeliverables", "SurveyPotentialMarket"],
    "DevelopImplementationPlan": ["DescribeProduct", "PackageDeliverables"],
    "WriteClientProposal": ["DevelopPricingPlan", "DevelopImplementationPlan"]
}

# Function to solve for best-case, expected, or worst-case durations
def solve_project_schedule(time_type):
    model = LpProblem("Project_Scheduling", LpMinimize)
    durations = {task: tasks[task][time_type] for task in tasks}

    # Define decision variables
    start_times = {task: LpVariable(f"Start_{task}", 0, None) for task in tasks_list}
    end_times = {task: LpVariable(f"End_{task}", 0, None) for task in tasks_list}
    
    # Objective: Minimize project time
    model += lpSum([end_times[task] for task in tasks_list]), "minimize_end_times"

    # Constraints: Task dependencies
    for task in tasks_list:
        model += end_times[task] == start_times[task] + durations[task], f"{task}_duration"
        for predecessor in dependencies[task]:
            model += start_times[task] >= end_times[predecessor], f"{task}_predecessor_{predecessor}"


    # Solve the LP model
    status = model.solve()

    # Extract results
    schedule_start = {task: value(start_times[task]) for task in tasks }
    schedule_end = {task: value(end_times[task]) for task in tasks }
    var_val = model.variables()

    return schedule_start, schedule_end, var_val

# Solve for each scenario
best_case_schedule_start, best_case_schedule_end, best_var_val = solve_project_schedule(0)

expected_case_schedule_start, expected_case_schedule_end, expected_var_val = solve_project_schedule(1)
worst_case_schedule_start, worst_case_schedule_end, worst_var_val = solve_project_schedule(2)

with open("output2.txt", "w") as f:
    # Print the results
    print("-----------------------------", file=f)
    print("Critical Path time for Best-case:", file=f)
    for task in tasks_list:
        if value(best_case_schedule_start[task]) == 0:
            print(f"{task} starts at time 0", file=f)
        if value(best_case_schedule_end[task]) == max([value(best_case_schedule_end[task]) for task in tasks_list]):
            print(f"{task} ends at {value(best_case_schedule_end[task])} hours in duration", file=f)

    # Print solution
    print("\nSolution variable values for Best-case:", file=f)
    for var in best_var_val:
        if var.name != "_dummy":
            print(var.name, "=", var.varValue, file=f)

    print("-----------------------------", file=f)
    print("Critical Path time for expected case:", file=f)
    for task in tasks_list:
        if value(expected_case_schedule_start[task]) == 0:
            print(f"{task} starts at time 0", file=f)
        if value(expected_case_schedule_end[task]) == max([value(expected_case_schedule_end[task]) for task in tasks_list]):
            print(f"{task} ends at {value(expected_case_schedule_end[task])} hours in duration", file=f)

    # Print solution
    print("\nSolution variable values for expected case:", file=f)
    for var in expected_var_val:
        if var.name != "_dummy":
            print(var.name, "=", var.varValue, file=f)

    print("-----------------------------", file=f)
    print("Critical Path time for worst case:", file=f)
    for task in tasks_list:
        if value(worst_case_schedule_start[task]) == 0:
            print(f"{task} starts at time 0", file=f)
        if value(worst_case_schedule_end[task]) == max([value(worst_case_schedule_end[task]) for task in tasks_list]):
            print(f"{task} ends at {value(worst_case_schedule_end[task])} hours in duration", file=f)

    # Print solution
    print("\nSolution variable values for worst case:", file=f)
    for var in worst_var_val:
        if var.name != "_dummy":
            print(var.name, "=", var.varValue, file=f)


    # Identify Critical Path
    def find_critical_path(schedule, durations):
        G = nx.DiGraph()
        for task in tasks:
            G.add_node(task, duration=durations[task])

        for task, predecessors in dependencies.items():
            for predecessor in predecessors:
                G.add_edge(predecessor, task, weight=durations[predecessor])

        # Compute longest path (Critical Path)
        critical_path = nx.dag_longest_path(G, weight="weight")
        critical_path_duration = sum(durations[task] for task in critical_path)

        return critical_path, critical_path_duration

    best_case_cp, best_case_cp_duration = find_critical_path(best_case_schedule_start, {task: tasks[task][0] for task in tasks})
    expected_case_cp, expected_case_cp_duration = find_critical_path(expected_case_schedule_start, {task: tasks[task][1] for task in tasks})
    worst_case_cp, worst_case_cp_duration = find_critical_path(worst_case_schedule_start, {task: tasks[task][2] for task in tasks})

    print(f"Critical Path (Best Case): {best_case_cp} - Duration: {best_case_cp_duration}", file=f)
    print(f"Critical Path (Expected Case): {expected_case_cp} - Duration: {expected_case_cp_duration}", file=f)
    print(f"Critical Path (Worst Case): {worst_case_cp} - Duration: {worst_case_cp_duration}", file=f)

    print(f"", file=f)
f.close()

# # Generate Gantt Chart
# def plot_gantt_chart(schedule, durations, title):
#     plt.figure(figsize=(10, 5))
#     for i, (task, start_time) in enumerate(schedule.items()):
#         plt.barh(task, durations[task], left=start_time, color="skyblue")
#     plt.xlabel("Time (Hours)")
#     plt.ylabel("Tasks")
#     plt.title(title)
#     plt.grid(axis="x")
#     plt.show()

# # Generate Gantt Charts
# plot_gantt_chart(best_case_schedule_start, {task: tasks[task][0] for task in tasks}, "Best-Case Gantt Chart")
# plot_gantt_chart(expected_case_schedule_start, {task: tasks[task][1] for task in tasks}, "Expected-Case Gantt Chart")
# plot_gantt_chart(worst_case_schedule_start, {task: tasks[task][2] for task in tasks}, "Worst-Case Gantt Chart")
