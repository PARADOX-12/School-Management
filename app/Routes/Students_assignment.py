from pymongo import MongoClient
from dotenv import load_dotenv
from app_config import Blueprint,json,jsonify,request,get_jwt_identity,jwt_required
from bson import ObjectId
import os

load_dotenv()

mongo_url = os.getenv('uri')
client = MongoClient(mongo_url)
db = client['School']


assignment_task = Blueprint('assignment' , __name__)


@assignment_task.route('/assignment' , methods=['PUT'])
@jwt_required()
def assignment():
   try:
       check_user = get_jwt_identity()
       if check_user[1] == 'Teacher':
           data = request.get_json()
           student_id = data['student_id']
           class_id = data['class_id']
           print(class_id)
           result = db.students.find_one({"_id" : ObjectId(student_id)})
           print(result)
           class_result = db.class_room.find_one({"_id": ObjectId(class_id)})
           print(class_result)
           if result:
               student_assigned = result.get("class_assigned", [])
               class_assigned = class_result.get("students_assignment", [])

               if class_id not in student_assigned and student_id not in class_assigned:
                   db.class_room.update_one({"_id": ObjectId(class_id)},
                                            {"$push": {"students_assignment": data["student_id"]}})
                   db.students.update_one({"_id": ObjectId(student_id)},
                                          {"$push": {"class_assigned": data["class_id"]}})
                   return jsonify({"Message": "Student assigned successfully"}), 200

               return jsonify({"Message": "Student already assigned"}), 403
           else:
               return jsonify({"Message": "Did not find class by this _id"}), 404

       else:
           return jsonify({
               'Message': "unauthorized to use this function"
           }), 401


   except Exception as e:
       return jsonify({
           "Error" : str(e)
       })


@assignment_task.route('/class/unassigned/<_id>' , methods = ['PUT'])
@jwt_required()
def unassigned(_id):
    try:
        check_user = get_jwt_identity()
        if check_user[1] == 'Teacher':
            body = request.get_json()
            student_id_to_remove = body.get('student_id')
            data = db.class_room.find_one({'_id': ObjectId(_id)})
            class_result = db.students.find_one({"_id": ObjectId(student_id_to_remove)})

            if data and class_result:
                student_assigned = data.get("students_assignment", [])
                class_assigned = class_result.get("class_assigned", [])

                if student_id_to_remove in student_assigned and _id in class_assigned:
                    student_assigned.remove(student_id_to_remove)
                    class_assigned.remove(_id)
                    db.class_room.update_one({"_id": ObjectId(_id)},
                                             {'$set': {"students_assignment": student_assigned}})
                    db.students.update_one({"_id": ObjectId(student_id_to_remove)},
                                           {'$set': {"class_assigned": class_assigned}})
                    return jsonify({"Message": "Students unassigned successfully"}), 200

                return jsonify({"Message": "Already unassigned"})

            else:
                return jsonify({"Message": "unable to find students_assigned with that _id"}), 404

        else:
            return jsonify({
                'Message': "unauthorized to use this function"
            }), 401


    except Exception as e:
        return jsonify({
            "Error" : str(e)
        })



@assignment_task.route('/class/<string:class_id>/students', methods=['GET'])
@jwt_required()
def get_students_in_class(class_id):
    try:
        check_user = get_jwt_identity()
        if check_user[1] == 'Teacher':
            class_object = db.class_room.find_one({"_id": ObjectId(class_id)})
            if class_object:
                student_ids = class_object.get("students_assignment", [])
                student_list = []
                for student in student_ids:
                    student_data = db.students.find_one({"_id": ObjectId(student)})

                    if student_data:
                        student_list.append(student_data)
                    else:
                        print(f"Student with ID {student_ids} not found")

                for student in student_list:
                    student["_id"] = str(student["_id"])

                return jsonify(student_list), 200
            else:
                return jsonify({"Message": "Class not found"}), 404

        else:
            return jsonify({
                'Message': "unauthorized to use this function"
            }), 401

    except Exception as e:
        return jsonify({"Error": str(e)})