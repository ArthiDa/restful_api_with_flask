from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

students = {
    'stu1' : { 'name': 'Arthi', 'dept' : 'CSE', 'sec' : 'B', 'language': 'Python' },
    'stu2' : { 'name': 'Mehrab', 'dept' : 'CSE', 'sec' : 'C', 'language': 'Python' },
    'stu3' : { 'name': 'Raihan', 'dept' : 'CSE', 'sec' : 'A', 'language': 'Ruby' },
    'stu4' : { 'name': 'Emdad', 'dept' : 'CSE', 'sec' : 'A', 'language': 'Ruby' },
}

def abort_if_student_doesnt_exist(stu_id):
    if stu_id not in students:
        abort(404, message= f"Student {stu_id} doesn't exist")

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name of the student is required', required=True)
parser.add_argument('dept', type=str, help='Department of the student is required', required=True)
parser.add_argument('sec', type=str, help='Section of the student is required', required=True)
parser.add_argument('language', type=str, help='Language of the student is required', required=True)


# Shows a single student details and lets us to delete and update a student details
class Student(Resource):
    def get(self, stu_id):
        abort_if_student_doesnt_exist(stu_id)
        return students[stu_id]
    
    def put(self, stu_id):
        abort_if_student_doesnt_exist(stu_id)
        args = parser.parse_args()
        student = {'name': args['name'],'dept': args['dept'],'sec': args['sec'],'language': args['language']}
        students[stu_id] = student
        return student, 201
    
    def delete(self, stu_id):
        abort_if_student_doesnt_exist(stu_id)
        del students[stu_id]
        return "",204

# Show a list of all students and lets us POST to add new students
class StudentList(Resource):
    def get(self):
        return students
    
    def post(self):
        args = parser.parse_args()
        stu_id = int(max(students.keys()).lstrip('stu')) + 1
        stu_id = 'stu%i' % stu_id
        students[stu_id] = {'name': args['name'],'dept': args['dept'],'sec': args['sec'],'language': args['language']}
        return students[stu_id], 201

# This is api home 
class Home(Resource):
    def get(self):
        return "Api is Running"


# Actually setup the Api resource routing here 
api.add_resource(Home, '/')
api.add_resource(StudentList, '/students')
api.add_resource(Student, '/students/<stu_id>')


if __name__ == '__main__':
    app.run(debug=True)