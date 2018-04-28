from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, desc
from json import dumps
from flask import jsonify, json

#using two databases
db_connect = create_engine('sqlite:///chinook.db') #sample dataset for sqlite
db2_connect = create_engine('sqlite:///sf-food-inspection.sqlite') #San Francisco Food Inspection Dataset. Downloaded from Public Affairs Data Journalism at Stanford starter pack site
app = Flask(__name__)
api = Api(app)

class Restaurants(Resource):
    def get(self):
        conn = db2_connect.connect()
        query = conn.execute("select business_id, business_name, inspection_score from inspection_records")
        result = {'restaurants': [dict(zip(tuple (query.keys()) , i)) for i in query.cursor]}
        return jsonify(result)  #returns as json

    def post(self):
        conn = db2_connect.connect()
        print(request.json)
        business_id = request.json['business_id']
        business_name = request.json['business_name']
        inspection_score = request.json['inspection_score']
        query = conn.execute("insert into inspection_records values(null,'{0}','{1}','{2}')".format(business_id,business_name,inspection_score))
        return {'status':'success'}

class Restaurants_Score(Resource):
    def get(self, score):
        conn = db2_connect.connect()
        query = conn.execute("select * from inspection_records where inspection_score =%d" %int(score))
        result = {'%d' %int(score): [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Employees(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from employees")
        result = {'employees': [i[0] for i in query.cursor.fetchall()]} #fetches first column that is employee id
        return jsonify(result)

class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

api.add_resource(Employees, '/employees')
api.add_resource(Employees_Name, '/employees/<employee_id>')
api.add_resource(Restaurants, '/restaurants')
api.add_resource(Restaurants_Score, '/restaurants/<score>')

if __name__ == '__main__':
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(port=5002)
