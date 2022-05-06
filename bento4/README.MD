Dockerfile not working on mac M1

Ubuntu is good

Check if mp4 is fragmented or not - Preferably the encoder should do it (ffmpeg)

bin/.mp4info <file>

If it's not fragmented:
bin/./mp4fragment <normal_file>.mp4 <fragmented_file>.mp4

bin/./mp4fragment videos/bbb/sva_1080p_30fps_normal.mp4 videos/bbb/sva_1080p_30fps_fragmented.mp4

bin/./mp4dash <file_4kp>.mp4 <file_1080p> <file_720> 

./mp4dash -o /opt/vod/streams/sva  /opt/vod/files/bbb_sunflower_1080p_30fps_stereo_abl_frag.mp4
