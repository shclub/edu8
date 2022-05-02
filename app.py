#!/usr/local/bin/python3

import os
import logging

# Patching
# DEV: This is here only for those who choose not to use `ddtrace-run`
from ddtrace import config, patch_all; patch_all(flask=True, requests=True)  # noqa

# Datadog
from ddtrace import tracer
from flask import Flask

# k8s에 적용시에 주석 처리
config.env = "jake_edu"      # the environment the application is in
config.service = "app"  # name of your application
config.version = "0.1"  # version of your application

patch_all()

FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
        '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
        '- %(message)s')

logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.INFO

app = Flask(__name__)
podname = os.uname()[1]

@app.route("/")
@tracer.wrap() # Function 앞에 추가
def index():
    ret_str = " Container EDU | POD Working : " + podname + " | v=1\n"
    log.info(ret_str)
    return ret_str

if __name__ == "__main__":
    app.run(host="0.0.0.0" ,port=5000)
