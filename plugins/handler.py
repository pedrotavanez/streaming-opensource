#!/usr/bin/env python3
from plugin_nginx_rtmp import ENCODER
extra_args = {
    "nginx_host": "localhost",
    "nginx_port": "8888",
    "nginx_proto": "http",
    "nginx_stats_path": "stat",
    "apps_mapping": {
        "encoder": {"name":"Encoder", "paths":["0c68c467"],
    }},  #"hls": {"name":"HLS Transcoder", "paths":[]}, "dash": {"name":"DASH Transcoder", "paths":[]}}}
    "app": "tsd",
    "env": "static",
    "ts_static_headers": {
        "X-TS-ID": "9e37d623-8875-43f1-85fc-d1f4fba7",
        "Authorization": "Bearer d83059fc39d4423eb3b0d9f02a07edf0",
        "Content-Type": "application/json",
    },
}
def handler(options):
    nginx = ENCODER(options)
    rtmp_stats = nginx.request_data()
    ts_json = nginx.parse_data(rtmp_stats)
    result=nginx.post_ts(ts_json)
    return result
handler(extra_args)