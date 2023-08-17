from mongoengine import Document,StringField,DateTimeField,DateField,ListField,EmbeddedDocument
from flask import json,jsonify,request
from bson.objectid import ObjectId

class ClassRoom(Document):
    _id = StringField()
    name = StringField(max_length=20, required=True)
    Description = StringField(min_length=3 , required= True)
    students_assignment = ListField(StringField())
    role = StringField()


    def to_json(self):
        {
            self._id,
            self.name,
            self.Description,
            self.students_assignment,
            self.role
        }

    @classmethod
    def add_class(cls):
        data = request.get_json()
        form = ClassRoom(
            name=data['name'],
            Description=data['Description'],
            role="Teacher"
        )
        form.save()


    @classmethod
    def get_class(cls, _id):
        class_exist = cls.objects(_id=ObjectId(_id))
        if class_exist:
            data = json.dumps(class_exist)
            return data

        return None


    @classmethod
    def update_class(cls, _id):
        data = cls.objects(_id= ObjectId(_id))
        if data:
            body = request.get_json()
            data.update(**body)

        return None


    @classmethod
    def delete_class(cls, _id):
        data =  cls.objects( _id = ObjectId(_id))
        if data:
            data.delete()

        return None


    @classmethod
    def classroom_exist(cls, name):
        data = cls.objects(name__contains=name)
        if data:
            serialised = json.dumps(data)
            return serialised

        return None

