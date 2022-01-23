### Overview
This is a set of Python scripts written by Nikita Samarin to analyze files generated
from CS 195 assignments. Contact Nikita (nsamarin@berkeley.edu) if you are a TA
in this class and need support.

### How to use this?
The Python source scripts that load and analyze data are located in the utils directory.

The intended way to use these scripts is via Jupyter Notebooks, examples of which
are located in the notebooks directory. These notebooks can import the functions from
the source Python files in the utils directory.

### Scripts Overview
loaders.py includes functions that load data from source files and spreadsheets into
Pandas dataframes that can then be analyzed and visualized in a Jupyter Notebook.
You can either provide the datapath manually or rely on the defaults, taken from
the paths indicated in constants.py
The format of these sources files is described in the next section.

analysis.py takes the Pandas dataframes and analyzes them by e.g., counting the
number of attendances, indicating whether assignments are complete or not, etc.

crowdgrader.py supports the loading of files from the CrowdGrader server, given
the source URLs provided in the JSON file that is downloaded manually from CrowdGrader.

constants.py includes paths to files and some constants, that can be easily changed
without affecting other parts of the code.

helpers.py provides supporting functionality.

### Source Files Overview
Although the source file would differ depending on the exact nature of assignments,
here is an overview of files that should work with the current codebase.

Names refer to constants name in constants.py

* DATA_DIR is the directory containing the source data files. This can be anything,
but it's easiest if you simply create a directory called "data" here. 

* ROSTER_FILE is a CSV file containing at least the following three columns:
('Name', 'Student ID', 'Email Address').

* ATTENDANCE_FILE is a .xlsx files obtained by saving Google form responses for
lecture attendance into a single Google spreadsheet, with each lecture corresponding
to a different sheet in the spreadsheet. You can generate this spreadsheet automatically
from the Google form settings. Once you have the spreadsheet, you can export it into
a single .xlsx file containing all of the sheets.

* SURVEY_FILE is a .xlsx file containing data for pre-lecture survey completion.
You can obtain this file in the same way as the ATTENDANCE_FILE.

* MAKEUP_FILE is a .xlsx file containing data for makeup responses for missed
attendances and pre-lecture surveys. In this codebase, we assume that it's also generated
from Google form responses and, thus, is similar to ATTENDANCE_FILE and SURVEY_FILE.

* ESSAY_X_CROWD_FILE refers to a .json file that you obtain by downloading all of the
submission data from the CrowdGrader website for each of the essays. The .json file
does not contain all of the necessary data, instead, it has endpoint URLs that you can
navigate to in order to obtain the remainder of the data (e.g., peer reviews). For this reason,
once you obtain this .json file from Crowdgrader, you have to process it using the
functions in crowdgrader.py (example shown in the crowdgrader.ipynb notebook).
Those functions generate an .xlsx file that you can then point to in the ESSAY_X_FILE.

* ESSAY_X_DSP_FILE contains information about late and DSP essay submissions, recorded
manually in a Google spreadsheet. You probably would need to change how this is handled.

* ZOOM_DIR is a directory containing Zoom participant data files, one for each Zoom session,
named as "zoom_[MONTH]_[DAY].csv". This can be used to supplement attendance data for students
who forgot to fill out the attendance survey but were present during the Zoom lecture.
