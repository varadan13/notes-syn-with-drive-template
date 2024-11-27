import os
import zipfile
import shutil
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def zip_wikis_folder(parent_folder):
    target_folder_name = 'wikis'
    target_folder_path = os.path.join(parent_folder, target_folder_name)

    if os.path.isdir(target_folder_path):
        zip_file_name = f"{target_folder_path}.zip"

        with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(target_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(
                        file_path, start=target_folder_path)
                    zipf.write(file_path, arcname)

        print(f"Created zip file: {zip_file_name}")
    else:
        print(
            f"The folder '{target_folder_name}' does not exist in '{parent_folder}'.")


def copy_zip_files(source_folder, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)

    for file_name in os.listdir(source_folder):
        if file_name.endswith('.zip'):
            source_file = os.path.join(source_folder, file_name)
            destination_file = os.path.join(destination_folder, file_name)

            try:
                shutil.move(source_file, destination_file)
                print(f"Copied: {file_name} to {destination_folder}")
            except Exception as e:
                print(f"Error copying {file_name}: {e}")


def upload_to_drive(drive, zip_file_path):

    file_list = drive.ListFile(
        {'q': f"title='{os.path.basename(zip_file_path)}' and trashed=false"}).GetList()

    if file_list:
        drive_file = file_list[0]
        drive_file.SetContentFile(zip_file_path)
        drive_file.Upload()
        print(f"Updated existing file: {drive_file['title']}")
    else:
        drive_file = drive.CreateFile(
            {'title': os.path.basename(zip_file_path)})
        drive_file.SetContentFile(zip_file_path)
        drive_file.Upload()
        print(f"Uploaded new file: {drive_file['title']}")
    print(f"Uploaded: {zip_file_path}")


def create_files():
    parent_folder = 'ideas'
    source_folder = "ideas"
    destination_folder = "zips"
    zip_wikis_folder(parent_folder)
    copy_zip_files(source_folder, destination_folder)


def upload():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    for filename in os.listdir('zips'):
        file_path = os.path.join('zips', filename)
        if os.path.isfile(file_path):
            print(f"Uploading: {file_path}")
            upload_to_drive(drive, file_path)


if __name__ == "__main__":
    create_files()
    upload()
