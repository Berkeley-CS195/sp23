from sid_mapping import get_sid_name

students = {}

class StudentGrades(object):
    def __init__(self, name, sid):
        self.name = name
        self.sid = int(sid)
        self.code_words = get_sid_name(self.sid)

        students[sid] = self

        self.attendances = {}
        self.surveys = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(len(self.grades))+' grades for ' + self.name + " : " + self.code_words


############### Process Surveys and Attendance #############
from glob import glob # find all mah surveys
from csv import DictReader

surveys = glob('surveys/*.csv')
attendances = glob('attendance/*.csv')

def get_student(sid, name):
    if sid not in students:
        try:
            int(sid)
            student = StudentGrades(name, sid)
        except Exception as e:
            print('Error on student name = {} sid = {}'.format(name, sid))
            print e
            return
    else:
        student = students[sid]

    # if student.name.strip() != name.strip():
    #     print 'Name mismatch: {} != {}'.format(student.name, name)

    return student

def process_attendance_entry(attendance_response, attendance_name):
    sid, name = attendance_response['What is your SID?'], attendance_response['What is your name?']
    student = get_student(sid, name)
    if not student:
        return
    student.attendances[attendance_name] = True

def process_survey_entry(survey_reader, survey_name):
    sid, name = attendance_response['What is your SID?'], attendance_response['What is your name?']
    student = get_student(sid, name)
    if not student: return
    student.grades[survey_name] = True

for attendance in attendances:
    with open(attendance) as attendance_file:
        reader = DictReader(attendance_file)
        for row in reader:
            process_attendance_entry(row, attendance)

for survey in surveys:
    with open(survey) as survey_file:
        reader = DictReader(survey_file)
        for row in reader:
            # process_survey_entry(row, attendance)
            pass

table_entry = """
            <tr>
                <td> <b>{code_words}: </b> </td>
                <td>{attendance_count}/6</td>
                <td>{survey_count}/6</td>
            </tr>
            """
def print_row(student_obj):
    return table_entry.format(
        code_words= student_obj.code_words,
        attendance_count= len(student_obj.attendances),
        survey_count= len(student_obj.surveys))



# //print students
