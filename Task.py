from datetime import datetime

class Task:
    """A simple task with a name, estimated 
    time to complete, and due date/time.
    """

    def __init__(self, name, est_completion_time, due_date) -> None:
        """The instantiation method for Task.

        Parameters
        ----------
        name : str
            The task itself.
        est_completion_time : float
            The estimated amount of time in hours 
            required to complete the task.
        due_date : datetime
            The due date and time of the task.
        """
        self.m_name = name
        self.m_est_completion_time = est_completion_time
        self.m_due_date = due_date

    def get_name(self):
        return self.m_name

    def get_est_completion_time(self):
        return self.m_est_completion_time

    def get_due_date(self):
        return self.m_due_date

    def set_est_completion_time(self, est_completion_time):
        self.m_est_completion_time = est_completion_time

    def __eq__(self, other_task) -> bool:
        return self.m_due_date == other_task.m_due_date
        
    def __le__(self, other_task) -> bool:
        return self.m_due_date <= other_task.m_due_date

    def __ge__(self, other_task) -> bool:
        return self.m_due_date >= other_task.m_due_date

    def __lt__(self, other_task) -> bool:
        return self.m_due_date < other_task.m_due_date

    def __gt__(self, other_task) -> bool:
        return self.m_due_date > other_task.m_due_date

    def __ne__(self, other_task) -> bool:
        return self.m_due_date != other_task.m_due_date

