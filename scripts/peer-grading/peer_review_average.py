# -*- coding: utf-8 -*-
"""
Grading

"""

# These are the packages you need to install, this will try to install them, otherwise use pip to install

import argparse

parser = argparse.ArgumentParser(
    prog='Canvas Peer Grader',
    description='What the program does')
parser.add_argument('-c', '--course', help='Course ID', required=True)
parser.add_argument('-t', '--token', help='Token', required=True)
parser.add_argument('-a', '--assignment', help='Assignment ID', required=True)

args = parser.parse_args()

course_id = args.course
token = args.token
assignment_id = args.assignment
confirmation = input('Input any key to continue:')

url = "https://bcourses.berkeley.edu/"


DRY_RUN = False

try:
    import requests
except:
    import pip
    pip.main(['install', 'requests'])
    import requests

try:
    import pandas as pd
except:
    import pip
    pip.main(['install', 'pandas'])
    import pandas as pd

try:
    import json
except:
    import pip
    pip.main(['install', 'json'])
    import json

print('Processing data, please wait......\n')


def course_url(end=''):
    return f'{url}/api/v1/courses/{course_id}/{end}'


auth_token = {'Authorization': f'Bearer {token}'}

try:
    # Obtaining the assignment information (settings, assignment id, rubric id)
    assignmentInfo = requests.get(
        course_url(f'assignments/{assignment_id}'),
        headers=auth_token
    )

    # Extracting assignment rubric id/rubric for the assignment
    assignmentInfo = json.loads(assignmentInfo.text)

    rubric_id = str(assignmentInfo['rubric_settings']['id'])

    payload = {'include': 'peer_assessments', 'style': 'full'}
    r = requests.get(course_url(f'/rubrics/{rubric_id}'),
                     params=payload,
                     headers=auth_token)

    rubric_return = json.loads(r.text)

    # Obtaining assessor_id (person who did peer review), score for the peer reviews
    assessments_df = pd.DataFrame(rubric_return['assessments'])

    # Obtaining user_id (person who was peer reviewed), completion and submission comments
    peerReview = requests.get(course_url(f'/assignments/{assignment_id}/peer_reviews'),
                              headers=auth_token)

    peerReviewInfo = json.loads(peerReview.text)
    peerReview_df = pd.read_json(peerReview.text)
    peerReview_df['user_id'] = peerReview_df['user_id'].astype(str)

    # Merging data together into one csv file named 'peer review information.csv'
    merged_df = pd.merge(peerReview_df, assessments_df, how='outer', left_on=[
                         'assessor_id', 'asset_id'], right_on=['assessor_id', 'artifact_id'])
    merged_df.to_csv('peer review information.csv')

    # Create a table table with user_id and mean peer review score of each assignment
    # (make sure the mean score is rounded to 2, and the user_id is a string)
    # breakpoint()
    groups = merged_df.groupby('user_id')
    scores = pd.DataFrame(groups['score'])
    # get the 2 largest scores from the 2nd column of scores
    scores['max'] = scores[1].apply(lambda x: sorted(x, reverse=True)[:2])
    scores['mean'] = scores['max'].apply(lambda x: round(sum(x) / len(x), 2))
    # breakpoint()
    scores['user_id'] = scores[0].astype(str)

    # Write the output to a csv file named 'peer_review_average.csv'
    scores.to_csv('peer_review_average.csv', index=False)
    print('Done!')

    meanScore = scores[pd.notnull(scores['mean'])]
    meanScore.to_csv(f'course_{course_id}_assignment_{assignment_id}_mean.csv')

    print('Data successfully gathered.\n')

    if not DRY_RUN:
        for index, row in meanScore.iterrows():
            student_id = row['user_id']
            score = row['mean']
            print(student_id, score)

            payload = {'submission[posted_grade]': score}
            r = requests.put(
                course_url(f'/assignments/{assignment_id}/submissions/{student_id}/'),
                params=payload,
                headers=auth_token
            )
            print('Data successfully uploaded.')
    else:
        print('Data not uploaded')
        for row in meanScore.iterrows():
            print(row)
finally:
    print('done')
# except Exception as e:
#     print(e)
#     print("Something went wrong. Perhaps you provided an invalid.....\n")
#     print("Course ID?")
#     print("Canvas API Token?")
#     print("Assignment ID?")
