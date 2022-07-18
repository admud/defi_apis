
from __future__ import print_function
import pickle

# import os.path, os.listdir
import os
import io
import shutil
import requests
from typing import List
from mimetypes import MimeTypes
from dateutil.parser import parse
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from apiclient import errors


global SCOPES
SCOPES = ["https://www.googleapis.com/auth/drive"]

def __init__(self,apikey):
        path = os.path.expanduser("~/google_pickle")
        with open(path, "rb") as token:
            self.creds = pickle.load(token)

        # Connect to the API service
        self.service = build("drive", "v3", credentials=self.creds)


def GoogleFileUpload(self, filepath: str, folderid: str) -> None:
        
    name = filepath.split("/")[-1]

    mimetype = MimeTypes().guess_type(name)[0]

    file_metadata = {"name": name, "parents": [folderid]}
    try:
        media = MediaFileUpload(filepath, mimetype=mimetype)
        file = (
            self.service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id",
            )
            .execute()
        )
        print(f"{filepath} Uploaded.")

    except Exception as e:
        print(e)
        raise Exception("Can't Upload File.")


def update_file(self, file_id, new_title, new_description, new_mime_type, new_filename, new_revision,folderid):
        """Update an existing file's metadata and content.

        Args:
            service: Drive API service instance.
            file_id: ID of the file to update.
            new_title: New title for the file.
            new_description: New description for the file.
            new_mime_type: New MIME type for the file.
            new_filename: Filename of the new content to upload.
            new_revision: Whether or not to create a new revision for this file.
        Returns:
            Updated file metadata if successful, None otherwise.
        """
        name = file_id
        file_metadata = {"name": name, "parents": [folderid]}
        try:
            # First retrieve the file from the API.
            file = self.service.files().get(fileId=file_id).execute()

            # File's new metadata.
            file['title'] = new_title
            file['description'] = new_description
            file['mimeType'] = new_mime_type

            # File's new content.
            media_body = MediaFileUpload(
                new_filename, mimetype=new_mime_type, resumable=True)

            return self.files().update(fileId=file_id, body=file_metadata, newRevision=new_revision, media_body=media_body).execute()

        except errors.HttpError as error:
            print(f"An error occurred: {error}")
            return None

def delete_gfile(self,filepath,folderid):
    file_id = self.get_fileid(filepath,folderid)
    try:
        self.service.files().delete(fileId=file_id).execute()
    except Exception as e:
        print(e)