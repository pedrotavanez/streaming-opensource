#!/usr/bin/env python3
def create_mg(metric_list, mg_name, external_link):
    suff=""
    if mg_name.upper() in ["HLS", "DASH", "MPD"]:
        suff=" Trasnc"
    metric_group_name=f"Nginx {mg_name}{suff}"
    metric_goup={
        metric_group_name: {
            "status": 100,
            "level": 1,
            "inline": True,
            "update_threshold": 10,
            "external_links": [{"name": "Nginx Stats", "url": external_link, "launch_type": "popup"}],
            "metrics": metric_list,
        }
    }
    return metric_goup

def build_ts_json(metric_group, app, paths, ts_json):
    if app.upper() in ["ENCODER", "NGINX ENCODER"]:
        length_of_path=2
    else:
        length_of_path=3
        format=app["name"].upper()
        if format=="DASH":
            format="MPD"
    for path in paths:
        path_s=path.split(".")
        if length_of_path==len(path_s)==2:
            ts_json=add_metric_group(ts_json, path_s[0],path, metric_group)
            return ts_json
        elif length_of_path==len(path_s)==3 and path_s[-1]==format:
            ts_json=add_metric_group(ts_json, path_s[0], path, metric_group)
            return ts_json

def add_metric_group(ts_json, channel_key, path, metric_group):
    if channel_key not in ts_json:
        ts_json[channel_key]={}
    ts_json[channel_key][path]=[metric_group]
    return ts_json