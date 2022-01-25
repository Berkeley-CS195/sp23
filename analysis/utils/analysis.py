import pandas as pd
import numpy as np

from datetime import datetime
from .loaders import email_to_sid, get_zoom_logs
from .helpers import *
from .constants import *

#
# Handle main attendance and pre-lecture survey Google sheets.
#

def process_sheets(sheets, form_name, reference_time, df):
    # Results in nicer column names.
    sheets = {k.replace('_', '/'):v for k,v in sheets.items()}

    for sheet_name, current_df in sheets.items():
        # Skip empty sheets.
        if len(current_df) == 0:
            continue

        # Define reference date for each submission.
        month, date = sheet_name.split('/')
        reference_date = datetime(year=2021, month=int(month), day=int(date), hour=reference_time[0], minute=reference_time[1], second=0)

        # Process data in the sheet.
        df = process_sheet(sheet_name, form_name, reference_date, current_df, df)

    return df

def add_zoom_info(sheet_name, df):
    """Adds Zoom timestamp for students who did not fill out attendance."""
    attendees_df = get_zoom_logs(sheet_name)

    # If there are no zoom logs for this date, then just return the original df.
    if attendees_df is None:
        return df

    # We only affect students who were in the Zoom call AND who don't have a valid timestamp.
    mask = df['SID'].isin(attendees_df['SID']) & df['Timestamp'].isna()
    df.loc[mask, 'Timestamp'] = attendees_df['Timestamp']
    df.loc[mask, 'Days Late'] = 0
    df.loc[mask, 'Status'] = 'Complete (Zoom Logs)'
    return df

def process_sheet(sheet_name, form_name, reference_date, current_df, main_df):
    # Avoid side-effects.
    current_df = current_df.copy()
    print('Processing {} for {}.'.format(form_name, sheet_name))

    # We MUST match on student ID. However, we also account for the fact that it might not be available.
    assert 'SID' in current_df or 'Email Address' in current_df

    # Map emails to SIDs (students might make typos) and remove unresolved (make sure to check manually!).
    current_df['SID'] = current_df['Email Address'].apply(email_to_sid).astype('int')
    current_df = current_df[current_df['SID'] != -1]

    # Get the make-up assignment responses, if applicable.
    extra_df = None
    if EXTRA_Q in current_df:
        extra_df = current_df[['SID', EXTRA_Q]].dropna(axis='index', subset=[EXTRA_Q]).drop_duplicates(subset='SID')

    # Students might submit their form multiple times. Keep the earliest timestamp only.
    current_df = current_df.sort_values(by=['SID', 'Timestamp']).drop_duplicates(subset='SID')[['SID', 'Timestamp']]

    # Now merge with the main dataframe.
    df = main_df.merge(current_df, how='left', on='SID')

    # Compute the lateness of submission and get just the number of days. (i.e. gives students 24-hour grace period)
    df['Days Late'] = (df['Timestamp'] - reference_date).dropna().apply(lambda x: x.days if x.days > 0 else 0)

    # Display completeness status for students.
    df['Status'] = df['Days Late'].apply(is_late)

    # Take into account make-up questions for students who submitted those.
    if extra_df is not None and len(extra_df) > 0:
        df.loc[df['SID'].isin(extra_df['SID']), 'Status'] = 'Complete (Make-up Question Answered)'

    # Take into account zoom logs for attendance.
    df = add_zoom_info(sheet_name, df) if form_name == 'Attendance' else df

    # Rename the time- and date-columns and return the dataframe.
    renames = {
        'Status': '{} ({}) Status'.format(form_name, sheet_name),
        'Days Late': '{} ({}) Days Late'.format(form_name, sheet_name),
        'Timestamp': '{} ({}) Timestamp'.format(form_name, sheet_name)
    }
    return df.rename(columns=renames)

#
# Handles makeup sheets.
#

def process_makeup_sheets(sheets, df):
    for sheet_name, current_df in sheets.items():
        # Skip empty sheets.
        if len(current_df) == 0:
            continue
        # Process data in the sheet.
        df = process_makeup_sheet(sheet_name, current_df, df)
    return df

