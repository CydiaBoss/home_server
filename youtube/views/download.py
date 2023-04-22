from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from yt_dlp import YoutubeDL

class YTDownloadView(APIView):
    
    # GET YT Video
    def get(self, request : Request):
        '''
        Retrieve YouTube a YT Video

        Route: [GET] 
        '''
        yt_dl = YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

        with yt_dl:
            result = yt_dl.extract_info(
                'http://www.youtube.com/watch?v=BaW_jenozKc',
                download=False, # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        return Response({
            'success': "ok",
            'payload': video
        })