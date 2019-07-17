start "rec" vlc screen:// :screen-fps=5 --sout=#transcode{vcodec=h264,acodec=none}:standard{access=file,mux=mp4,dst=TEST.FLV}

ping localhost -w 1000 -n 10 >nul

TASKKILL /IM VLC.EXE

PAUSE


