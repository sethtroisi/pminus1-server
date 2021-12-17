## Mersenne P-1 Repository

A frontend to organize, download, and upload Prime95 P-1 partial files.

```shell
pip install -r requirements.txt

# Setup
git clone https://github.com/sethtroisi/pminus1-server
cd pminus1-server

# Download P-1 files from ???

python app.py
```

A local server should now be running at http://localhost:5090

### TODO

* [ ] View records
* [ ] Download files
* [ ] Upload files
* [ ] Reserve work
* [ ] Sorted list of "best" work to do
  * [ ] Catagories: No known factors, many factors, <100K, <1M
