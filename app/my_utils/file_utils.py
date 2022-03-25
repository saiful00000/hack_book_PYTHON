from fileinput import filename
from datetime import datetime
import os
from typing import Dict

from fastapi import File, UploadFile


def save_profile_picture(profile_picture: UploadFile, user_id: str) -> Dict:
    try:
        os.mkdir("profile_pictures")
        print(f"current directory = {os.getcwd()}")
    except Exception as e:
        print(f"Exception 1 : {e}")

    file_name = user_id + profile_picture.filename

    file_path = f"{os.getcwd()}/profile_pictures/{file_name}"

    with open(file_path, "wb+") as fl:
        fl.write(profile_picture.file.read())
        fl.close()

    return {"file_name": file_name, "file_path": file_path}
