import os
import zipfile

def zip_directory(folder_path, zip_name):
    zip_path = os.path.join(folder_path, f"{zip_name}.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".mp3"):
                    zipf.write(os.path.join(root, file), file)
    return zip_path
