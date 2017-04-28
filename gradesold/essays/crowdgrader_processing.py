#!/usr/bin/python

"""
This will place a json file with all the students score per essay in the directory of this script

Downloaded from crowdgrader: http://doc.crowdgrader.org/crowdgrader-documentation/downloading-all-data

Modified by Daniel Feldman November 2016 d.feldman@berkeley.edu


Copyright CrowdGrader LLC, 2014

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import getopt
import json
import os
import os.path
from urllib.request import urlopen
import sys
from collections import defaultdict

PASSING_THRESHOLD = 1.6  # Score needed to pass an essay


def usage():
    print("Usage: download_assignment.py <assignment_file.json> <destination_directory>")


email_to_names = {}


# ESSAY_NAME = None


class StudentEssayGrades(object):
    essay_name = None

    def __init__(self, email):
        self.email = email
        # self.essay_name = ESSAY_NAME
        self.their_reviews = []
        self.review_scores = []

    @property
    def essay_passed(self):
        num_reviews = len(self.review_scores)

        if self.review_scores is [] or num_reviews == 0:
            return False

        if sum(self.review_scores) / num_reviews > PASSING_THRESHOLD:
            return True

        return False

    @property
    def peer_reviews(self):
        return len(self.their_reviews)

    def serialize(self):
        return {
            'email': self.email,
            'essay name': self.essay_name,
            'passing': self.essay_passed,
            'review_count': len(self.their_reviews),
        }


student_essay_grades_list = {}


def get_or_make_student(email):
    if email in student_essay_grades_list:
        return student_essay_grades_list[email]
    else:
        new_student = StudentEssayGrades(email)
        student_essay_grades_list[email] = new_student
        return new_student


def main(json_file_name, dest_dir):
    if check_directory_exists(dest_dir):
        print("Error: Destination directory already exists.")

    assignment_data = read_json_file(json_file_name)

    # create all the Student objects
    StudentEssayGrades.essay_name = assignment_data.get('Assignment')
    for subm in assignment_data.get('Submission list', []):
        get_or_make_student(subm['User email'])

    for submission in assignment_data.get('Submission list', []):
        essay_author = student_essay_grades_list[submission['User email']]

        json_dir = os.path.join(dest_dir, essay_author.email + '.json')
        reviews_json = get_json(submission, json_dir)  # Either download it or read it from the disk

        for review in reviews_json['Reviews']:
            if review['Declined']:
                continue
            reviewer = get_or_make_student(review['Review author'])
            reviewer.their_reviews.append(essay_author)

            essay_author.review_scores.append(review['Review grade'])

    print("All assignment data downloaded.")

    gradesfile_name = (dest_dir + 'grades.json').replace('/', '')
    with open(gradesfile_name, 'w') as gradesfile:
        students_serialized = [student.serialize() for student in student_essay_grades_list.values()]
        grades_json = json.dumps(students_serialized)
        gradesfile.write(grades_json)
        print('Wrote grades file to {}'.format(gradesfile_name))


def get_json(submission_json, file_path):
    review_link = submission_json['Reviews']  # get review from json

    review_json = None
    if os.path.isfile(file_path):
        f = open(file_path, 'r')
        try:
            review_json = json.loads(f.read())
        except:
            review_json = None
        f.close()

    if review_json == {} or review_json is None:
        review_data = my_url_open(review_link)[0]
        f = open(file_path, 'w')
        f.write(review_data)
        print("Downloaded reviews for {}'s essay".format(submission_json['User email']))
        f.close()
        review_json = json.loads(review_data)

    return review_json


def check_directory_exists(dir_name):
    return os.path.isdir(dir_name)


def read_json_file(json_file_name):
    """Reads the json file containing the assignment data."""
    try:
        f = open(json_file_name, 'r')
        d = json.loads(f.read())
        return d
    except Exception as e:
        print("Error:", e)
        sys.exit(2)


def make_directory(dir_name):
    if not check_directory_exists(dir_name):
        os.makedirs(dir_name)


def my_url_open(url, n_retries=3):
    for i in range(n_retries):
        try:
            w = urlopen(url)
            return w.read().decode('utf-8'), w.info()
        except Exception as e:
            print("Error in download:", e)
        print("Retrying")
    print("Failed")
    return '', []


def tostring(s):
    t = s.encode('utf-8', 'ignore')
    return t.replace('\r\n', os.linesep)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[3:], "", [])
    except getopt.GetoptError as e:
        print(str(e))
        usage()
        sys.exit(2)

    if len(sys.argv) < 3:
        usage()
        sys.exit(2)

    main(sys.argv[1], sys.argv[2])
