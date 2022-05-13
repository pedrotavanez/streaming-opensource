#!/usr/bin/env python3
def create_mg(metric_list, mg_name, external_link):

    metric_goup={
        f"Nginx {mg_name}": {
            "status": 100,
            "level": 1,
            "inline": True,
            "update_threshold": 1,
            "external_links": [external_link],
            "metrics": metric_list,
        }
    }
    return metric_goup

