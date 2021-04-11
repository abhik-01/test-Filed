from flask import Flask, request, json, Response
from pymongo import MongoClient
from bson.objectid import ObjectId
import uuid
from bson import errors
from mongoengine import *
from datetime import datetime

connection_string = 'mongodb://localhost:27017'  # connection string for the database
connect('test')  # name of the database, connects to the db using Mongoengine
audioFiles = ['Song', 'Podcast', 'Audiobook']  # type of files should be entered to the database

app = Flask(__name__)

try:
    mongo = MongoClient(connection_string)  # connects to the database using Pymongo
    db = mongo.get_database('test')
    collection = db.test1
    mongo.server_info()
except:
    print("can't connect to the database")


# set properties of a song file

class Song:
    def __init__(self, id, name, duration, uploaded_time):
        self._id = id
        self.name = name
        self.duration = duration
        self._uploaded_time = uploaded_time

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if type(value) == str:
            if 0 < len(value) < 100:
                self._name = value
            else:
                raise ValueError('Name cannot be empty or larger than 100.')
        else:
            raise ValueError('Name is not of type string')

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if type(value) == int:
            if value > 0:
                self._duration = f"{value}sec"
            else:
                raise ValueError("Duration cannot be negative")
        else:
            raise ValueError('Duration is not an integer value')

    @property
    def uploaded_time(self):
        return self._uploaded_time


# set properties for a podcast file

class Podcast:
    def __init__(self, id, name, duration, uploaded_time, host, participants=False):
        self._id = id
        self.name = name
        self.duration = duration
        self._uploaded_time = uploaded_time
        self.host = host
        self.participants = participants

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if type(value) == str:
            if 0 < len(value) < 100:
                self._name = value
            else:
                raise ValueError('Name cannot be empty or larger than 100.')
        else:
            raise ValueError('Name is not of type string')

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if type(value) == int:
            if value > 0:
                self._duration = f"{value}sec"
            else:
                raise ValueError("Duration cannot be negative")
        else:
            raise ValueError('Duration is not an integer value')

    @property
    def uploaded_time(self):
        return self._uploaded_time

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        if type(value) == str:
            if 0 < len(value) < 100:
                self._host = value
            else:
                raise ValueError('Host cannot be empty or larger than 100.')
        else:
            raise ValueError('Host is not of type string')

    @property
    def participants(self):
        return self._participants

    @participants.setter
    def participants(self, value):
        if not value:
            pass
        elif type(value) == list and len(value) <= 10:
            for item in value:
                if type(item) == str:
                    if 0 < len(item) < 100:
                        self._participants = value
                    else:
                        raise ValueError('Participant name cannot be empty or larger than 100')
                else:
                    raise ValueError('Participant name is not of type string')
        else:
            raise ValueError('Participants must be type of list and there cannot be more than 10 members')


# set properties for a Audiobook file

class Audiobook:
    def __init__(self, id, title, author, narrator, duration, uploaded_time):
        self._id = id
        self.title = title
        self.author = author
        self.narrator = narrator
        self.duration = duration
        self._uploaded_time = uploaded_time

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if type(value) == str:
            if 0 < len(value) < 100:
                self._title = value
            else:
                raise ValueError('Title cannot be empty or larger than 100.')
        else:
            raise ValueError('Title is not of type string')

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if type(value) == str:
            if 0 < len(value) < 100:
                self._author = value
            else:
                raise ValueError('Author cannot be empty or larger than 100.')
        else:
            raise ValueError('Author is not of type string')

    @property
    def narrator(self):
        return self._narrator

    @narrator.setter
    def narrator(self, value):
        if type(value) == str:
            if 0 < len(value) < 100:
                self._narrator = value
            else:
                raise ValueError('Narrator cannot be empty or larger than 100.')
        else:
            raise ValueError('Narrator is not of type string')

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if type(value) == int:
            if value > 0:
                self._duration = f"{value}sec"
            else:
                raise ValueError("Duration cannot be negative")
        else:
            raise ValueError('Duration is not an integer value')

    @property
    def uploaded_time(self):
        return self._uploaded_time


# property for the string field

class PropertyForString:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if type(value) == str:
            if 0 < len(value) < 100:
                self._name = value
            else:
                raise ValueError('Cannot be empty or larger than 100.')
        else:
            raise ValueError('Not a string value')


# property for the duration field

class Duration:
    def __init__(self, duration):
        self.duration = duration

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if type(value) == int:
            if value > 0:
                self._duration = f"{value}sec"
            else:
                raise ValueError("Cannot be negative")
        else:
            raise ValueError('Not an integer value')


