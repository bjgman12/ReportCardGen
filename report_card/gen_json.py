import csv
import json
import sys



class CsvStudentToJSON:


    

    def csv_interpreter(self,filePath):
        """Turns CSV into 2D Array

        Args:
            filePath ([str]): [path to csv file]

        Returns:
            [list]: [csv in 2d Array from]
        """
        interpreted = [] 
        try:
            with open(filePath) as csv_file:
                csv_reader = csv.reader(csv_file,delimiter=',')

                line_count = 0 
                for row in csv_reader:
                    if line_count == 0:
                        line_count +=1
                    else:
                        line_count +=1
                        interpreted.append(row)

                return interpreted
        except FileNotFoundError as e:
            return f'Error {e.errno}'

    def interpreted_to_list_of_ob(self,interpreted,key1,key2,key3):
        """[takes interpreted 2d Array and turns it into a dictionary, keys are assigned via args]

        Args:
            interpreted ([list]): [2d Array]
            key1 ([str]): [dictionary key]
            key2 ([str]): [dictionary key]
            key3 ([str]): [dictionary key]

        Returns:
            [dict]: [csv file now represented in a dictionary]
        """
        ret_list = []
        for row in interpreted:
            tempStu =  { key1 : row[0], key2 : row[1], key3 : row[2] }
            ret_list.append(tempStu)

        return ret_list



class School(CsvStudentToJSON):
    def __init__(self,courses,students,marks,tests,json):
        self.formated_students = []
        self.courses_path = courses
        self.studentpath = students
        self.mark_path = marks
        self.test_path = tests
        self.json_path = json
        self.students = self.getStudents()


    

    def getStudents(self):
        """[utilised csv_interpreter to grab students]

        Returns:
            [list]: [2d representation of students]
        """
        raw = self.csv_interpreter(self.studentpath)
        stagedStus = []

        for row in raw:
                tempStu =  Student(row[0],row[1])
                stagedStus.append(tempStu)
        
        print(stagedStus)
        return stagedStus

    def formatStudents(self):
        """[students to dict]
        """
        for student in self.students:
            self.formated_students.append(student.format())

    def getCurriculum(self):
        """[Curriculum to dict]

        Returns:
            [dict]: [courses]
        """
        rawCurriculum = self.csv_interpreter(self.courses_path)
        return self.interpreted_to_list_of_ob(rawCurriculum,'id','name','teacher')


    def getTests(self):
        """[Tests to dict]
        """
        rawTests = self.csv_interpreter(self.test_path)
        return(self.interpreted_to_list_of_ob(rawTests,'id','course_id','weight'))

    def getMarks(self):
        """[Marks to dict]

        Returns:
            [dict]: [student marks]
        """
        rawMarks = self.csv_interpreter(self.mark_path)
        return self.interpreted_to_list_of_ob(rawMarks,'test_id','student_id','mark')

    def marks_to_students(self):
        """[Sorts marks to corresponding students]
        """
        marks = self.getMarks()
        for student in self.students:
            for mark in marks:
                if mark['student_id'] == student.id:
                    student.tests.append(mark)


    def show_students(self):
        """[function to show students in current state]
        """
        for student in self.students:
            print(student,'\n')

    def marks_to_courses(self):
        """[Sorts each students marks to corresponding courses]
        """
        testData = self.getTests()

        for student in self.students:
            temp_scores = []
            for mark in student.tests:
                for test in testData:
                    if mark['test_id'] == test['id']:
                        sum = round(float(mark['mark']) * float(test['weight'])/100,2)
                        weight_course_id = { 'weighted' : sum , 'course_id' : test['course_id']}
                        temp_scores.append(weight_course_id)
            student.weightedScores = temp_scores


    def student_schedules(self):
        """[Gives each student their courses]
        """
        for student in self.students:
            student.schedules()

    def average_scores(self):
        """[Calculates and assigns average grade for each course of each student]
        """
        for student in self.students:
           student.average_grades()

    def course_info(self):
        """[Finds teachers and course names based on id]
        """
        courses = self.getCurriculum()
        for student in self.students:
            student.get_course_info(courses)

    def total_averages(self):
        """[Calculates and assigned each student total averages]
        """
        for student in self.students:
            student.total_average()
         

    def filter_tests(self,weighted_scores,id):
        """[Associates tests and weighted scores with corresponding courses]

        Args:
            weighted_scores ([float]): [test scores weighted]
            id ([int]): [course-id]

        Returns:
            [list]: [weighted scores]
        """
        ret_val = []

        for score in weighted_scores:
            if score['course_id'] == id:
                ret_val.append(score['weighted'])

        return ret_val


    def to_JSON(self):
        """[Writes Completed report card to JSON file]
        """
        self.formatStudents()
        newObj = { 'students ' : self.formated_students}
        with open(self.json_path, 'w') as my_output:
            json.dump(newObj,my_output,indent = 4)



class Student(CsvStudentToJSON):
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.totalAverage = 0
        self.weightedScores = []
        self.courses = []
        self.tests = []

    def format(self):
        """[Returns report card formatted students]

        Returns:
            [dict]: [students for report cards]
        """
        return { 'id': self.id , 'name' : self.name, 'total_Average' : self.totalAverage, 'courses' : self.courses}
    
    def average_grades(self):
        """[Calulated Average course scores]
        """
        for course in self.courses:
            course['course_average'] = []
            for score in self.weightedScores:
                if score['course_id'] == course['course_id']:
                    course['course_average'].append(float(score['weighted']))

            course['course_average'] = sum(course['course_average'])

    def get_course_info(self,courses):
        """[course info / name/ teacher]

        Args:
            courses ([dcit]): [courses]
        """
        for subject in self.courses:
            for course in courses:
                if course['id'] == subject['course_id']:
                    subject['course_name'] = course['name']
                    subject['teacher'] = course['teacher']

    def total_average(self):
        """[Students Total grade]
        """
        grades = []
        for subject in self.courses:
            grades.append(subject['course_average'])
        
        self.totalAverage = round(sum(grades)/len(grades),2)
    
    def schedules(self):
        ids = []
        for score in self.weightedScores:
            if score['course_id'] not in ids:
                ids.append(score['course_id'])
        for id in ids:
            self.courses.append({ 'course_id' : id })



            
def getArgs():
    """[Grabs Command line Args]

    Returns:
        [list]: [file paths]
    """
    sys.argv.pop(0)

    if len(sys.argv) == 5:
        return sys.argv
    else:
        print('We need all the file paths')
                
                

if __name__ == "__main__":
    paths = getArgs()
    CSTJ = CsvStudentToJSON()
    sc = School(paths[0],paths[1],paths[2],paths[3],paths[4])
    sc.getCurriculum()
    sc.marks_to_students()
    sc.marks_to_courses()
    sc.student_schedules()
    sc.average_scores()
    sc.course_info()
    sc.total_averages()
    sc.show_students()
    sc.to_JSON()
