#!/bin/bash

on_die ()
{
    # kill all children
    pkill -KILL -P $$
}

trap 'on_die' TERM
# $1 server
# $2 app
# $3 stream name
ffmpeg -i rtmp://localhost/myapp/$1 -c copy -f flv rtmp://$1/$2/$3 &
wait