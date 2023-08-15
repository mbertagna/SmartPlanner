[![Demos](https://colab.research.google.com/assets/colab-badge.svg)](https://drive.google.com/drive/folders/1cqswaQJGbJOl_Nq6G_xX4XubCg4tdbF-?usp=sharing)


# SmartPlanner
A dynamic scheduler application which can curate and save multiple schedules in one planner.
Simply create a subdirectory named "schedules" and add one or more text files (with a ".txt" extension) to it with any amount of tasks using the following format:
```
SCHEDULE TITLE
<newline>
<newline>
TASK NAME
ESTIMATED AMOUNT OF TIME IN HOURS TO COMPLETE TASK IN DECIMAL FORM (e.g. 6.5)
DUE DATE AND TIME IN FORMAT: YEAR-MONTH-DAY HOUR:MINUTE (e.g. 1999-07-22 15:05)
<newline>
TASK NAME
ESTIMATED AMOUNT OF TIME IN HOURS TO COMPLETE TASK IN DECIMAL FORM (e.g. 6.5)
DUE DATE AND TIME IN FORMAT: YEAR-MONTH-DAY HOUR:MINUTE (e.g. 1999-07-22 15:05)
<newline>
```
Then, run the main.py script via the command line (python3 main.py). A file named "plan.txt" will be created in the current directory containing a curated day-to-day plan!
