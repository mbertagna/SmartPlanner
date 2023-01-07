from Task import Task, datetime
from re import search

class Schedule:
    """A simple schedule with a name and 
    list of tasks.
    """

    def __init__(self, name, tasks) -> None:
        """The instantiation method for Schedule.

        Parameters
        ----------
        name : str
            The name of the schedule.
        tasks : list
            The list of Task objects associated with the schedule.
        """
        self.m_name = name
        self.m_tasks = tasks

    def add_task(self):
        name = input("NAME: ")

        est_completion_time = input("ESTIMATED TIME TO COMPLETE: ")
        while not (type(est_completion_time) in [float, int] and float(est_completion_time) > 0): 
            print("TYPE ERROR: PLEASE INPUT A POSITIVE DECIMAL VALUE.")
            est_completion_time = input("ESTIMATED TIME TO COMPLETE: ")
        est_completion_time = float(est_completion_time)

        due_date_str = input("DUE DATE (E.G., 1999-07-22 14:34): ")
        while not search("^\d{4}-\d{2}-\d{2}\h\d{2}:\d{2}$", due_date_str):
            print("FORMAT ERROR: PLEASE INPUT A CORRECTLY FORMATTED DUE DATE.")
            due_date_str = input("DUE DATE (E.G., 1999-07-22 14:34): ")
        due_date = datetime.fromisoformat(due_date_str)
        
        new_task = Task(name, est_completion_time, due_date)

        self.m_tasks.append(new_task)