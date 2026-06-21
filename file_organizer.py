import os
import shutil

source_folder = "Downloads"

file_types = {
    "Images": [".jpg", ".png", ".jpeg"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv"],
}

for file in os.listdir(source_folder):

    file_path = os.path.join(source_folder, file)

    if os.path.isfile(file_path):

        ext = os.path.splitext(file)[1].lower()

        for folder, extensions in file_types.items():

            if ext in extensions:

                destination = os.path.join(source_folder, folder)

                os.makedirs(destination, exist_ok=True)

                shutil.move(
                    file_path,
                    os.path.join(destination, file)
                )

                print(f"Moved {file} -> {folder}")