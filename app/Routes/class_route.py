from app_config import Blueprint,jsonify,json,request,jwt_required,get_jwt_identity
from app.Models.Class import ClassRoom

class_route = Blueprint('class', __name__)

@class_route.route('/class', methods = ['POST'])
@jwt_required()
def add_class():
    try:
        check_user = get_jwt_identity()
        body = request.get_json()
        data = ClassRoom.classroom_exist(body['name'])
        if data:
            return jsonify({
                "Message" : "classroom already exist"
            }),403
        if check_user[1] == 'Teacher':
            ClassRoom.add_class()
            return jsonify({
                'Message': 'class added Successfully'
            }), 201

        return jsonify({
            'Message': "unauthorized to use this function"
        }), 401

    except Exception as e:
        return jsonify({
            "Message": "Error occured ", "Error": str(e)
        }), 500



@class_route.route('/class/get/<_id>', methods=['GET'])
@jwt_required()
def get_class(_id):
    try:
        check_user = get_jwt_identity()
        if ClassRoom.get_class(_id):
            if check_user[1] == 'Teacher':
                data = ClassRoom.get_class(_id)
                change = json.loads(data)
                valid_data = [{**items, "_id": items["_id"]["$oid"]} for items in change]
                return valid_data, 200

            return jsonify({
                'Message': "unauthorized to use this function"
            }), 401

        else:
            return jsonify({
                "Message": "Did not find class by this _id"
            }), 400


    except Exception as e:
        return jsonify({
            "Error": str(e)
        }),500



@class_route.route('/class/update/<_id>', methods=['PUT'])
@jwt_required()
def update_class(_id):
    try:
        check_user = get_jwt_identity()
        if ClassRoom.get_class(_id):
            if check_user[1] == 'Teacher':
                ClassRoom.update_class(_id)
                return jsonify({
                    "Message": "class updated successfully"
                }), 200

            return jsonify({
                'Message': "unauthorized to use this function"
            }), 401


        else:
            return jsonify({
                "Message": "Cannot find class with that _id"
            }), 400


    except Exception as e:
        return jsonify({
            "Error": str(e)
        }), 500


@class_route.route('/class/delete/<_id>', methods=['DELETE'])
@jwt_required()
def delete_class(_id):
    try:
        check_user = get_jwt_identity()
        data = ClassRoom.get_class(_id)
        if data:
            if check_user[1] == 'Teacher':
                ClassRoom.delete_class(_id)
                return jsonify({
                    "Message": "class delete successfully"
                }), 200

            return jsonify({
                'Message': "unauthorized to use this function"
            }), 401

        else:
            return jsonify({
                "Message": "Cannot find data by this _id to delete"
            }), 404


    except Exception as e:
        return jsonify({
            "Error": str(e)
        }), 500

