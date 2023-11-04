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


import os
import time


# TODO these should maybe live in a config file, be arguments, or ...

SERVE_DIR = "/home/five/Downloads/GIMPS/p95_partials/serving/"

MAX_N = 3 * 10 ** 6


def create_descriptive_directories(base, n):
    print(f"Create descriptive (1M/1.23M) directories in {base!r}")
    if not os.path.isdir(base):
        print(f"Does not exist: {base!r}")
        exit(1)

    time.sleep(5)

    os.chdir(base)

    for extra_dir in ("uploads", "temp", "bad", "old", "extra"):
        if not os.path.exists(extra_dir):
            print(extra_dir)
            os.mkdir(extra_dir)

    # folder per 10000 -> max of 1229, "average" of ~700
    for interval in range(0, n, 10000):
        outer = f"{interval // 10 ** 6}M"
        inner = f"{interval  / 10 ** 6:.2f}M"
        if not os.path.exists(outer):
            print(outer)
            os.mkdir(outer)

        inner_path = os.path.join(outer, inner)
        if not os.path.exists(inner_path):
            print(inner_path)
            os.mkdir(inner_path)



if __name__ == "__main__":
    create_descriptive_directories(SERVE_DIR, MAX_N)
