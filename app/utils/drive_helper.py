from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from flask import current_app
import os

class DriveService:
    def __init__(self):
        self.credentials = None
        self.service = None

    def initialize_service(self, token_info):
        """Initialize the Drive service with OAuth2 credentials"""
        self.credentials = Credentials(
            token=token_info.get('access_token'),
            refresh_token=token_info.get('refresh_token'),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=current_app.config['GOOGLE_DRIVE_CLIENT_ID'],
            client_secret=current_app.config['GOOGLE_DRIVE_CLIENT_SECRET'],
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        self.service = build('drive', 'v3', credentials=self.credentials)
        return self.service

    def create_course_folders(self, course_title):
        """Create folders for course content and return folder IDs"""
        if not self.service:
            raise Exception("Drive service not initialized")

        # Create main course folder
        course_folder = self.service.files().create(
            body={
                'name': f'Course: {course_title}',
                'mimeType': 'application/vnd.google-apps.folder'
            },
            fields='id'
        ).execute()

        # Create subfolders for videos and materials
        video_folder = self.service.files().create(
            body={
                'name': 'Videos',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [course_folder.get('id')]
            },
            fields='id'
        ).execute()

        material_folder = self.service.files().create(
            body={
                'name': 'Materials',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [course_folder.get('id')]
            },
            fields='id'
        ).execute()

        return {
            'video_folder_id': video_folder.get('id'),
            'material_folder_id': material_folder.get('id')
        }

    def upload_content(self, file_path, folder_id, content_type):
        """Upload course content and return file ID and viewable link"""
        if not self.service:
            raise Exception("Drive service not initialized")

        file_name = os.path.basename(file_path)
        
        # Set mime type based on content type
        mime_type = {
            'video': 'video/mp4',
            'document': 'application/pdf',
            'tutorial': 'application/pdf'
        }.get(content_type, 'application/octet-stream')

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        media = MediaFileUpload(
            file_path,
            mimetype=mime_type,
            resumable=True
        )

        try:
            # Upload file
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            # Make it viewable by anyone with the link
            self.service.permissions().create(
                fileId=file.get('id'),
                body={
                    'type': 'anyone',
                    'role': 'reader'
                }
            ).execute()

            # Get the webViewLink
            file = self.service.files().get(
                fileId=file.get('id'),
                fields='webViewLink'
            ).execute()

            return {
                'file_id': file.get('id'),
                'view_link': file.get('webViewLink')
            }

        except Exception as e:
            current_app.logger.error(f"Error uploading to Drive: {str(e)}")
            raise

drive_service = DriveService()
