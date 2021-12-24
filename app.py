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

from collections import defaultdict

from flask import Flask
from flask import Response, render_template, send_from_directory
from flask_caching import Cache

import prime95_status

print("Setting up P-1 repository controller")

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


# Result of prime95_status.py <SERVE_DIR> --json status.json --recursive
SERVE_DIR = "/home/five/Downloads/GIMPS/p95_partials/"
FACTORS_FN = "mersenneca_known_factors_0G.txt"
STATUS_FN = "status.json"

# TODO TF, P-1 data from mersenne.ca/export

MAX_COLLECT_N = 10 ** 6


def load_factors(STOP=1e7):
    total = 0
    count = defaultdict(list)
    with open(os.path.join(app.root_path, FACTORS_FN)) as f:
        for line in f:
            raw = line.split(",")
            m, k = int(raw[0]), int(raw[1])
            if m > STOP:
                break
            total += 1
            count[m].append(k)

    print(f"Loaded {total} factors for {len(count)} exponents")
    return count


FACTORS = load_factors()

@app.route('/factors/<int:n>')
def get_factors(n):
    global FACTORS
    factors = map(lambda k: str(2*n*k + 1), FACTORS.get(n, []))
    return f'"{",".join(factors)}"'

def add_factor_count(wu):
    global FACTORS
    """ Lookup number of factors of n"""
    wu["num_factors"] = len(FACTORS.get(wu["n"], []))

def add_tags(wu):
    """ Add list of [(tag1, style1), (tag2, style2)]"""
    tags = []

    n = wu["n"]
    for under in [10, 100, 200]:
        if n <= under * 1000:
            tags.append((f"Under {under}k", "secondary"))
            break

    if wu["num_factors"] == 0:
        tags.append((f"NF", "warning"))

    if wu["num_factors"] > 5:
        tags.append(("MF", "info"))

    wu["tags"] = tags


# NOTE: status file is small (XXX kb) but avoid loading it on each request.
@cache.cached(timeout=5 * 60)
def get_status():
    status_path = os.path.join(app.root_path, STATUS_FN)
    if not os.path.exists(status_path):
        return None

    with open(status_path) as status_file:
        return json.load(status_file)


@app.route('/download/<filename>')
def download(filename):
    # Fine because get_status is cached
    status = get_status()

    if filename not in status:
        return f"{filename} not found", 404

    rel_path = status[filename]["path"]
    print(SERVE_DIR, rel_path)
    return send_from_directory(directory=SERVE_DIR, filename=rel_path)


@app.route("/")
def main_page():
    status = get_status()

    for name in list(status):
        wu = status[name]
        work = wu.pop('work_type')
        if work != 'PM1':
            status.pop(name)
            continue

        wu["number_str"] = prime95_status.number_str(wu)

        # These just busy up data
        wu.pop("B1_bound", None)
        wu.pop("B2_bound", None)
        wu.pop("path")


    exponents = set()
    B1 = []
    B2 = []
    for wu in status.values():
        add_factor_count(wu)
        add_tags(wu)

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
