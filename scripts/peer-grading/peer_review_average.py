# -*- coding: utf-8 -*-
"""
Grading

"""

#These are the packages you need to install, this will try to install them, otherwise use pip to install

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

#Ensure Canvas API token is in the designated file Canvas API Token.txt
print ('Before you begin the process, please ensure you have copy & pasted your Canvas API token into the file Canvas API Token.txt.')
confirmation = input ('Input any key to continue:')

token = input('Enter Canvas token')

url = "https://bcourses.berkeley.edu/"

#Course number
course = input('Input course ID and hit ENTER:\n')

#Input assignment ID number (located in URL)
assignment_id = input('Input assignment ID number and hit ENTER:\n')

print ('Processing data, please wait......\n')

try:
#Obtaining the assignment information (settings, assignment id, rubric id)
    assignmentInfo = requests.get(url + '/api/v1/courses/' + str(course) + '/assignments/' + str(assignment_id),
                 headers= {'Authorization': 'Bearer ' + token})

#Extracting assignment rubric id/rubric for the assignment
    assignmentInfo = json.loads(assignmentInfo.text)
    rubric_id = str(assignmentInfo['rubric_settings']['id'])

    payload = {'include': 'peer_assessments',
           'style' : 'full'}
    r = requests.get(url + '/api/v1/courses/' + str(course) + '/rubrics/' + rubric_id,
                 params = payload,
                 headers= {'Authorization': 'Bearer ' + token})

    rubric_return = json.loads(r.text)

#Obtaining assessor_id (person who did peer review), score for the peer reviews
    assessments_df = pd.DataFrame(rubric_return['assessments'])


#Obtaining user_id (person who was peer reviewed), completion and submission comments
    peerReview = requests.get(url + '/api/v1/courses/' + str(course) + '/assignments/' + assignment_id + '/peer_reviews',
                 headers= {'Authorization': 'Bearer ' + token})

    peerReviewInfo = json.loads(peerReview.text)
    peerReview_df = pd.read_json(peerReview.text)
    peerReview_df['user_id'] = peerReview_df['user_id'].astype(str)

#Merging data together into one csv file named 'peer review information.csv'
    merged_df = pd.merge(peerReview_df, assessments_df, how='outer', left_on=['assessor_id', 'asset_id'], right_on=['assessor_id', 'artifact_id'])
    merged_df.to_csv('peer review information.csv')

    #Create a table table with user_id and mean peer review score of each assignment
    #(make sure the mean score is rounded to 2, and the user_id is a string)
    scores = pd.DataFrame(merged_df.groupby('user_id')['score']
    meanScore = scores.nlargest().mean().round(2).reset_index())
    meanScore = meanScore[pd.notnull(meanScore['score'])]
    meanScore['user_id'] = meanScore['user_id'].astype(str)
    meanScore.to_csv("course_" + course + "_" + "assignment_" + assignment_id + '_complete mean score.csv')


    print('Data successfully gathered.\n')
    #if input is True, uploads scores onto Canvas Gradecenter (does not create new assignment)
    upload = input('Type True to upload peer review scores onto Gradecenter.\n')

    if upload==True:
        for index, row in meanScore.iterrows():

            student_id = str(row['user_id'])
            print(student_id)
            score = str(row['score'])


            payload = {'submission[posted_grade]': score}

            r = requests.put(url + '/api/v1/courses/' + str(course) + '/assignments/' + str(assignment_id) +'/submissions/' + str(student_id) + '/', params=payload, headers= {'Authorization': 'Bearer ' + token})
            print('Data successfully uploaded.')
    else:
        print('Data not uploaded')

except KeyError:
    print ("Something went wrong. Perhaps you provided an invalid.....\n")
    print ("Course ID?")
    print ("Canvas API Token?")
    print ("Assignment ID?")