# property for the participants field

class Participants:
    def __init__(self, participants):
        self.participants = participants

    @property
    def participants(self):
        return self._participants

    @participants.setter
    def participants(self, value):
        if type(value) == list and len(value) <= 10:
            for item in value:
                if type(item) == str:
                    if 0 < len(item) < 100:
                        self._participants = value
                    else:
                        raise ValueError('Participant name cannot be empty or larger than 100')
                else:
                    raise ValueError('Participant name is not of type string')
        else:
            raise ValueError('Must be type of list and there cannot be more than 10 members')


# set properties for adding data to the database an

class Create(Document):
    audioFileType = StringField(required=True)
    audioFileMetadata = DictField(required=True)

    meta = {
        "collection": "test1"
    }


# endpoint for adding data

@app.route('/add', methods=['POST'])
def add():
    try:
        audioFileType = request.json['audioFileType']
        audioFileMetadata = request.json['audioFileMetadata']
        if len(audioFileMetadata) >= 2:  # metadata must contain 2 or more fields
            if audioFileType == audioFiles[0]:  # check if it's a song

                # validate the inputs

                validation = Song(id=uuid.uuid4().node,
                                  name=audioFileMetadata['name'],
                                  duration=audioFileMetadata['duration'],
                                  uploaded_time=datetime.utcnow())

                # add entry to the database after validation

                Create(audioFileType=audioFileType,
                       audioFileMetadata=validation.__dict__).save()

            elif audioFileType == audioFiles[1]:  # check if it's a podcast

                # validate the inputs

                validation = Podcast(id=uuid.uuid4().node,
                                     name=audioFileMetadata['name'],
                                     duration=audioFileMetadata['duration'],
                                     uploaded_time=datetime.utcnow(),
                                     host=audioFileMetadata['host'],
                                     participants=audioFileMetadata['participants'])

                # add data to the database after validation

                Create(audioFileType=audioFileType,
                       audioFileMetadata=validation.__dict__).save()

            elif audioFileType == audioFiles[2]:  # check if it's an audiobook

                # validate the inputs

                validation = Audiobook(id=uuid.uuid4().node,
                                       title=audioFileMetadata['title'],
                                       author=audioFileMetadata['author'],
                                       narrator=audioFileMetadata['narrator'],
                                       duration=audioFileMetadata['duration'],
                                       uploaded_time=datetime.utcnow())

                # add data to database after validation

                Create(audioFileType=audioFileType,
                       audioFileMetadata=validation.__dict__).save()

            # if file is not of the above three types
            else:
                return Response(
                    response=json.dumps({"message": "Not a valid filetype"}),
                    status=400,
                    mimetype="application/json"
                )

        # if the mandatory fields are not present
        else:
            return Response(
                response=json.dumps({"message": "Please enter mandatory fields"}),
                status=400,
                mimetype="application/json"
            )
    # if mandatory keys are missing
    except KeyError:
        return Response(
            response=json.dumps({"message": "Please enter valid keys"}),
            status=400,
            mimetype="application/json"
        )
    return json.dumps({"message": "Entry Added"})


# entrypoint for getting data

@app.route('/get/<fileType>/<fileID>', methods=['GET'])
@app.route('/get/<fileType>', methods=['GET'])
def get(fileType, fileID=False):
    try:
        try:
            if fileType in audioFiles:  # check for filetype

                if request.path == f'/get/{fileType}':  # if no key is entered
                    data = list(collection.find({"audioFileType": fileType}))
                    for item in data:
                        item["_id"] = str(item["_id"])
                    return Response(
                        response=json.dumps(data),
                        status=200,
                        mimetype="application/json"
                    )

                elif request.path == f'/get/{fileType}/{fileID}':  # if valid key is entered
                    data = list(collection.find({"audioFileType": fileType,
                                                 "_id": ObjectId(fileID)}))
                    for item in data:
                        item["_id"] = str(item["_id"])
                    return Response(
                        response=json.dumps(data),
                        status=200,
                        mimetype="application/json"
                    )

            # if not a valid filetype
            else:
                return Response(
                    response=json.dumps({"message": "Not a valid filetype"}),
                    status=400,
                    mimetype="application/json"
                )

        # if entered id is not a valid id
        except errors.InvalidId:
            return Response(
                response=json.dumps({"message": "Invalid ID"}),
                status=400,
                mimetype="application/json"
            )

    # if any error occurs while reading the database
    except TypeError:
        return Response(
            response=json.dumps({"message": "can't read database"}),
            status=500,
            mimetype="application/json"
        )


# entrypoint for deleting data

