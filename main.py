"""
Launching process :
pip install fastapi uvicorn[standard]
save code as main.py
start the app using : uvicorn main:app --reload
go to : http://localhost:8000/

informations go to : http://localhost:8000/docs#/

access to specific file : http://localhost:8000/files/toto/tata/titi.txt
"""



from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import os
import shutil
from starlette.responses import FileResponse


# Create new FastAPI app
app = FastAPI (debug=True)

# Create User class to manage users
class User (BaseModel) :
	username : str
	password : str


security = HTTPBasic ()

def get_current_user (credentials : HTTPBasicCredentials = Depends(security)) :
	root_user = "ArnoSG"
	root_password = "Arno_SG"

	"""
	# Can be done like this
	if credentials.username != root_user :
		raise HTTPException (status_code = HTTP_401_UNAUTHORIZED, detail = "Wrong Username")
	elif credentials.password != root_password :
		raise HTTPException (status_code = HTTP_401_UNAUTHORIZED, detail = "Wrong Password")
	else : 
		pass
	"""

	# But we prefer like this to avoid giving too much informations to a potential hacker
	if credentials.username != root_user or credentials.password != root_password :
		raise HTTPException (status_code = status.HTTP_401_UNAUTHORIZED, detail = "Wrong Username or Password")

	return credentials.username

@app.post ("/user/signup")
def create_user (user : User) :
	# Writing in the secret file
	with open ("secret.txt", "a") as f :
		f.write (f"{user.username}:{user.password}\n")

	return {"message" : "User created successfully !"}

@app.get ("/user/whoami")
def whoami (current_user : str = Depends (get_current_user)) :
	return {"username" : current_user, "password" : "Arno_SG"}

@app.put ("/files/{filename:path}")
def create_file (filename : str, file : UploadFile = File (...), current_user : str = Depends (get_current_user)) :
	path = os.path.join (current_user, filename)

	with open (path, "wb") as f :
		shutil.copyfileobj (file.file, f)

	return {"message" : f"{filename} created successfully !"}

@app.delete ("/files/{filename:path}")
def delete_file (filename : str, current_user : str = Depends (get_current_user)) :
	path = os.path.join (current_user, filename)

	if os.path.exists (path) :
		os.remove (path)
		return {"message" : f"{filename} deleted successfully !"}
	else :
		raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = "File not found !")

@app.get ("/files/{filename:path}")
def get_file (filename : str, current_user : str = Depends (get_current_user)) :
	path = os.path.join (current_user, filename)

	if os.path.exists (path) :
		return FileResponse (path)
	else :
		raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = "File not found !")

"""
@app.get("/files/{prefix:path}")
def get_files(prefix: str, current_user: str = Depends(get_current_user)):
    files = []
    path = os.path.join(current_user, prefix)
    if os.path.isdir(path):
        for root, dirnames, filenames in os.walk(path):
            for filename in filenames:
                files.append(os.path.relpath(os.path.join(root, filename), current_user))
        return {"files": files}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prefix not found or not a directory!")
"""
@app.get("/files/{prefix:path}")
def get_files(prefix: str, current_user: str = Depends(get_current_user)):
    files = []
    current_dir = os.getcwd()  # get current working directory
    user_dir = os.path.join(current_dir, current_user)
    prefix_path = os.path.join(user_dir, prefix)

    if os.path.isdir(user_dir) and os.path.isdir(prefix_path):
        for root, dirnames, filenames in os.walk(prefix_path):
            for filename in filenames:
                files.append(os.path.relpath(os.path.join(root, filename), user_dir))
        return {"files": files}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prefix not found or not a directory!")
