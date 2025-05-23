import os

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser

from cdn.models import File, Folder

from common.utils import get_media_types, get_or_none

from django.conf import settings

class UploadView(APIView):
    
    parser_classes = (FileUploadParser,)

    # Upload File
    def put(self, request : Request, filepath=""):
        '''
        Upload API for manual user upload

        Route: [PUT] /cdn/upload/:filepath

        # Request Path
        - filepath: Location to upload the file to

        # Request Body
        - file: File to upload
        '''
        # Override Flag
        override = request.query_params.get("override", "0") == "1"

        # Uploaded file
        file = request.FILES.get("file")

        # Grab Valid Media Types
        media_type, _ = get_media_types()

        # Validate file exists
        if file is None:
            return Response(
                data={
                    "success": "fail",
                    "message": "file not found"
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        # Validate file name is not empty
        elif filepath == "" or filepath == ":filepath":
            return Response(
                data={
                    "success": "fail",
                    "message": "filepath not provided"
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        # Validate file type is valid media type
        elif file.content_type.lower() not in media_type:
            return Response(
                data={
                    "success": "fail",
                    "message": "file type not allowed"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to make directory entries first
        parent : Folder = None
        for folder in filepath.split("/"):
            try:
                # Attempt to make folder
                root = folder
                if parent is not None:
                    root = f"{parent.path}/{folder}"
                os.mkdir(f"{settings.MEDIA_ROOT}/{root}")

                # Generate Folder object if success
                parent = Folder(parent=parent, name=folder)
                parent.save()
            except FileExistsError:
                # Grab object if already exist (should already exist)
                parent = get_or_none(Folder, parent=parent, name__iexact=folder)
                if parent is None:
                    return Response(
                        data={
                            "success": "fail",
                            "message": "An internal error has occurred during folder query"
                        }, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            except Exception:
                return Response(
                    data={
                        "success": "fail",
                        "message": "An internal error has occurred when generating the folder"
                    }, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Look if already exists
        file_name_chunks = file.name.split(".")
        file_obj, created = File.objects.get_or_create(
            folder=parent,
            file_name=".".join(file_name_chunks[:-1]),
            file_ext=file_name_chunks[-1]
        )

        # Already exist override?
        if not created and not override:
            return Response(
                data={
                    "success": "fail",
                    "message": "File with existing name already exist in that folder; use override query parameter to override"
                }, 
                status=status.HTTP_409_CONFLICT
            )
        
        # Make update in DB
        file_obj.uploaded_by = request.user

        # Upload 
        f = open(f"{settings.MEDIA_ROOT}/{parent.path}/{file.name}", "wb")
        f.write(file.read())
        f.close()

        # Save
        file_obj.save()

        # Return
        return Response(
            data={
                "success": "success",
                "message": "file %s uploaded successfully" % filepath
            }, 
            status=status.HTTP_200_OK
        )