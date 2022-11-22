#!/usr/bin/env python
# coding: utf-8
"""
https://gradescope-autograders.readthedocs.io/en/latest/troubleshooting/
"""
DIR = "/autograder/"
LOCAL_DIR = "."
DIR = LOCAL_DIR # FOR LOCAL TESTING TODO

import numpy as np
import pandas as pd
import json
import os

sid_json = json.load(open(os.path.join(DIR, "submission/SID.json"), 'r'))
sid = int(sid_json['SID'])
# grades = pd.read_csv('/autograder/source/grades.csv', index_col=0).loc[sid]

SID_COL = 3
TOT_LECTURES = 7
TOT_SURVEYS = 6
LECTURES = [f"Lecture {lecture:02d}" for lecture in range(2, TOT_LECTURES+2)]
SURVEYS = [f"Survey {survey:02d}" for survey in [1, 2, 3, 5, 6, 7, 8]]
grades = pd.read_csv(os.path.join(DIR, "source/grades.csv"),
                    index_col=SID_COL).loc[sid]

gs_output = {'tests': []}

def output_lecture_attendance(grades, gs_output):
  lectures_attended = [lec for lec in LECTURES if grades.loc[lec]]
  n_lectures = len(lectures_attended)
  n_makeups = grades['Makeup attendance']
  n_absences = TOT_LECTURES - n_lectures
  pass_lecture_attendance = (n_absences - n_makeups) <= 2
  lecture_attendance_outputs = [
    "You have attended these lectures:",
    "  " + "\n  ".join(lectures_attended),
    ## if makeups used, then incldue makeups
    f"Total lectures attended: {n_lectures}",
    f"Lectures where attendance was taken: {TOT_LECTURES}",
    f"Absences: {n_absences}",
    f"Makeups completed {n_makeups}",
    f"Lecture attendance OK? ((absences + makeups) <= 2) = {pass_lecture_attendance}",
    """Notes:
    - No attendance taken Lecture 01.
    - To request a lecture makeup beyond the two
    automatically excused absences, please post on Ed.
    Makeups involve attending Wednesday's H195 in-person 5-6pm section."""
      ]

  gs_output['tests'].append({
      'name': 'Lecture Attendance',
      'score': int(pass_lecture_attendance),
      'max_score': 1,
      'output': '\n'.join(lecture_attendance_outputs)
      })

def output_survey_completion(grades, gs_output):
  surveys_completed = [survey for survey in SURVEYS if grades.loc[survey]]
  survey_12 = ("Survey 01" in surveys_completed) + \
                ("Survey 02" in surveys_completed)
  other_surveys = len([survey for survey in surveys_completed \
                  if survey not in ["Survey 01", "Survey 02"]])
  n_surveys = survey_12 + other_surveys
  n_surveys_missed = TOT_SURVEYS - n_surveys
  pass_survey_completion = n_surveys_missed <= 2
  survey_completion_outputs = [
      "You have completed these surveys:",
      "  " + "\n  ".join(surveys_completed),
      f"Total surveys completed: {n_surveys}",
      "(Note Surveys 1, 2 count as one survey)",
      f"Survey completion OK? (surveys missed <= 2) = {pass_survey_completion}",
      """Notes:
      - Survey 01 and 02 counted as one single survey.
      - No Survey 04 was given.
      - To make up a survey, please fill it out
      by the end of the semester."""
    ]
  gs_output['tests'].append({
    'name': 'Survey Attendance',
    'score': int(pass_survey_completion),
    'max_score': 1,
    'output': '\n'.join(survey_completion_outputs)
    })
    
def output_overall_score(grades, gs_output):
    # for staff use when viewing on Gradescope
    print(grades)
    print(gs_output)

output_lecture_attendance(grades, gs_output)
output_survey_completion(grades, gs_output)
output_overall_score(grades, gs_output)

out_path = os.path.join(DIR, "results/results.json")
with open(out_path, 'w') as f:
    f.write(json.dumps(gs_output))
