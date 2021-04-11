import unittest
import requests
import json


class TestMain(unittest.TestCase):

    # Fetch the data

    def testcase1(self):
        # Get the response when try to fetch data from database. Should return response 200
        api = "http://127.0.0.1:8000/"
        get_url = "{}/get/Song".format(api)
        result = requests.get(get_url)
        self.assertEqual(result.status_code, 200)

    def testcase2(self):
        # If file id is invalid, should return response 400
        api = "http://127.0.0.1:8000/"
        get_url = "{}/get/Song/49281".format(api)
        result = requests.get(get_url)
        self.assertEqual(result.status_code, 400)

    def testcase3(self):
        # If filetype is not in database, should return response 400
        api = "http://127.0.0.1:8000/"
        get_url = "{}/get/audio".format(api)
        result = requests.get(get_url)
        self.assertEqual(result.status_code, 400)

    def testcase4(self):
        # If filetype and id is valid, should return response 200
        api = "http://127.0.0.1:8000/"
        get_url = "{}/get/Song/6071992e701dbf6bf0b90bcf".format(api)
        result = requests.get(get_url)
        self.assertEqual(result.status_code, 200)

    # Add data to the database

    def testcase5(self):
        # If not a valid format or keys are missing, should return response 400
        data = json.dumps({"audioFileType": "audio"})
        headers = {"content-type": "application/json"}
        api = "http://127.0.0.1:8000/"
        add_url = "{}/add".format(api)
        result = requests.post(url=add_url, data=data, headers=headers)
        self.assertEqual(result.status_code, 400)

    def testcase6(self):
        # If the file doesn't has all the fields, should return response 400
        data = json.dumps({"audioFileType": "Song",
                           "audioFileMetadata": {
                               "name": 10
                           }})  # duration is not there
        headers = {"content-type": "application/json"}
        api = "http://127.0.0.1:8000/"
        add_url = "{}/add".format(api)
        result = requests.post(url=add_url, data=data, headers=headers)
        self.assertEqual(result.status_code, 400)

    def testcase7(self):
        # If any of the fields are not of the required type, should have a ValueError & return response 500
        data = json.dumps({"audioFileType": "Song",
                           "audioFileMetadata": {
                               "name": 10,  # int type, should be be a string
                               "duration": 90
                           }})
        headers = {"content-type": "application/json"}
        api = "http://127.0.0.1:8000/"
        add_url = "{}/add".format(api)
        result = requests.post(url=add_url, data=data, headers=headers)
        self.assertEqual(result.status_code, 500)

    def testcase8(self):
        # If all the inputs are correct, should return response 200
        data = json.dumps({"audioFileType": "Song",
                           "audioFileMetadata": {
                               "name": "ok",
                               "duration": 90
                           }})
        headers = {"content-type": "application/json"}
        api = "http://127.0.0.1:8000/"
        add_url = "{}/add".format(api)
        result = requests.post(url=add_url, data=data, headers=headers)
        self.assertEqual(result.status_code, 200)

    # Update data

    def testcase9(self):
        # If not a valid filetype, should return response 400
        data = json.dumps({"audioFileType": "Audio",  # not a valid filetype for the database
                           "audioFileMetadata": {
                               "title": "ok"
                           }})
        headers = {"content-type": "application/json"}
        api = "http://127.0.0.1:8000/"
        add_url = "{}/update/Audiobook/607041bd56c943d3f520eb26".format(api)
        result = requests.put(url=add_url, data=data, headers=headers)
        self.assertEqual(result.status_code, 400)

    def testcase10(self):
        # If inputs are not of required type, should have a ValueError & return response 500
        data = json.dumps({"audioFileType": "Audiobook",
                           "audioFileMetadata": {
                               "title": 123,  # int type, should be a string
                               "duration": "ok"
                           }})
        headers = {"content-type": "application/json"}
        api = "http://127.0.0.1:8000/"
        add_url = "{}/update/Audiobook/607041bd56c943d3f520eb26".format(api)
        result = requests.put(url=add_url, data=data, headers=headers)
        self.assertEqual(result.status_code, 500)

    def testcase11(self):
        # If everything goes well, should return response 200
        data = json.dumps({"audioFileType": "Audiobook",
                           "audioFileMetadata": {
                               "title": "ok",
                               "author": "abc",
                               "duration": 1000
                           }})
        headers = {"content-type": "application/json"}
        api = "http://127.0.0.1:8000/"
        add_url = "{}/update/Audiobook/607041bd56c943d3f520eb26".format(api)
        result = requests.put(url=add_url, data=data, headers=headers)
        self.assertEqual(result.status_code, 200)

    # Delete data

    def testcase12(self):
        # If not a valid filetype, should return response 400
        headers = {"content-type": "application/json"}
        api = "http://127.0.0.1:8000/"
        add_url = "{}/delete/Audio/60729c689a3348db05aac5c7".format(api)  # not a valid filetype for the database
        result = requests.delete(url=add_url, headers=headers)
        self.assertEqual(result.status_code, 400)

    def testcase13(self):
        # If not a valid key, should return response 400
        headers = {"content-type": "application/json"}
        api = "http://127.0.0.1:8000/"
        add_url = "{}/delete/Song/4900352235".format(api)  # not a valid key
        result = requests.delete(url=add_url, headers=headers)
        self.assertEqual(result.status_code, 400)

    def testcase14(self):
        # If a valid filetype with the valid key, should delete the data & return response 200
        headers = {"content-type": "application/json"}
        api = "http://127.0.0.1:8000/"
        add_url = "{}/delete/Song/60729c689a3348db05aac5c7".format(api)
        result = requests.delete(url=add_url, headers=headers)
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
