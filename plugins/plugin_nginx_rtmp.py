#!/usr/bin/env python3
from helpers.create_metric import create_metric
from helpers.convert import convert
from helpers.requester import requester
from helpers.create_mg import create_mg, build_ts_json
from helpers.getE2Epaths import get_e2e_paths, find_paths
import logging
import json
log = logging.getLogger()

class ENCODER:
    def __init__(self, options):
        self.nginx_host = options["nginx_host"]
        self.nginx_port = options["nginx_port"]
        self.nginx_proto = options["nginx_proto"]
        self.nginx_stats_path = options["nginx_stats_path"]
        self.apps_mapping = options["apps_mapping"]
        self.mapping=options["mapping"]
        self.host = options["app"]
        self.ts_host = f"https://{self.host}.touchstream.global"
        self.env = options["env"]
        self.ts_headers = options["ts_" + str(self.env) + "_headers"]
        self.ts_json={}
        self.paths = get_e2e_paths(self.ts_host, self.ts_headers)

    def request_data(self):
        # Note: No Authentication needed for the example
        for nginx_host in self.mapping:
            data=self.obtain_data_set(nginx_host, self.mapping[nginx_host]["port"])
            self.parse_data(data, self.mapping[nginx_host]["touchstream_channel"])
        return self.ts_json

    def obtain_data_set(self, nginx_host, port):
        self.nginx_stats = f"{self.nginx_proto}://{nginx_host}:{port}/{self.nginx_stats_path}"
        result = requester("get",self.nginx_stats)
        return result

    def parse_data(self, nginx_data, touchstream_channel):
        for app in nginx_data:
            if app["name"] in self.apps_mapping.keys():
                if app["name"] in ["hls", "dash","mpd"]:
                    audio_data = app["live"]["stream"][0]["meta"]["audio"]
                    video_data = app["live"]["stream"][0]["meta"]["video"]
                    app_data=app["live"]["stream"][0]
                else:
                    audio_data = app["live"]["stream"]["meta"]["audio"]
                    video_data = app["live"]["stream"]["meta"]["video"]
                    app_data=app["live"]["stream"]

                profiles = create_metric(app["live"]["nclients"], "nclients")
                v_codec = create_metric(
                    f"{video_data['codec']} {video_data['profile']} {video_data['level']}",
                    "Video Codec",
                    type="text"
                )
                v_bits_s = create_metric(
                    convert(app_data["bw_video"]), "Video bits/s", True
                )
                v_size = create_metric(
                    f"{video_data['width']}x{video_data['height']}", "Video Size",type="text"
                )
                v_fps = create_metric(f"{video_data['frame_rate']}", "Video FPS")
                a_codec = create_metric(
                    f"{audio_data['codec']} {audio_data['profile']}", "Audio Codec",type="text"
                )
                a_bits_s = create_metric(
                    convert(app_data["bw_audio"]), "Audio bits/s", True
                )
                a_freq = create_metric(f"{video_data['frame_rate']}", "Audio Freq")
                a_chan = create_metric(f"{audio_data['channels']}", "Audio Channels")
                by_in = create_metric(
                    convert(app_data["bytes_in"]), "In bytes", True
                )
                by_out = create_metric(
                    convert(app_data["bytes_out"]), "Out bytes", True
                )
                bw_in = create_metric(
                    convert(app_data["bw_in"]), "In bits/s", True
                )
                bw_out = create_metric(convert(app_data["bw_out"]), "Out bits/s", True)

                metric_list = [
                    profiles,
                    v_codec,
                    v_bits_s,
                    v_size,
                    v_fps,
                    a_codec,
                    a_bits_s,
                    a_freq,
                    a_chan,
                    by_in,
                    by_out,
                    bw_in,
                    bw_out,
                ]
                mg_dict=create_mg(metric_list, self.apps_mapping[app["name"]]["name"], self.nginx_stats)
                paths=find_paths(self.paths, touchstream_channel)
                self.ts_json=build_ts_json(mg_dict, self.apps_mapping[app["name"]], paths, self.ts_json)
        return self.ts_json

    def post_ts(self, ts_json):
        url=self.ts_host + "/api/rest/e2eMetrics/"
        result=requester("post",url, headers=self.ts_headers, data=json.dumps(ts_json))
        return result