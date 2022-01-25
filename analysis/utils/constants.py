import os

# Define file names.
DATA_DIR = os.path.join('..', 'data')
ROSTER_FILE = os.path.join(DATA_DIR, 'roster.csv')
ROSTER_H195_FILE = os.path.join(DATA_DIR, 'roster_h195.csv')
ATTENDANCE_FILE = os.path.join(DATA_DIR, 'attendance.xlsx')
SURVEY_FILE = os.path.join(DATA_DIR, 'survey.xlsx')
MAKEUP_FILE = os.path.join(DATA_DIR, 'makeup_responses.xlsx')

ESSAY_1_CROWD_FILE = os.path.join(DATA_DIR, 'essay_1.json')
ESSAY_1_FILE = os.path.join(DATA_DIR, 'essay_1.xlsx')
ESSAY_1_DSP_FILE = os.path.join(DATA_DIR, 'essay_1_dsp.xlsx')

ESSAY_2_CROWD_FILE = os.path.join(DATA_DIR, 'essay_2.json')
ESSAY_2_FILE = os.path.join(DATA_DIR, 'essay_2.xlsx')
ESSAY_2_DSP_FILE = os.path.join(DATA_DIR, 'essay_2_dsp.xlsx')

ESSAY_3_FILE = os.path.join(DATA_DIR, 'essay_3.xlsx')

ZOOM_DIR = os.path.join(DATA_DIR, 'zoom')
ZOOM_FILES = [os.path.join(ZOOM_DIR, f) for f in os.listdir(ZOOM_DIR) if f.endswith('.csv')]

# Define deadline time variables.
SURVEY_HR = 23
SURVEY_MN = 59
ATTEND_HR = 13
ATTEND_MN = 30

# How many days to give as a grace period?
ALLOWED_DAYS_LATE = 7

# How many minutes participant had to stay in the zoom call?
MIN_ZOOM_DURATION = 10

# How many reviews need to complete to pass.
MIN_REVIEW_COUNT = 3

# Define other constants.
COLUMNS = [
    'Email Address', 'Timestamp'
]
EXTRA_Q = 'What did you find the most interesting about the readings?'
MAKEUP_Q = 'What assignment are you making up for this week?'

SURVEY_COLS = [
    'Survey (11/30)', 'Survey (11/16)', 'Survey (11/09)',
    'Survey (10/26)', 'Survey (10/19)', 'Survey (10/12)',
    'Survey (10/05)', 'Survey (09/28)', 'Survey (09/20)',
    'Survey (09/14)', 'Survey (09/06)', 'Survey (08/31)', 'Survey (08/25)'
]
SURVEY_COLS = ['{} Status'.format(x) for x in SURVEY_COLS]

ATTENDANCE_COLS = [
    'Attendance (12/01)', 'Attendance (11/17)', 'Attendance (11/10)', 'Attendance (11/03)',
    'Attendance (10/27)', 'Attendance (10/20)', 'Attendance (10/13)',
    'Attendance (10/06)', 'Attendance (09/29)', 'Attendance (09/22)',
    'Attendance (09/15)', 'Attendance (09/08)', 'Attendance (09/01)', 'Attendance (08/25)'
]
ATTENDANCE_COLS = ['{} Status'.format(x) for x in ATTENDANCE_COLS]

ESSAY_COLS = [
    'Essay 1', 'Essay 1 Reviews', 'Essay 2', 'Essay 2 Reviews', 'Essay 3', 'Peer Reviews'
]

CLASS_REQS = [
    'Attendance', 'Survey', 'Essay 1', 'Essay 2', 'Essay 3', 'Peer Reviews'
]

# Useful dictionary for make-up assignments.
WEEK_TO_ATTENDANCE = {
    'Week 1': 'Attendance (08/25) Status',
    'Week 2': 'Attendance (09/01) Status',
    'Week 3': 'Attendance (09/08) Status',
    'Week 4': 'Attendance (09/15) Status',
    'Week 5': 'Attendance (09/22) Status',
    'Week 6': 'Attendance (09/29) Status',
    'Week 7': 'Attendance (10/06) Status',
    'Week 8': 'Attendance (10/13) Status',
    'Week 9': 'Attendance (10/20) Status',
    'Week 10': 'Attendance (10/27) Status',
    'Week 11': 'Attendance (11/03) Status',
    'Week 12': 'Attendance (11/10) Status',
    'Week 13': 'Attendance (11/17) Status',
    'Week 14': 'Attendance (12/01) Status'
}

WEEK_TO_SURVEY = {
    'Week 2': 'Survey (08/31) Status',
    'Week 3': 'Survey (09/06) Status',
    'Week 4': 'Survey (09/14) Status',
    'Week 5': 'Survey (09/20) Status',
    'Week 6': 'Survey (09/28) Status',
    'Week 7': 'Survey (10/05) Status',
    'Week 8': 'Survey (10/12) Status',
    'Week 9': 'Survey (10/19) Status',
    'Week 10': 'Survey (10/26) Status',
    'Week 12': 'Survey (11/09) Status',
    'Week 13': 'Survey (11/16) Status',
    'Week 14': 'Survey (11/30) Status'
}
