Dockerfile not working on mac M1

Ubuntu is good

Check if mp4 is fragmented or not - Preferably the encoder should do it (ffmpeg)

bin/.mp4info <file>

If it's not fragmented:
bin/./mp4fragment <normal_file>.mp4 <fragmented_file>.mp4

bin/./mp4fragment videos/bbb/sva_1080p_30fps_normal.mp4 videos/bbb/sva_1080p_30fps_fragmented.mp4

bin/./mp4dash <file_4kp>.mp4 <file_1080p> <file_720> 

./mp4dash -o /opt/vod/streams/sva  /opt/vod/files/bbb_sunflower_1080p_30fps_stereo_abl_frag.mp4


#FFMPEG Magic

* MP4 - 1080p

<code>
ffmpeg -i input.mov -preset slow -codec:a libfdk_aac -b:a 128k -codec:v libx264 -pix_fmt yuv420p -b:v 4500k -minrate 4500k -maxrate 9000k -bufsize 9000k -vf scale=-1:1080 output.mp4
</code>

* MP4 - 720p

<code>
ffmpeg -i input.mov -preset slow -codec:a libfdk_aac -b:a 128k -codec:v libx264 -pix_fmt yuv420p -b:v 2500k -minrate 1500k -maxrate 4000k -bufsize 5000k -vf scale=-1:720 output.mp4
</code>

* MP4 - 480p

<code>
ffmpeg -i input.mov -preset slow -codec:a libfdk_aac -b:a 128k -codec:v libx264 -pix_fmt yuv420p -b:v 1000k -minrate 500k -maxrate 2000k -bufsize 2000k -vf scale=-1:480 output.mp4
</code>

* MP4 - 360p

<code>
ffmpeg -i input.mov -preset slow -codec:a libfdk_aac -b:a 128k -codec:v libx264 -pix_fmt yuv420p -b:v 750k -minrate 400k -maxrate 1000k -bufsize 1500k -vf scale=-1:360 output.mp4
</code>