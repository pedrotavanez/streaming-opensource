#!/usr/bin/env python3
import requests
import xmltodict
import xml
import json
import logging

log = logging.getLogger()


def requester(method,url, headers=None, auth=None, data=None):
    return_message = {}
    if type(data) == dict:
        datas = json.dumps(data)
    else:
        datas = data
    try:
        r = requests.request(method, url, headers=headers, auth=None, data=datas)
        r.raise_for_status()
        print(r.status_code)
        print(r.url)
        print(r.text)
        return_message["status"] = r.status_code
        return_message["data"] = None
        if method == "get":
            try:
                rtmp_dict = xmltodict.parse(r.text)
            except xml.parsers.expat.ExpatError as e:
                log.warning(f"XML Error: {r.text}")
                log.warning(e)
                return {"status_code": r.status_code, "message": r.text, "url": r.url}
            if "touchstream.global" in url:
                return {"status_code": r.status_code, "message": r.text, "url": r.url}
            return_message["data"] = rtmp_dict
        elif method == "post":
            try:
                response = json.loads(r.text)
            except json.decoder.JSONDecodeError as e:
                log.warning(f"JSON Error: {r.text}")
                log.warning(e)
                return {"status_code": r.status_code, "message": r.text, "url": r.url}
            if (
                r.status_code == 200
                and "errors" in response
                and response["errors"] != []
            ):
                log.warning(r.status_code)
                log.warning(f"Error posting: {r.text}")
                return {"status_code": r.status_code, "message": r.text, "url": r.url}
    except requests.exceptions.HTTPError as e:
        log.warning(f"Status Code: {r.status_code}")
        log.warning(f"Message: {r.text}")
        log.warning(e)
        return {"status_code": r.status_code, "message": r.text, "url": r.url}
    return return_message["data"]["rtmp"]["server"]["application"]
