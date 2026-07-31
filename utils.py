from fastapi import UploadFile
import shutil 
import os

def _save_file_to_server(uploaded_file: UploadFile, path: str = "./", save_as: str | None = None) -> str:
    filename = uploaded_file.filename or "upload"
    extension = os.path.splitext(filename)[-1]
    if save_as is None:
        save_as = os.path.splitext(filename)[0] or "upload"

    save_as_stem, save_as_ext = os.path.splitext(save_as)
    if not save_as_ext:
        save_as_ext = extension

    temp_file = os.path.join(path, save_as_stem + save_as_ext)

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    return temp_file