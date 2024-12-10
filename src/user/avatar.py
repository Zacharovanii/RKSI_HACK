import os
from fastapi import UploadFile, File
from fastapi.responses import FileResponse


AVATAR_DIR = "avatars"

async def upload_avatar(user_id: int, file: UploadFile = File(...)):
    if not os.path.exists(AVATAR_DIR):
        os.makedirs(AVATAR_DIR)

    file_path = os.path.join(AVATAR_DIR, f"{user_id}.jpeg")
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    return {"filename": file.filename}

async def get_avatar(user_id: int):
    file_path = os.path.join(AVATAR_DIR, f"{user_id}.jpeg")
    default_avatar_path = os.path.join(AVATAR_DIR, "1.jpeg")

    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse(default_avatar_path)

async def remove_avatar(user_id: int):
    file_path = os.path.join(AVATAR_DIR, f"{user_id}.jpeg")
    default_avatar_path = os.path.join(AVATAR_DIR, "1.jpeg")
    
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"state": 200, "description": "Ваш аватар сброшен до стандартного."}
    else:
        return {"state": 200, "description": "Ваша аватарка стандартная."}
