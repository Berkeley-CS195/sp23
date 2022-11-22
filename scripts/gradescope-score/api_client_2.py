#!/usr/bin/env python3
import json
import getpass
import numpy as np
import os
import pandas as pd
import requests

BASE_URL = 'https://www.gradescope.com'
COURSE_ID = 437281 # CHANGE THIS
ASSIGNMENT_ID = 2394038 # CHANGE THIS

GRADES_PATH = os.path.join("autograder", "grades.csv")
SID_JSON = "SID.json"

class APIClient:
    def __init__(self):
        self.session = requests.Session()

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def log_in(self, email, password):
        url = "{base}/api/v1/user_session".format(base=BASE_URL)

        form_data = {
            "email": email,
            "password": password
        }
        r = self.post(url, data=form_data)

        print(r)
        self.token = r.json()['token']

    def upload_pdf_submission(self, course_id, assignment_id, student_email, filename):
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        files = {'pdf_attachment': open(filename, 'rb')}

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

    def replace_pdf_submission(self, course_id, assignment_id, student_email, filename):
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions/replace_pdf".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        files = {'pdf_attachment': open(filename, 'rb')}

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

    def upload_programming_submission(self, course_id, assignment_id, student_email, filenames):
        url = "{base}/api/v1/courses/{0}/assignments/{1}/submissions".format(
            course_id, assignment_id, base=BASE_URL
        )

        form_data = {
            "owner_email": student_email
        }
        files = [('files[]', (filename, open(filename, 'rb'))) for filename in filenames]

        request_headers = {'access-token': self.token}
        r = self.post(url, data=form_data, headers=request_headers, files=files)
        return r

if __name__ == '__main__':
    client = APIClient()
    email = input("Please provide the email address on your Gradescope account: ")
    password = getpass.getpass('Password: ')
    client.log_in(email, password)
    grades = pd.read_csv(GRADES_PATH)
    for i in grades.index:
        if np.isnan(grades.loc[i, 'SID']):
            continue
        sid = {'SID' : int(grades.loc[i, 'SID'])}
        with open(SID_JSON, 'w') as f:
            f.write(json.dumps(sid))
        print(grades.loc[i, 'Email'], int(grades.loc[i, 'SID']))
        client.upload_programming_submission(COURSE_ID, ASSIGNMENT_ID, grades.loc[i, 'Email'], [SID_JSON])
    # Use the APIClient to upload submissions after logging in, e.g:
    # client.upload_pdf_submission(1234, 5678, 'student@example.edu', 'submission.pdf')
    # client.upload_programming_submission(1234, 5678, 'student@example.edu', ['README.md', 'src/calculator.py'])
    # You can get course and assignment IDs from the URL, e.g.
    # https://www.gradescope.com/courses/1234/assignments/5678
    # course_id = 1234, assignment_id = 5678