@app.route('/delete/<fileType>/<fileID>', methods=['DELETE'])
def delete(fileType, fileID):
    try:
        try:
            if fileType in audioFiles:  # check for valid filetype
                collection.delete_one({"audioFileType": fileType,
                                       "_id": ObjectId(fileID)})

            else:
                return Response(
                    response=json.dumps({"message": "Not a valid filetype"}),
                    status=400,
                    mimetype="application/json"
                )

        # if not a valid id
        except errors.InvalidId:
            return Response(
                response=json.dumps({"message": "Invalid key"}),
                status=400,
                mimetype="application/json"
            )

    # if the query is not valid
    except TypeError:
        return Response(
            response=json.dumps({"message": "Invalid query"}),
            status=500,
            mimetype="application/json"
        )
    return json.dumps({"message": "Entry deleted"})


# entrypoint for updating data

@app.route('/update/<fileType>/<fileID>', methods=['PUT'])
def update(fileType, fileID):
    try:
        _id = fileID
        audioFileType = request.json['audioFileType']
        audioFileMetadata = request.json['audioFileMetadata']

        # check for valid filetype & the metadata must have at least one element in order to perform update operation

        if fileType and audioFileType in audioFiles and len(audioFileMetadata) >= 1:
            if audioFileType == audioFiles[0]:  # if it's a song

                # check for the field user wants to update

                if 'name' in audioFileMetadata:
                    validation = PropertyForString(name=audioFileMetadata['name'])  # validate the input

                    # update the entry
                    collection.update_one({"_id": ObjectId(_id)},
                                          {"$set": {"audioFileMetadata._name": validation.__dict__['_name']}})

                if 'duration' in audioFileMetadata:
                    validation = Duration(duration=audioFileMetadata['duration'])
                    collection.update_one({"_id": ObjectId(_id)},
                                          {"$set": {"audioFileMetadata._duration": validation.__dict__['_duration']}})

            if audioFileType == audioFiles[1]:  # if it's a podcast

                # check for the field

                if 'name' in audioFileMetadata:
                    validation = PropertyForString(name=audioFileMetadata['name'])
                    collection.update_one({"_id": ObjectId(_id)},
                                          {"$set": {"audioFileMetadata._name": validation.__dict__['_name']}})

                if 'duration' in audioFileMetadata:
                    validation = Duration(duration=audioFileMetadata['duration'])
                    collection.update_one({"_id": ObjectId(_id)},
                                          {"$set": {"audioFileMetadata._duration": validation.__dict__['_duration']}})

                if 'host' in audioFileMetadata:
                    validation = PropertyForString(name=audioFileMetadata['host'])
                    collection.update_one({"_id": ObjectId(_id)},
                                          {"$set": {"audioFileMetadata._host": validation.__dict__['_host']}})

                if 'participants' in audioFileMetadata:
                    validation = Participants(participants=audioFileMetadata['participants']).__dict__['_participants']
                    for item in validation:
                        collection.update_one({"_id": ObjectId(_id)},
                                              {"$push":
                                                   {"audioFileMetadata._participants": item}})

            if audioFileType == audioFiles[2]:  # if it's an audiobook

                # check for the field

                if 'title' in audioFileMetadata:
                    validation = PropertyForString(name=audioFileMetadata['title'])
                    collection.update_one({"_id": ObjectId(_id)},
                                          {"$set": {"audioFileMetadata._title": validation.__dict__['_name']}})

                if 'author' in audioFileMetadata:
                    validation = PropertyForString(name=audioFileMetadata['author'])
                    collection.update_one({"_id": ObjectId(_id)},
                                          {"$set": {"audioFileMetadata._author": validation.__dict__['_name']}})

                if 'narrator' in audioFileMetadata:
                    validation = PropertyForString(name=audioFileMetadata['narrator'])
                    collection.update_one({"_id": ObjectId(_id)},
                                          {"$set": {"audioFileMetadata._narrator": validation.__dict__['_name']}})

                if 'duration' in audioFileMetadata:
                    validation = Duration(duration=audioFileMetadata['duration'])
                    collection.update_one({"_id": ObjectId(_id)},
                                          {"$set": {"audioFileMetadata._duration": validation.__dict__['_duration']}})

        # if not a valid filetype
        else:
            return Response(
                response=json.dumps({"message": "Not a valid filetype"}),
                status=400,
                mimetype="application/json"
            )

    # if invalid keys entered
    except KeyError:
        return Response(
            response=json.dumps({"message": "Please enter valid keys"}),
            status=400,
            mimetype="application/json"
        )

    return json.dumps({"message": "Entry updated"})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
