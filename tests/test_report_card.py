from report_card import __version__
from report_card.gen_json import CsvStudentToJSON, School ,Student


def test_csv_interpret():
    interp = CsvStudentToJSON()
    actual = interp.csv_interpreter('StudentData/students.csv')
    expected = [['1','A'],['2','B'],['3','C']]
    assert actual == expected

def test_file_not_found():
    interp = CsvStudentToJSON()
    actual = interp.csv_interpreter('StudentData/student.csv')
    expected = 'Error 2'
    assert actual == expected


def test_getStudents(self):
    pass