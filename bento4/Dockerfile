# mac M1
#ARG x86_64
#FROM --platform=linux/${arch} ubuntu
#FROM --platform=linux/amd64 ubuntu
FROM ubuntu

RUN mkdir -p /opt/bento4/tmp && mkdir -p /opt/vod/files && mkdir /opt/vod/streams
# Project specific
RUN mkdir /opt/vod/streams/sva
RUN mkdir /opt/vod/streams/sva_dash
RUN mkdir /opt/vod/streams/sva_hls
RUN apt update -y
RUN apt install -y unzip wget python3 curl speedtest-cli
COPY /opt/projects/vod/files/bbb_sunflower_1080p_30fps_stereo_abl.mp4 /opt/vod/files
COPY /opt/projects/vod/files/bbb_sunflower_2160p_60fps_stereo_abl.mp4 /opt/vod/files
WORKDIR /opt/bento4/tmp

RUN wget https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-639.x86_64-unknown-linux.zip
RUN unzip Bento4-SDK-1-6-0-639.x86_64-unknown-linux.zip
RUN cp -r Bento4-SDK-1-6-0-639.x86_64-unknown-linux/* /opt/bento4/
RUN rm -rf /opt/bento4/tmp

WORKDIR /opt/vod/files/


WORKDIR /opt/bento4/bin

# I know the files are not fragmented, don't care, just want to run this start the container and get an nginx in front of it
#RUN ./mp4fragment /opt/vod/files/bbb_sunflower_1080p_30fps_stereo_abl.mp4 /opt/vod/files/bbb_sunflower_1080p_30fps_stereo_abl_frag.mp4
#RUN ./mp4fragment /opt/projects/vod/files/bbb_sunflower_2160p_60fps_stereo_abl.mp4 /opt/projects/vod/files/bbb_sunflower_2160p_60fps_stereo_abl_frag.mp4

#RUN ./mp4dash -o /opt/vod/streams/sva /opt/projects/vod/files/bbb_sunflower_2160p_60fps_stereo_abl_frag.mp4 /opt/vod/files/bbb_sunflower_1080p_30fps_stereo_abl_frag.mp4
# mp4dash video_1000.mp4 video_2000.mp4 video_3000.mp4




# compile ffmpeg as well
# Replace with proper nginx compiled
RUN apt install nginx -y
COPY default /etc/nginx/sites-enabled/.
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]