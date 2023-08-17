from app_config import jsonify,request,Blueprint,jwt_required,get_jwt_identity,create_access_token,create_refresh_token
from app.Models.Students import Students
from app.Models.Class import ClassRoom

auth = Blueprint('auth' , __name__)


@auth.route('/register', methods = ['POST'])
def register():
    try:
        data = request.get_json()
        check_user_exist = Students.students_exist(data['name'])
        check_user = ClassRoom.classroom_exist(data['name'])
        if not check_user_exist or not  check_user:
            access_token = create_access_token(identity=(data['name'] , data['role']))
            refresh_token = create_refresh_token(identity=(data['name'], data['role']))
            return jsonify({
                "Message" : "user added successfully",
                "access_token" : access_token,
                "refresh_token" : refresh_token
            }),200

        return jsonify({
            "Message": "credentails are incorrect"
        }), 401



    except Exception as e:
        return jsonify({
            "Error" : "error occured",
            "Message" : str(e)
        })



@auth.route('/refresh' , methods = ['POST'])
@jwt_required(refresh= True)
def refresh_token():
   try:
       current_user = get_jwt_identity()
       if current_user:
           access_token = create_access_token(identity=current_user)
           return jsonify({
               "access_token": access_token
           }), 200

       return jsonify({
           "Message" : "Invalid credentials"
       }),401

   except Exception as e:
       return jsonify({
           "ERROR" : "error occured",
           "Message" : str(e)
       }),200



@auth.route('/login', methods = ['POST'])
@jwt_required()
def login():
    try:
        data = request.get_json()
        check_data = Students.students_exist(data['name'])
        check_user = ClassRoom.classroom_exist(data['name'])
        if check_data or check_user:
            access_token = create_access_token(identity=(data['name'], data['role']))
            refresh_token = create_refresh_token(identity=(data['name'], data['role']))
            return jsonify({
                "Message": "Login successfully",
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200

        else:
            return jsonify({
                "Message": "credentails are incorrect"
            }), 401

    except Exception as e:
        return jsonify({
            "message": "Error occured", "Error": str(e)
        }), 500


