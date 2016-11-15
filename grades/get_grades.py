from .sid_mapping import get_sid_name
import os

GRADES = 'grades'
students = {} # holds Student objectss. Will be used by publish.py to write out the grades
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
        self.peer_reviews = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(len(self.attendances) + len(self.surveys)) + \
               ' grades for ' + self.name + " : " + self.code_words

    def serialize(self):
        """Return the json obj/dict obj for writing to a the grades.csv file eventually"""
        d = {
            'Surveys': len(self.surveys),
            'Attendances': len(self.attendances),
            'Codeword': self.code_words,
            'Essays': len(self.essays),
            'Peer Reviews': len(self.peer_reviews),
        }
        return d


############### Setup for processing Surveys and Attendance #############
from glob import glob
from csv import DictReader

email_file = open(os.path.join(GRADES, 'emailToSid.csv'))
email_reader = DictReader(email_file)
emails = {row['Email Address'].strip(): row['Student ID'].strip() for row in email_reader}
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


#### Process surveys & attendances ####
surveys = glob(os.path.join(GRADES, 'surveys/*.csv'))
attendances = glob(os.path.join(GRADES, 'attendance/*.csv'))

for attendance in attendances:
    with open(attendance) as attendance_file:
        reader = DictReader(attendance_file)
        for row in reader:
            process_attendance_entry(row, attendance)

for survey in surveys:
    with open(survey) as survey_file:
        reader = DictReader(survey_file)
        for row in reader:
            process_survey_entry(row, survey)

#### Print resulting data into grades_table.html
table_entry = """
            <tr>
                <td> <b>{code_words}: </b> </td>
                <td>{attendance_count}/6</td>
                <td>{survey_count}/6</td>
            </tr>
            """

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

print('Following emails not found:')
print("\r\n".join(students_not_found))
