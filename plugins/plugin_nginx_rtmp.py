#!/usr/bin/env python3
import requests

# import json
import simplejson as json
from pprint import pprint
from xmljson import yahoo as bf
from xml.etree.ElementTree import fromstring, tostring
import xmljson
import subprocess
import xmltodict
import math
import datetime

# Setup Nginx host & port & proto
nginx_host = ""
nginx_port = ""
nginx_proto = "http"
nginx_stats_path = "/stat"
# NGINX RTMP Stats URL and config
nginx_stats = f"{nginx_proto}://{nginx_host}:{nginx_port}/{nginx_stats_path}"

# If using same box for encode / transcode, otherwise, comment HLS/DASH
nginx_e2e_mapping = {
    "apps": {"Encoder": "encoder", "HLS Transcoder": "hls", "DASH Transcoder": "dash"}
}

def bytesto(bytes, to, bsize=1024):
    a = {"k": 1, "m": 2, "g": 3, "t": 4, "p": 5, "e": 6}
    r = float(bytes)
    return bytes / (bsize ** a[to])


def convertXML2JSON(message):
    xpars = xmltodict.parse(message)
    data = json.dumps(xpars)
    nginx_data = json.loads(data)["rtmp"]
    return nginx_data


def extractKPIS(nginx_data):
    nginx_kpi_dict = {}
    nginx_kpi_dict["info"] = []
    nginx_kpi_dict["kpis"] = {}
    info_dict = {}
    for info in nginx_data:
        # Useful data is under key "server"
        # print(info)
        info_dict[info] = nginx_data[info]

        # print(f"#\nkey: {info} - Value: {nginx_data[info]}\n#")
        if info == "server":
            # print("********")
            print("Details")
            # print(nginx_data["server"]["application"])
            # print(len(nginx_data["server"]["application"]))
            for app in nginx_data["server"]["application"]:
                # print(app)
                if app["name"] in nginx_e2e_mapping["apps"].values():
                    print(f"Found 1 app in mapping: {app['name']}")
                    nginx_kpi_dict["kpis"][app["name"]] = {}
                    # print(app.keys())
                    # print(app['live'].keys())
                    # print("Full Detail - stream")
                    # print(f"nclients-{app['name']}:{app['live']['nclients']}")
                    nginx_kpi_dict["kpis"][app["name"]]["profiles"] = app["live"][
                        "nclients"
                    ]
                    print(app["live"])
    print("INFO")
    # pprint(info_dict)
    print("TEST DEBUG")
    print(nginx_e2e_mapping["apps"])
    print(nginx_kpi_dict["kpis"])

    # pprint(nginx_kpi_dict)


def request_data():
    return_message = {}
    # Note: No Authentication needed for the example
    r = requests.get(nginx_stats)
    return_message["status"] = r.status_code
    return_message["data"] = None
    if return_message["status"] == 200:
        response = r.text
        # New and untested
        #data_json = convertXML2JSON(response)
        # Process response into a dictionary
        rtmp_dict = xmltodict.parse(response)
        return_message["data"] = rtmp_dict
    else:
        return_message["error"] = "Error parsing data, dumping response in 'data'"
        return_message["data"] = r.text
    return return_message


def transform_data():
    rtmp_stats = request_data()
    pprint(rtmp_stats)


extractKPIS()
