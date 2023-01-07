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

    def create_plan(self, include_today=True, hours_per_day=6.0):
        first_day = date.today()

        if not include_today:
            first_day = first_day + timedelta(days=1)

        plan_dict = {} # structure: {date1 : [[hours_remaining], [task1, numHours], [task2, numHours]], date2 : [[hours_remaining], [task1, numHours], [task2, numHours]]}

        end_note = "\n\n\n\n***NOTE***\n\n"
        
        all_tasks_list = []

        for schedule in self.m_schedules:
            for task in schedule.m_tasks:
                all_tasks_list.append(task)

        all_tasks_list.sort()

        start_day = first_day
        curr_date = start_day
        latest_due_date = all_tasks_list[len(all_tasks_list)-1].m_due_date.date()

        while curr_date < latest_due_date:
            plan_dict[curr_date] = [[hours_per_day]]
            curr_date = curr_date + timedelta(days=1)

        for task in all_tasks_list:
            tname = task.m_name
            test_completion_time = task.m_est_completion_time
            tdue_date = task.m_due_date.date()

            tdays_to_complete = (tdue_date - start_day).days
            thours_per_day = test_completion_time/tdays_to_complete

            tcurr_day = start_day
            ttotal_hours = 0.0
            while tcurr_day < tdue_date:
                ttotal_hours += plan_dict[tcurr_day][0][0]
                tcurr_day = tcurr_day + timedelta(days=1)

            if test_completion_time > ttotal_hours:
                end_note += "THE TASK \"" + tname + "\" CANNOT BE COMPLETED WITHOUT WORKING OVERTIME EACH DAY. CONSIDER WORKING FASTER OR NOT SLEEPING.\n\n"

                print(tcurr_day, tdue_date)

                while tcurr_day < tdue_date:
                    print("RAN")
                    plan_dict[tcurr_day][0][0] = 0.0
                    plan_dict[tcurr_day] = plan_dict[tcurr_day] + [[tname, thours_per_day]]
                    tcurr_day = tcurr_day + timedelta(days=1)
                
            else:
                tcurr_day = start_day

                while tcurr_day < tdue_date:

                    if plan_dict[tcurr_day][0][0] < thours_per_day:
                        plan_dict[tcurr_day] = plan_dict[tcurr_day] + [[tname, plan_dict[tcurr_day][0][0]]]
                        test_completion_time -= plan_dict[tcurr_day][0][0]
                        plan_dict[tcurr_day][0][0] = 0.0
                        start_day = tcurr_day + timedelta(days=1)
                        tdays_to_complete = (tdue_date - start_day).days
                        thours_per_day = test_completion_time/tdays_to_complete
                        tcurr_day = tcurr_day + timedelta(days=1)
                    else:
                        plan_dict[tcurr_day][0][0] -= thours_per_day
                        plan_dict[tcurr_day] = plan_dict[tcurr_day] + [[tname, thours_per_day]]
                        tcurr_day = tcurr_day + timedelta(days=1)
        
        self.write_plan_from_dict(plan_dict, first_day, latest_due_date, end_note)
        

    def write_plan_from_dict(self, plan_dict, first_day, last_day, end_note):
        curr_day = first_day
        with open('plan.txt', 'w') as f:
            while curr_day < last_day:
                curr_day_list = plan_dict[curr_day]

                curr_day_str = curr_day.strftime("%m-%d-%Y")

                f.write(curr_day_str + "\n")

                for list in curr_day_list:
                    if len(list) > 1:
                        f.write("\t" + "{:.2f}".format(list[1]) + " hours-" + list[0] + "\n")
                
                f.write("\n")

                curr_day = curr_day + timedelta(days=1)

            if end_note != "\n\n\n\n***NOTE***\n\n":
                f.write(end_note)


    def read_schedules(self) -> bool:
        """Opens and reads each file in the local "schedules" 
        folder and populates the schedules in the planner.
        """
        all_task_names = set()

        for filename in os.listdir(os.getcwd()+"/schedules"):
            with open(os.path.join(os.getcwd()+"/schedules", filename), 'r') as f:
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

                    new_task = Task(tname, float(test_completion_time), datetime.fromisoformat(tdue_date_str))

                    all_task_names.add(tname)

                    stasks.append(new_task)
                    stasks = insertionSort(stasks)

                self.m_schedules.append(Schedule(sname, stasks))

        return True


