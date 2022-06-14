from requester import requester
def get_e2e_paths(ts_host,ts_headers):
    url=ts_host+"/api/rest/e2ePaths/"
    paths=requester("get", url, headers=ts_headers)
    return paths

def find_paths(paths, channel_name):
    for channel in paths:
        if channel["channel_name"]==channel_name:
            return channel
    return "Channel not found"