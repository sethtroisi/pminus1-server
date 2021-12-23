## Mersenne P-1 Repository

A frontend to organize, download, and upload Prime95 P-1 partial files.

```shell
pip install -r requirements.txt

# Setup
git clone https://github.com/sethtroisi/pminus1-server
cd pminus1-server

# git submodule later
# wget for people who aren't me
ln -s ../../misc-scripts/mersenne/status_report/prime95_status.py .

# Download P-1 files from ???

# Link know factors file
# wget https://www.mersenne.ca/export/mersenneca_known_factors_0G.txt.xz
# unxz mersenneca_known_factors_0G.txt.xz
ln -s ~/Downloads/GIMPS/mersenneca_known_factors_0G.txt .

FLASK_APP=app.py FLASK_ENV=development flask run
```

A local server should now be running at http://localhost:5090

### TODO

* [x] View records
  * [ ] Allow sorting
* [x] Download files
* [ ] Upload files
* [ ] Reserve work
* [ ] Sorted list of "best" work to do
  * [ ] Catagories: No known factors, many factors, <100K, <1M
