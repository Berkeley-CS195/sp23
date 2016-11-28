import json

try:
    from .sid_mapping import get_sid_name
except:
    from sid_mapping import get_sid_name
import os

GRADES = 'grades'
students = {}  # holds Student objectss. Will be used by publish.py to write out the grades
students_not_found = set()


class StudentGrades(object):
    def __init__(self, name, sid):
        self.name = name
        self.sid = int(sid)
        self.code_words = get_sid_name(self.sid)

        students[sid] = self

        self.attendances = {}
        self.surveys = {}

        self.essays = {}

        self.essay1_score = None
        self.essay2_score = None
        self.essay1_peer_reviews = None
        self.essay2_peer_reviews = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(len(self.attendances) + len(self.surveys)) + \
               ' grades for ' + self.name + " : " + self.code_words

    def serialize(self):
        """Return the json obj/dict obj for writing to a the grades.csv file eventually"""
        for essay_name, essay_grade in self.essays.items():
            # print(essay_name)
            if 'Assignment_1' in essay_name:
                # Giving everyone in essay 1 a 'Passing' score
                self.essay1_score = 'Passed' #if essay_grade['Grade'] > 1.29 else 'Not Passed'
                self.essay1_peer_reviews = essay_grade['Review Count']
            elif 'Assignment_2' in essay_name:
                self.essay2_score = 'Passed' if essay_grade['Grade'] > 1.2 else 'Not Passed' # borderline grades
                self.essay2_peer_reviews = essay_grade['Review Count']

        return {
            'Codeword': self.code_words,

            'Surveys': len(self.surveys),
            'Attendances': len(self.attendances) + 1, # Free attendance!

            'Essay 1 Score': self.essay1_score,
            'Essay 1 Peer Reviews': self.essay1_peer_reviews,

            'Essay 2 Score': self.essay2_score,
            'Essay 2 Peer Reviews': self.essay2_peer_reviews,

        }


############### Setup for processing Surveys and Attendance #############
from glob import glob
from csv import DictReader

email_file = open(os.path.join(GRADES, 'emailToSid.csv'))
email_reader = DictReader(email_file)
emails = {row['Email Address'].strip().lower(): row['Student ID'].strip() for row in email_reader}
email_file.close()


def get_sid_from_email(email):
    return emails[email]


def get_student(sid, name):
    if sid not in students:
        try:
            int(sid)
            student = StudentGrades(name, sid)
        except Exception as e:
            print('Error on student name = {} sid = {}'.format(name, sid))
            return
    else:
        student = students[sid]

    return student


def process_attendance_entry(attendance_response, attendance_name):
    sid, name = attendance_response['What is your SID?'], attendance_response['What is your name?']
    student = get_student(sid, name)
    if not student:
        return
    student.attendances[attendance_name] = True


def process_survey_entry(survey_response, survey_name):
    email = survey_response['Username'].strip()

    if not email:
        return

    if email not in emails:
        students_not_found.add(email)
        return

    sid = emails[email]
    student = get_student(sid, email)
    if not student:
        return
    student.surveys[survey_name] = True


missing_essay_emails = set()


def process_essay_entry(essay_grade_info, essay_name):
    email = essay_grade_info['Student'].strip().lower()

    if email not in emails:
        missing_essay_emails.add(email)
        return

    sid = get_sid_from_email(email)
    student_obj = get_student(sid, email)

    essay_grade_dict = {
        'Grade': float(essay_grade_info['Submission Grade']),
        'Review Count': essay_grade_info['Reviews Completed']
    }


    if essay_name in student_obj.essays and student_obj.essays[essay_name] != essay_grade_dict:
        if student_obj.essays[essay_name]['Grade'] > essay_grade_dict['Grade']:
            return # Otherwise, just let it overwrite below

    student_obj.essays[essay_name] = essay_grade_dict


#### Process surveys & attendances ####
attendances = glob(os.path.join(GRADES, 'attendance/*.csv'))

for attendance in attendances:
    with open(attendance) as attendance_file:
        reader = DictReader(attendance_file)
        for row in reader:
            process_attendance_entry(row, attendance)

surveys = glob(os.path.join(GRADES, 'surveys/*.csv'))
for survey in surveys:
    with open(survey) as survey_file:
        reader = DictReader(survey_file)
        for row in reader:
            process_survey_entry(row, survey)

#### Process essays and peer reviews #####
essays = glob(os.path.join(GRADES, 'essays/*.csv'))
for essay in essays:
    with open(essay) as essay_file:
        reader = DictReader(essay_file)
        for row in reader:
            process_essay_entry(row, essay)

# lost_souls = set()

"""
for essaygradefilename in ['essay1grades.json', 'essay2grades.json']:
    with open(os.path.join(GRADES, 'essays', essaygradefilename), 'r') as essay_grades_json:
        essay_grades = json.loads(essay_grades_json.read())

        for student_essay_obj in essay_grades:
            if student_essay_obj['email'] not in emails:
                lost_souls.add(student_essay_obj['email'])
            else:
                sid = emails[student_essay_obj['email']]
                student_obj = students[sid]  # I think I've named things badly, oops
                student_obj.essays.append(student_essay_obj)
                # student_obj.essay1_score = student_essay_obj.essay_passed
                # student_obj.essay1_peer_reviews = len(student_essay_obj.their_reviews)
"""
print('For essay we cant match the following emails to a SID')
print('\n'.join(missing_essay_emails))

#
# def print_row(student_obj):
#     return table_entry.format(
#         code_words=student_obj.code_words,
#         attendance_count=len(student_obj.attendances),
#         survey_count=len(student_obj.surveys))
#
#
# with open('grades_table.html', 'w') as grades_table:
#     for student in students.values():
#         grades_table.write(print_row(student))

# print('Following emails not found:')
# print("\r\n".join(students_not_found))
