from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser

from cdn.models import File
from home_user.models import User

from common.utils import get_or_none

from home_server import settings

class UploadView(APIView):
    
    parser_classes = (FileUploadParser,)

    def put(self, request : Request, filename=""):
        '''
        Upload API for manual user upload

        Route: [PUT] /cdn/upload/:filename

        # Request Body
        - file: File to upload
        '''
        # Uploaded file
        file = request.FILES.get("file")

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
        elif filename == "":
            return Response(
                data={
                    "success": "fail",
                    "message": "filename not found"
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        # Validate file type is valid media type
        elif file.content_type.lower() not in settings.MEDIA_MIMETYPES:
            return Response(
                data={
                    "success": "fail",
                    "message": "file type not allowed"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Make entry in DB
        file = File(
            file_name=".".join(filename.split(".")[0:-1]),
            file_ext=filename.split(".")[-1],
            uploaded_by=request.user,
        )
        file.save()

        # Upload 
        f = open(f"{settings.MEDIAROOT}/{filename}", "wb")
        f.write(file.read())
        f.close()

        # Return
        return Response(
            data={
                "success": "success",
                "message": "user logged out"
            }, 
            status=status.HTTP_200_OK
        )