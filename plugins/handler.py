#!/usr/bin/env python3
from plugin_nginx_rtmp import ENCODER

extra_args = {
    "nginx_host": "localhost",
    "nginx_port": "80",
    "nginx_proto": "http",
    "nginx_stats_path": "stat",
    "apps_mapping": {
        "encoder": {
            "name": "Encoder",
            "paths": ["0c68c467"],
        }
    },  # "hls": {"name":"HLS Transcoder", "paths":[]}, "dash": {"name":"DASH Transcoder", "paths":[]}}}
    "app": "tsd",
    "env": "static",
    "ts_static_headers": {
        "X-TS-ID": "9e37d623-8875-43f1-85fc-d1f4fba7",
        "Authorization": "Bearer d83059fc39d4423eb3b0d9f02a07edf0",
        "Content-Type": "application/json",
    },
}
# This will post to tsd: Demo AWS Events
touchstream = {
    "nginx_host": "3.93.17.52",
    "nginx_port": "8888",
    "nginx_proto": "http",
    "nginx_stats_path": "stat",
    "mapping":{"3.93.17.52":{"touchstream_channel":"Touchstream OpenSource","port":"8888"}},
    "apps_mapping": {
        "encoder": {
            "name": "Encoder",
            "paths": ["9123698ad6432c4d17d577fda2f7063f"],
        },
        "hls": {"name": "HLS Transc", "paths": ["9123698ad6432c4d17d577fda2f7063f.Events.HLS"]},
        "dash": {"name": "DASH Transc", "paths": ["9123698ad6432c4d17d577fda2f7063f.Events.MPD"]},
    },
    "app": "tsd",
    "env": "static",
    "ts_static_headers": {
        "X-TS-ID": "a596052b-7a22-43c2-b384-a6bbf4d3",
        "Authorization": "Bearer 82ff62fee5664b2e80c95eeb0eb969b7",
        "Content-Type": "application/json",
    },
}

def handler(options):
    nginx = ENCODER(options)
    rtmp_stats = nginx.request_data()
    ts_json = nginx.parse_data(rtmp_stats)
    result = nginx.post_ts(ts_json)
    return result

handler(touchstream)