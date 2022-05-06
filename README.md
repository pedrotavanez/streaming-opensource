# Bento4

* FMMPEG used for resizing/rescalling
* Bento4 used for packaging mp4 to HLS/DASH streams
* Nginx serves the files and provides complete JSON log with headers

# Docker

Inside docker there are 2 directories
encoder :
Uses nginx-rtmp module, receives an RTMP stream and then using exec directives launches ffmpeg to build the different profiles.


Current issues:
* Dash manifests is not stable and it's not passing Dash validator
