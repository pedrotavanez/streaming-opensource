#!/usr/bin/env python3
from helpers.create_metric import create_metric
from helpers.convert import convert
from helpers.request import requester
from helpers.create_mg import create_mg
from pprint import pprint
import logging

log = logging.getLogger()

class ENCODER:
    def __init__(self, options):
        self.nginx_host = options["nginx_host"]
        self.nginx_port = options["nginx_port"]
        self.nginx_proto = options["nginx_proto"]
        self.nginx_stats_path = options["nginx_stats_path"]
        self.apps_mapping = options["apps_mapping"]
        self.host = options["app"]
        self.ts_host = f"https://{self.host}.touchstream.global"
        self.env = options["env"]
        self.ts_headers = options["ts_" + str(self.env) + "_headers"]
        self.ts_json={}

    def request_data(self):
        # Note: No Authentication needed for the example
        self.nginx_stats = f"{self.nginx_proto}://{self.nginx_host}:{self.nginx_port}/{self.nginx_stats_path}"
        result=requester(self.nginx_stats, "get")
        return result

    def parse_data(self, nginx_data):
        for app in nginx_data:
            if app["name"] in self.apps_mapping.keys():

                audio_data = app["live"]["stream"]["meta"]["audio"]
                video_data = app["live"]["stream"]["meta"]["video"]

                profiles = create_metric(app["live"]["nclients"], "nclients")
                v_codec = create_metric(
                    f"{video_data['codec']} {video_data['profile']} {video_data['level']}",
                    "Video Codec",
                )
                v_bits_s = create_metric(
                    convert(app["live"]["stream"]["bw_video"]), "Video bits/s", True
                )
                v_size = create_metric(
                    f"{video_data['width']}x{video_data['height']}", "Video Size"
                )
                v_fps = create_metric(f"{video_data['frame_rate']}", "Video FPS")
                a_codec = create_metric(
                    f"{audio_data['codec']} {audio_data['profile']}", "Audio Codec"
                )
                a_bits_s = create_metric(
                    convert(app["live"]["stream"]["bw_audio"]), "Audio bits/s", True
                )
                a_freq = create_metric(f"{video_data['frame_rate']}", "Audio Freq")
                a_chan = create_metric(f"{audio_data['channels']}", "Audio Channels")
                by_in = create_metric(
                    convert(app["live"]["stream"]["bytes_in"]), "In bytes", True
                )
                by_out = create_metric(
                    convert(app["live"]["stream"]["bytes_out"]), "Out bytes", True
                )
                bw_in = create_metric(
                    convert(app["live"]["stream"]["bw_in"]), "In bits/s", True
                )
                bw_out = create_metric(convert(app["live"]["stream"]["bw_out"]), "Out bits/s", True)

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
                self.build_ts_json(mg_dict, self.apps_mapping[app["name"]])
        print("TS_JSON")
        pprint(self.ts_json)
        return self.ts_json

    def build_ts_json(self, mg_dict, app_map):
        paths=app_map["paths"]
        for path in paths:
            channel=path.split(".")[0]
            if channel not in self.ts_json:
                self.ts_json[channel]={}
            if path not in self.ts_json[channel]:
                self.ts_json[channel][path]=[]
            self.ts_json[channel][path].append(mg_dict)

    def post_ts(self, ts_json):
        url=self.ts_host + "/api/rest/e2eMetrics/"
        result=requester(url, "post", headers=self.ts_headers)
        pprint(result)
        return result