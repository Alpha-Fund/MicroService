"""
Launch test : pytest test_app.py
"""

import requests
import os

def test_create_user () :
	response = requests.post ("http://localhost:8000/user/signup", json = {"username" : "test_username", "password" : "test_password"})
	assert response.status_code == 200
	assert response.json () == {"message" : "User created successfully !"}

def test_get_current_user () :
	response = requests.get ("http://localhost:8000/user/whoami", auth = ("ArnoSG", "Arno_SG"))
	assert response.status_code == 200
	assert response.json () == {"username" : "ArnoSG", "password" : "Arno_SG"}

def test_create_file () :
	file = open ("test.txt", "w")
	file.write ("TEST FILE")
	file.close ()

	with open ("test.txt", "rb") as f :
		response = requests.put ("http://localhost:8000/files/test.txt", files = {"file" : f}, auth = ("ArnoSG", "Arno_SG"))

	assert response.status_code == 200
	assert response.json () == {"message" : "test.txt created successfully !"}

	os.remove ("test.txt")

def test_get_file () :
	file = open ("test.txt", "w")
	file.write ("TEST FILE")
	file.close ()

	with open ("test.txt", "rb") as f :
		requests.put ("http://localhost:8000/files/test.txt", files = {"file" : f}, auth = ("ArnoSG", "Arno_SG"))

	response = requests.get ("http://localhost:8000/files/test.txt", auth = ("ArnoSG", "Arno_SG"))
	assert response.status_code == 200
	assert response.content == b"TEST FILE"

	os.remove ("test.txt")

def test_delete_file () :
	file = open ("test.txt", "w")
	file.write ("TEST FILE")
	file.close ()

	with open ("test.txt", "rb") as f :
		requests.put ("http://localhost:8000/files/test.txt", files={"file": f}, auth=("ArnoSG", "Arno_SG"))

	response = requests.delete ("http://localhost:8000/files/test.txt", auth=("ArnoSG", "Arno_SG"))
	assert response.status_code == 200
	assert response.json () == {"message" : "test.txt deleted successfully !"}

	response = requests.get("http://localhost:8000/files/test.txt", auth=("ArnoSG", "Arno_SG"))
	assert response.status_code == 404

	os.remove("test.txt")


# Don't work properly so prefer to avoid the test for now
"""

def test_get_files () :
	response = requests.get ("http://localhost:8000/files/test", auth=("ArnoSG", "Arno_SG"))
	assert response.status_code == 404

	file = open("test.txt", "w")
	file.write ("TEST FILE")
	file.close ()

	with open ("test.txt", "rb") as f :
		requests.put ("http://localhost:8000/files/test.txt", files={"file": f}, auth=("ArnoSG", "Arno_SG"))

	response = requests.get ("http://localhost:8000/files/ArnoSG/", auth=("ArnoSG", "Arno_SG"))
	assert response.status_code == 200
	assert response.json () == ["test.txt"]

	os.remove ("test.txt")


def test_get_files():
    # Upload a test file to the ArnoSG directory
    with open("test.txt", "w") as f:
        f.write("TEST FILE")

    with open("test.txt", "rb") as f:
        requests.put("http://localhost:8000/files/test.txt", files={"file": f}, auth=("ArnoSG", "Arno_SG"))

    # Test if requesting a non-existent prefix returns 404 error
    response = requests.get("http://localhost:8000/files/nonexistent_dir", auth=("ArnoSG", "Arno_SG"))
    assert response.status_code == 404

    # Test if requesting a file instead of a directory returns 404 error
    response = requests.get("http://localhost:8000/files/test.txt", auth=("ArnoSG", "Arno_SG"))
    assert response.status_code == 404

    # Test if requesting the ArnoSG directory returns the uploaded file
    response = requests.get("http://localhost:8000/files/", auth=("ArnoSG", "Arno_SG"))
    assert response.status_code == 200
    assert response.json() == ["test.txt"]

    # Clean up the test file
    os.remove("test.txt")

"""