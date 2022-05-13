#!/usr/bin/env python3
import requests
import xmltodict
import xml
import json
import logging
log=logging.getLogger()

def requester(url, method, headers=None, auth=None, data=None):
    return_message={}
    print(url)
    try:
        r = requests.request(method, url, headers=None, auth=None, data=None)
        r.raise_for_status()
        return_message["status"] = r.status_code
        return_message["data"] = None
        if method=="get":
            try:
                rtmp_dict = xmltodict.parse(r.text)
            except xml.parsers.expat.ExpatError as e:
                log.warning(f"XML Error: {r.text}")
                log.warning(e)
                return {"status_code": r.status_code, "message": r.text, "url": r.url}
            return_message["data"] = rtmp_dict
        elif method=="post":
            try:
                response=json.loads(r.text)
            except json.decoder.JSONDecodeError as e:
                log.warning(f"JSON Error: {r.text}")
                log.warning(e)
                return {"status_code": r.status_code, "message": r.text, "url": r.url}
            if r.status_code==200 and "error" in r.text:
                log.warning(r.status_code)
                log.warning(f"Error posting: {r.text}")
                return {"status_code": r.status_code, "message": r.text, "url": r.url}
    except requests.exceptions.HTTPError as e:
        log.warning(f"Status Code: {r.status_code}")
        log.warning(f"Message: {r.text}")
        log.warning(e)
        return {"status_code": r.status_code, "message": r.text, "url": r.url}
    return return_message["data"]["rtmp"]["server"]["application"]