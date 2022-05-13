#!/usr/bin/env python3
from helpers.thresholds import validate_threshold
def create_metric(metric_value, metric_name_ts, has_suffix="", visible=True, critical=False):
    value=metric_value
    suffix=has_suffix
    status, status_mg=validate_threshold(metric_value, metric_name_ts, suffix, critical)
    if has_suffix==True:
        value=metric_value.split(" ")[0]
        suffix=metric_value.split(" ")[1]
    metric_dict={
        "name": metric_name_ts,
        "suffix": f" {suffix}",
        "value": value,
        "type": "numeric",
        "status": status,
        "visible": visible,
    }
    return metric_dict