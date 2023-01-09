from Schedule import Schedule, Task, datetime
from datetime import date, timedelta
from util import insertionSort
import os

class Planner:
    """A simple planner with a name which is 
    comprised of multiple schedules.
    """

    def __init__(self, name) -> None:
        """The instantiation method for Planner.

        Parameters
        ----------
        name : str
            The name of the Planner.
        schedules : list
            The list of Schedule objects associated with the planner.
        """
        self.m_name = name
        self.m_schedules = []

    def create_plan(self, include_today, hours_per_date=8.0):
        todays_date = date.today()

        end_note = "\n\n***NOTE***\n\n" # create store for notes to user about exceptions to schedule

        # set first plan day
        if include_today:
            first_day = todays_date
        else:
            first_day = todays_date + timedelta(days=1)
        
        # create list of all tasks sorted in ascending order by due datetime
        all_tasks_list = []
        for schedule in self.m_schedules:
            for task in schedule.m_tasks:
                if task.get_est_completion_time() >= 0.5:
                    all_tasks_list.append(task)
                else:
                    end_note += "THE TASK \"" + task.get_name() + "\" WAS REMOVED AS IT IS QUICK ENOUGH TO BE DONE NOW RATHER THAN LATER. DO IT IMMEDIATELY!!!.\n\n"

        all_tasks_list.sort()

        start_day = first_day # set day to start alloting hours (keeps track of last open day)

        curr_date = start_day # set curr date to start iterating over

        latest_due_date = all_tasks_list[len(all_tasks_list)-1].m_due_date.date() # set latest due date in set of tasks (sentinal value)

        # create plan dictionary
        plan_dict = {} # structure: {date1 : [[hours_remaining], [task1, numHours, dueDate], [task2, numHours]], date2 : [[hours_remaining], [task2, numHours]]}
        while curr_date < latest_due_date:
            plan_dict[curr_date] = [[hours_per_date]]
            curr_date = curr_date + timedelta(days=1)

        # plan formulation loop
        while len(all_tasks_list) > 0:
            # clear/declare the lists which stores popped tasks and popped tasks hours per day (hpd)
            popped_tasks = []
            popped_tasks_hpd = []
            # pop a task off the front of the list
            popped_tasks.append(all_tasks_list.pop(0))
            # continue popping while the due date is the same
                # store the first due date popped and pop next if due date same (make sure to cast to date)
            due_date_popped = popped_tasks[0].get_due_date().date()
            while len(all_tasks_list) > 0 and all_tasks_list[0].get_due_date().date() == due_date_popped:
                popped_tasks.append(all_tasks_list.pop(0))
            # compute total time required to complete tasks (separate function) and total time before date (separate function)
            # if total time required to complete tasks is > total time before date, spread the hours out over remaining days before due date
            if self.total_completion_time(popped_tasks) > self.total_time_before_due(due_date_popped, start_day, plan_dict):
                # compute hours per day for each task
                popped_tasks_hpd = self.hours_per_day(popped_tasks, due_date_popped, start_day)
                # loop through each day and assign hours
                    # ensure that each day is checked to see if remaining hours > 0 to set new start day
                curr_date = start_day
                while curr_date < due_date_popped:
                    # loop through all popped tasks
                    for idx in range(len(popped_tasks)):
                        # if last one, add due datetime to list
                        if curr_date == due_date_popped - timedelta(days=1): # if last day to work on task, add due date to list
                            plan_dict[curr_date] = plan_dict[curr_date] + [[popped_tasks[idx].get_name(), "{:.2f}".format(popped_tasks_hpd[idx]), (popped_tasks[idx].get_due_date()).strftime("%m-%d-%Y at %H:%M")]]
                            # add to user note
                            end_note += "THE TASK \"" + popped_tasks[idx].get_name() + "\" CANNOT BE COMPLETED WITHOUT WORKING OVERTIME. CONSIDER WORKING FASTER OR SACRIFICING SLEEP.\n\n"
                        # else, add task+hours to plan dictionary day
                        else:
                            plan_dict[curr_date] = plan_dict[curr_date] + [[popped_tasks[idx].get_name(), "{:.2f}".format(popped_tasks_hpd[idx])]]
                    # modify hours in plan dictionary day based on added hours
                    plan_dict[curr_date][0][0] = plan_dict[curr_date][0][0] - sum(popped_tasks_hpd)
                    # if hours on day are <= 0.0, increment the start day
                    if plan_dict[curr_date][0][0] <= 0.0:
                        start_day = curr_date + timedelta(days=1)
                    # increment current day
                    curr_date = curr_date + timedelta(days=1)
            # else compute the hours per day for each task
            else:
                popped_tasks_hpd = self.hours_per_day(popped_tasks, due_date_popped, start_day)
                # loop through each day
                curr_date = start_day
                while curr_date < due_date_popped:
                    # if available hours in given day > sum of daily hours to be assigned for tasks, assign hours to day
                    if plan_dict[curr_date][0][0] >= sum(popped_tasks_hpd):
                        # loop through all popped tasks
                        for idx in range(len(popped_tasks)):
                            # if last one, add due datetime to list
                            if curr_date == due_date_popped - timedelta(days=1): # if last day to work on task, add due date to list
                                plan_dict[curr_date] = plan_dict[curr_date] + [[popped_tasks[idx].get_name(), "{:.2f}".format(popped_tasks_hpd[idx]), (popped_tasks[idx].get_due_date()).strftime("%m-%d-%Y at %H:%M")]]
                            # else, add task+hours to plan dictionary day
                            else:
                                plan_dict[curr_date] = plan_dict[curr_date] + [[popped_tasks[idx].get_name(), "{:.2f}".format(popped_tasks_hpd[idx])]]
                        # modify hours in plan dictionary day based on added hours
                        plan_dict[curr_date][0][0] = plan_dict[curr_date][0][0] - sum(popped_tasks_hpd)
                    # else available hours in given day < sum of hours to be assigned for tasks
                    else:
                        # determine task with max est. hours to complete
                        max_time_task_index = popped_tasks_hpd.index(max(popped_tasks_hpd))
                        # calculate available hours on day and allot this amount of time to that task on day
                        available_hours = plan_dict[curr_date][0][0]
                        # see how many hours left for task
                        task_hours_left = popped_tasks[max_time_task_index].get_est_completion_time()
                        # compute difference of hours left and available hours
                        hours_difference = task_hours_left - available_hours
                        # if the number of hours left for the task is greater than or equal to the the available hours, allot the available hours
                        if hours_difference >= 0:
                            hours_to_add = available_hours
                            plan_dict[curr_date] = plan_dict[curr_date] + [[popped_tasks[max_time_task_index].get_name(), "{:.2f}".format(hours_to_add)]]
                            # substract hours from task est. hours to complete
                            popped_tasks[max_time_task_index].set_est_completion_time(popped_tasks[max_time_task_index].get_est_completion_time() - hours_to_add)
                        # else, add task hours remaining
                        else:
                            hours_to_add = task_hours_left
                            plan_dict[curr_date] = plan_dict[curr_date] + [[popped_tasks[max_time_task_index].get_name(), "{:.2f}".format(hours_to_add)]]
                            # remove task from popped list
                            popped_tasks.pop(max_time_task_index)
                            
                        # set new start day (must be done before start day is incremented and hours per day for each task recalculated)
                        plan_dict[curr_date][0][0] = plan_dict[curr_date][0][0] - hours_to_add
                        # if hours on day are <= 0.0, increment the start day
                        if plan_dict[curr_date][0][0] <= 0.0:
                            start_day = curr_date + timedelta(days=1)

                        # recalculate hours per day for each task
                        popped_tasks_hpd = self.hours_per_day(popped_tasks, due_date_popped, start_day)


                    # if hours on day are <= 0.0, increment the start day
                    if plan_dict[curr_date][0][0] <= 0.0:
                        start_day = curr_date + timedelta(days=1)
                    # increment current day
                    curr_date = curr_date + timedelta(days=1)

        self.write_plan_from_dict(plan_dict, first_day, latest_due_date, end_note)
        
    def total_completion_time(self, list_of_tasks):
        total_time = 0.0
        for task in list_of_tasks:
            total_time += task.get_est_completion_time()
        return total_time

    def total_time_before_due(self, due_date, start_day, plan_dict):
        total_time = 0.0
        curr_day = start_day
        while curr_day < due_date:
            total_time += plan_dict[curr_day][0][0]
            curr_day = curr_day + timedelta(days=1)
        return total_time

    def hours_per_day(self, tasks, due_date, start_day):
        tasks_hpd = []
        days_to_complete = (due_date - start_day).days
        for task in tasks:
            tasks_hpd.append(task.get_est_completion_time()/days_to_complete)
        return tasks_hpd

    def write_plan_from_dict(self, plan_dict, first_day, last_day, end_note):
        curr_day = first_day
        with open('plan.txt', 'w') as f:
            while curr_day < last_day:
                curr_day_list = plan_dict[curr_day]

                curr_day_str = curr_day.strftime("%m-%d-%Y")

                f.write(curr_day_str + "\n")

                for list in curr_day_list:
                    if len(list) == 2:
                        f.write("\t" + list[1] + " hours-" + list[0] + "\n")
                    elif len(list) == 3:
                        f.write("\t" + list[1] + " hours-" + list[0] + "-due " + list[2] + "\n")

                curr_day = curr_day + timedelta(days=1)

            if end_note != "\n\n***NOTE***\n\n":
                f.write(end_note)


    def read_schedules(self, include_today) -> bool:
        """Opens and reads each file in the local "schedules" 
        folder and populates the schedules in the planner.
        """
        all_task_names = set()

        todays_date = date.today()

        if include_today:
            first_day = todays_date
        else:
            first_day = todays_date + timedelta(days=1)

        for filename in os.listdir(os.getcwd()+"/schedules"):
            with open(os.path.join(os.getcwd()+"/schedules", filename), 'r') as f:
                
                try:
                    lines = f.readlines()

                    sname = lines.pop(0).strip()
                    stasks = []

                    lines.pop(0)
                    lines.pop(0)
            
                    while len(lines) > 0:
                        tname = lines.pop(0).strip()
                        test_completion_time= lines.pop(0).strip()
                        tdue_date_str = lines.pop(0).strip()
                        lines.pop(0)
                        
                        if datetime.fromisoformat(tdue_date_str).date() <= first_day:
                            error_string = "\n***TASK DATE ERROR***\nALL TASKS MUST HAVE BE DUE AFTER THE FIRST DAY OF WORK.\n"
                            error_string += "THE TASK \"" + tname + "\" HAS AN INVALID DUE DATE.\n"
                            print(error_string)
                            return False

                        new_task = Task(tname, float(test_completion_time), datetime.fromisoformat(tdue_date_str))

                        if tname in all_task_names:
                            error_string = "\n***TASK NAME ERROR***\nALL TASKS MUST HAVE UNIQUE NAMES.\n"
                            error_string += "THE NAME \"" + tname + "\" APPEARED MORE THAN ONCE AMOUNGST THE INPUTTED SCHEDULES.\n"
                            print(error_string)
                            return False
                        else:
                            all_task_names.add(tname)

                        stasks.append(new_task)
                        stasks = insertionSort(stasks)

                    self.m_schedules.append(Schedule(sname, stasks))

                except(ValueError, IndexError):
                    error_string = """
***FILE FORMAT ERROR***
PLEASE USE THE FOLLOWING FORMAT FOR ALL FILES:
SCHEDULE TITLE
<newline>
<newline>
TASK NAME
ESTIMATED AMOUNT OF TIME TO COMPLETE TASK IN DECIMAL FORM
DUE DATE AND TIME IN FORMAT: YEAR-MONTH-DAY HOUR:MINUTE (e.g. 1999-07-22 15:05)
<newline>
                    """
                    print(error_string)
                    return False

        if len(all_task_names) == 0:
            print("\n***NO INPUT FILES FOUND***\nPLEASE MOVE ALL SCHEDULE FILES IN THE LOCAL \"schedules\" DIRECTORY.\n")
            return False

        return True


