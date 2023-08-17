from mongoengine import Document,StringField,DateTimeField,DateField,ListField,DictField
from flask import json,jsonify,request
from bson.objectid import ObjectId


class Students(Document):
    _id = StringField()
    name = StringField(min_length= 3, max_length=20, required=True)
    Last_name = StringField(min_length=3 , max_length= 20, required= True)
    DOB = DateField(required=True)
    role = StringField()
    class_assigned = ListField(StringField())

    def to_json(self):
        {
            self._id,
            self.name,
            self.Last_name,
            self.DOB,
            self.role,
            self.class_assigned
        }


    @classmethod
    def add_students(cls):
        data = request.get_json()
        data = Students(
            name=data['name'],
            Last_name=data['Last_name'],
            DOB=data['DOB'],
            role = 'student'
        )
        data.save()


    @classmethod
    def get_students(cls, _id):
        students_exist = cls.objects(_id=ObjectId(_id))
        if students_exist:
            data = json.dumps(students_exist)
            return data

        return None


    @classmethod
    def update_students(cls, _id):
        data = cls.objects(_id= ObjectId(_id))
        if data:
            body = request.get_json()
            data.update(**body)

        return None


    @classmethod
    def delete_students(cls, _id):
        data =  cls.objects( _id = ObjectId(_id))
        if data:
            data.delete()
        return None


    @classmethod
    def students_exist(cls, name):
        data = cls.objects(name__contains=name)
        if data:
            serialised = json.dumps(data)
            return serialised

        return None






