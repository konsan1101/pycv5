@ECHO Off

ECHO ffmpeg -list_devices true -f dshow -i dummy
     ffmpeg -list_devices true -f dshow -i dummy

pause

ECHO ffmpeg -f dshow -i video="Microsoft Camera Rear" temp_video.mkv
     ffmpeg -f dshow -i video="Microsoft Camera Rear" temp_video.mkv

pause