def process_makeup_sheet(sheet_name, current_df, main_df):
    # Avoid side-effects.
    current_df = current_df.copy()
    print('Processing make-up assignments for {}.'.format(sheet_name))

    # We MUST match on student ID. However, we also account for the fact that it might not be available.
    assert 'SID' in current_df or 'Email Address' in current_df

    # Map emails to SIDs (students might make typos) and remove unresolved (make sure to check manually!).
    current_df['SID'] = current_df['Email Address'].apply(email_to_sid).astype('int')
    current_df = current_df[current_df['SID'] != -1]

    # Select columns with questions for the assignment.
    columns = current_df.columns.tolist()

    # In most cases there are multiple assignments to make-up.
    if MAKEUP_Q in columns:
        idx = columns.index(MAKEUP_Q) + 1
        makeup_cols = columns[idx:]

    # But for one week, there is only attendance make-up.
    else:
        idx = columns.index('SID') + 1
        makeup_cols = columns[idx:]

    # Validate the makeup-assignment responses.
    current_df[makeup_cols] = current_df[makeup_cols].applymap(validate_makeup)
    current_df['Completes'] = (current_df[makeup_cols] == 'Complete').sum(axis=1)

    # Expand the selected assignment column into multiple indicator columns.
    if MAKEUP_Q in columns:
        assignments_df = current_df[MAKEUP_Q].str.get_dummies(sep=', ').astype(bool)
        current_df = pd.concat([current_df, assignments_df], axis=1)
    else:
        current_df[['Lecture attendance', 'Pre-lecture survey']] = [True, False]

    # Now process the makeup assignments.
    for idx, row in current_df.iterrows():
        sid, completes_num = row['SID'], row['Completes']

        # Start with attendance.
        if row['Lecture attendance'] and completes_num > 0:
            status_col = WEEK_TO_ATTENDANCE[sheet_name]
            main_df.loc[main_df['SID'] == sid, status_col] = 'Complete (Make-up Question Answered)'
            completes_num = completes_num - 1

        # Then pre-lecture survey.
        if row['Pre-lecture survey'] and completes_num > 0:
            status_col = WEEK_TO_SURVEY[sheet_name]
            main_df.loc[main_df['SID'] == sid, status_col] = 'Complete (Make-up Question Answered)'

    return main_df

#
# Handles essay sheets.
#

def process_essays(sheets, df):
    for sheet_name, current_df in sheets.items():
        # Skip empty sheets.
        if len(current_df) == 0:
            continue
        # Process data in the sheet.
        df = process_essay(sheet_name, current_df, df)

    # Count total number of reviews and simply show whether complete or not.
    df['Peer Reviews'] = df.apply(lambda x: count_reviews(x['Essay 1 Reviews'], x['Essay 2 Reviews']), axis=1)
    df['Peer Reviews'] = df['Peer Reviews'].apply(lambda x: 'Complete' if x >= MIN_REVIEW_COUNT else '*Missing*')
    return df

def process_essay(sheet_name, current_df, main_df):
    # Avoid side-effects.
    current_df = current_df.copy()
    print('Processing essay assignments for {}.'.format(sheet_name))

    # We MUST match on student ID. However, we also account for the fact that it might not be available.
    assert 'SID' in current_df or 'Email Address' in current_df

    # Map emails to SIDs (students might make typos) and remove unresolved (make sure to check manually!).
    current_df['SID'] = current_df['Email Address'].apply(email_to_sid).astype('int')
    current_df = current_df[current_df['SID'] != -1].drop(columns=['Email Address'])

    # Merge with the main dataframe.
    df = main_df.merge(current_df, how='left', on='SID')

    # Replace missing grades with 0's.
    df['Grade'] = df['Grade'].fillna(value=0)

    # Replace missing reviews with 0.
    df['Reviews Num'] = df['Reviews Num'].fillna(value=0)

    # Submissions can be "Complete" (avg. grade == 2), "Submitted", or "Missing".
    df['Submission date'] = df.apply(lambda x: get_essay_status(x['Submission date'], x['Grade']), axis=1)

    # Rename columns and return the dataframe.
    renames = {
        'Reviews Num': '{} Reviews'.format(sheet_name),
        'Submission date': '{}'.format(sheet_name),
        'Grade': '{} Grade'.format(sheet_name)
    }
    return df.rename(columns=renames)

#
# Handles makeup essay sheets.
#

def process_essay_makeup_sheets(sheets, df):
    for sheet_name, current_df in sheets.items():
        # Skip empty sheets.
        if len(current_df) == 0:
            continue
        # Process data in the sheet.
        df = process_essay_makeup_sheet(sheet_name, current_df, df)
    return df

def process_essay_makeup_sheet(sheet_name, current_df, main_df):
    # Avoid side-effects.
    current_df = current_df.copy()
    print('Processing essay make-up assignments for {}.'.format(sheet_name))

    # We MUST match on student ID. However, we also account for the fact that it might not be available.
    assert 'SID' in current_df or 'Email Address' in current_df

    # Map emails to SIDs (students might make typos) and remove unresolved (make sure to check manually!).
    current_df['SID'] = current_df['Email Address'].apply(email_to_sid).astype('int')
    current_df = current_df[current_df['SID'] != -1].drop(columns=['Email Address'])

    # Simply indicate whether complete or missing.
    current_df['Reviewed?'] = current_df['Reviewed?'].apply(lambda x: 'Complete' if (x == 'Pass' or x == 'Excused') else '*Missing*')

    # Add the data into the correct rows and cols of the main dataframe.
    makeup_SIDs = current_df['SID']
    df = main_df.merge(current_df, how='left', on='SID')
    df.loc[df['SID'].isin(makeup_SIDs), sheet_name] = df.loc[df['SID'].isin(makeup_SIDs), 'Reviewed?']

    # Afterwards, we don't need that extra column.
    df = df.drop(columns=['Reviewed?'])
    return df
