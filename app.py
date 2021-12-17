'''
Copyright 2021 Seth Troisi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


import json
import os

from flask import Flask
from flask import Response, render_template
from flask_caching import Cache

import prime95_status

print("Setting up P-1 repository controller")

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


# Result of prime95_status.py <SERVE_DIR> --json status.json
SERVE_DIR = "/home/five/Downloads/GIMPS/p95_partials/7_to_20K/"
STATUS_FN = "status.json"

# TODO TF, P-1 data from mersenne.ca/export

MAX_N = 10 ** 6


# NOTE: status file is small (XXX kb) but avoid loading it on each request.
@cache.cached(timeout=5 * 60)
def get_status():
    status_path = os.path.join(app.root_path, STATUS_FN)
    if not os.path.exists(status_path):
        return None

    with open(status_path) as status_file:
        return json.load(status_file)


@app.route("/")
def controller():
    status = get_status()

    for name in status:
        wu = status[name]
        work = wu.pop('work_type')
        if work != 'PM1':
            status.pop(name)
            continue

        wu["number_str"] = prime95_status.number_str(wu)

        # These just busy up data
        wu.pop("B1_bound", None)
        wu.pop("B2_bound", None)


    exponents = set()
    B1 = []
    B2 = []
    for wu in status.values():
        exponents.add(wu["number_str"])
        b1 = wu.get("B1_progress", None)
        if b1:
            B1.append(b1)
            b2 = wu.get("B2_progress", None)
            if b2:
                B2.append(b2)


    return render_template(
        "index.html",
        status=status,
        total_exponents=len(exponents),
        B1_range = (min(B1), max(B1)),
        B2_range = (min(B2, default=None), max(B2, default=None)),
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
