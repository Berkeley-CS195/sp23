import pandas as pd
import numpy as np

from .constants import ALLOWED_DAYS_LATE

#
# Functions that support data analysis.
#

def is_late(x):
    if np.isnan(x):
        return '*Missing*'
    elif x > ALLOWED_DAYS_LATE:
        return '*Incomplete* (Late Submission)'
    else:
        return 'Complete (Form Submission)'

def validate_makeup(xs):
    "The makeup assignment submission should be between 200 and 400 words."
    if isinstance(xs, float) and np.isnan(xs):
        return '*Missing*'
    word_num = len(xs.split())
    # We can be even more lenient, just in case.
    return 'Complete' if word_num >= 100 else '*Incomplete*'

def get_essay_status(date, grade):
    if pd.isnull(date):
        return '*Missing*'
    if grade == 2:
        return 'Complete'
    else:
        return 'Submitted'

def count_reviews(x, y):
    if np.isnan(x) and np.isnan(y):
        return 0
    if np.isnan(x):
        return y
    if np.isnan(y):
        return x
    return x + y

def count_completes(xs):
    is_complete = lambda x: (('Complete' in x) or ('Excused' in x)) and ('Incomplete' not in x)
    count = len([x for x in xs if is_complete(x)])
    return '{} / {}'.format(count, len(xs))

def determine_pass(x, assignment):
    y, z = x.split(' / ')
    y, z = int(y), int(z)
    if assignment == 'Attendance':
        return 'Complete' if (z - y) <= 2 else '*Incomplete*'
    elif assignment == 'Survey':
        return 'Complete' if (z - y) <= 3 else '*Incomplete*'
    else:
        return 'Complete' if (z - y) == 0 else '*Incomplete*'
