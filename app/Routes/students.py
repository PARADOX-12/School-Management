from app_config import Blueprint,jsonify,json,request,jwt_required,get_jwt_identity
from app.Models.Students import Students

students_route = Blueprint('students', __name__)

@students_route.route('/students', methods = ['POST'])
@jwt_required()
def add_students():
    try:
        Students.add_students()
        return jsonify({
            'Message': 'student added Successfully'
        }), 200

    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500


@students_route.route('/students/get/<_id>', methods=['GET'])
@jwt_required()
def get_students(_id):
    try:
        data = Students.get_students(_id)
        if data:
            print('h')
            data = Students.get_students(_id)
            change = json.loads(data)
            valid_data = [{**items, "_id" : items["_id"]["$oid"], "DOB" : items["DOB"]["$date"]} for items in change]
            return valid_data, 200


        else:
            return jsonify({
                "Message": "Did not find student by this _id"
            }), 400


    except Exception as e:
        return jsonify({
            "Error": str(e)
        }),500



@students_route.route('/students/update/<_id>', methods=['PUT'])
@jwt_required()
def update_students(_id):
    try:
        if Students.get_students(_id):
            Students.update_students(_id)
            return jsonify({
                "Message": "Students updated successfully"
            }), 200

        else:
            return jsonify({
                "Message": "Cannot find students with that _id"
            }), 400


    except Exception as e:
        return jsonify({
            "Error": str(e)
        }), 500


@students_route.route('/students/delete/<_id>', methods=['DELETE'])
@jwt_required()
def delete_students(_id):
    try:
        check_user = get_jwt_identity()
        print(check_user)
        check = Students.get_students(_id)
        if check:
            if check_user[0] == 'Teacher':
                Students.delete_students(_id)
                return jsonify({
                    "Message": "Student delete successfully"
                }), 200

            return jsonify({
                "Message" : "unauthorized to use this function"
            }),401

        else:
            return jsonify({
                "Message": "Cannot find data by this _id to delete"
            }), 404


    except Exception as e:
        return jsonify({
            "Error": str(e)
        }), 500

