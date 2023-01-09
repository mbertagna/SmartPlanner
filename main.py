from Planner import Planner

p = Planner("Michael's Planner")

include_today = True

read_success = p.read_schedules(True)

if read_success:
    p.create_plan(True)