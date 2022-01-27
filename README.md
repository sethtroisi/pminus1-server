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
ln -s ../../misc-scripts/mersenne/status_report/prime95_manage.py .

# Download P-1 files from ???

# Link know factors file
# wget https://www.mersenne.ca/export/mersenneca_known_factors_0G.txt.xz
# unxz mersenneca_known_factors_0G.txt.xz
ln -s ~/Downloads/GIMPS/mersenneca_known_factors_0G.txt .

FLASK_APP=app.py FLASK_ENV=development flask run
```

A local server should now be running at http://localhost:5090

### Layout

I considered two directory structures
* 2 digits of Hex (256 folders)
   * Pros: Each folder is more uniform
   * Cons: Zipping is harder
* X00K, X.YM
   * Pros: Content is spatical close for zipping
   * Cons: More code, folders have thousands of items per

Space requirement is roughly

```python
for i in range(10**6, 10**7+1, 10**6):
    print(f"|{i:8}|{primesieve.count_primes(i):6}|{sum(p + 2048 for p in primesieve.primes(i))/8e9:5.1f}|")
```

|Max Prime|Primes|Space (GB)|
|---|---|---|
| 1000000| 78498|  4.7|
| 2000000|148933| 17.9|
| 3000000|216816| 39.1|
| 4000000|283146| 68.1|
| 5000000|348513|104.9|
| 6000000|412849|149.2|
| 7000000|476648|201.0|
| 8000000|539777|260.2|
| 9000000|602489|326.8|
|10000000|664579|400.6|

I've targetted 3,000,000 (216,816 residual files) as my target.

Opting for better names I've gone with `0.01M`, `0.51M`, `2.12M` BUT I'll nest them twice `1M/1.12M/M1120001`


### TODO

* [x] View records
  * [ ] Allow sorting
* [x] Download files
* [ ] Import script
* [ ] Upload files
* [ ] Reserve work
* [ ] Sorted list of "best" work to do
  * [ ] Catagories: No known factors, many factors, <100K, <1M
