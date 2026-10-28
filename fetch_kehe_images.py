"""Download KeHE catalog images by UPC into images/products/<UPC>.jpg.
Usage:   python3 fetch_kehe_images.py          (a few minutes; safe to re-run, it skips photos you already have)
         python3 fetch_kehe_images.py --retry   (also re-check products that had no image last time)
Then:    python3 build.py    -> the site lists ONLY products that have an image.
Uses only Python's standard library."""
import json, os, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "images", "products"); os.makedirs(OUT, exist_ok=True)
BASE = os.environ.get("KEHE_BASE", "https://s3.amazonaws.com/kehe-connect/prod/public_common/catalogimages/{size}/{upc}.jpg")
UA = "Mozilla/5.0 (PivoxMarket catalog builder)"
prods = json.load(open(os.path.join(HERE, "products_all.json"), encoding="utf-8"))
miss_path = os.path.join(OUT, "_no_image.txt")
known_missing = set() if "--retry" in sys.argv or not os.path.exists(miss_path) else set(open(miss_path).read().split())
def fetch(size, upc):
    """returns bytes, or None if KeHE has no image (403/404 or not an image); raises on network trouble"""
    req = urllib.request.Request(BASE.format(size=size, upc=upc.zfill(12)), headers={"User-Agent": UA})
    try:
        data = urllib.request.urlopen(req, timeout=25).read()
    except urllib.error.HTTPError as e:
        if e.code in (403, 404): return None
        raise
    return data if len(data) > 1500 and (data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n") else None
# pick the largest image size KeHE offers (tests a few products)
SIZE = "400"
for size in ("1000", "800", "600"):
    try:
        if any(fetch(size, p["u"]) for p in prods[:12]): SIZE = size; break
    except Exception: pass
print("Using image size:", SIZE)
have = {os.path.splitext(f)[0] for f in os.listdir(OUT)}
todo = [p["u"] for p in prods if p["u"] not in have and p["u"] not in known_missing]
print(f"{len(have)} photos already saved, checking {len(todo)} products...")
def work(upc):
    for _ in range(3):
        try:
            data = fetch(SIZE, upc)
            if data: open(os.path.join(OUT, upc + ".jpg"), "wb").write(data); return upc, "ok"
            return upc, "none"
        except Exception: pass
    return upc, "error"
res = {"ok": 0, "none": 0, "error": 0}; none = set(known_missing)
with ThreadPoolExecutor(8) as ex:
    for n, (upc, r) in enumerate(ex.map(work, todo), 1):
        res[r] += 1
        if r == "none": none.add(upc)
        if n % 200 == 0: print(f"  {n}/{len(todo)} checked, {res['ok']} saved", flush=True)
open(miss_path, "w").write("\n".join(sorted(none)))
total = len({os.path.splitext(f)[0] for f in os.listdir(OUT)} & {p["u"] for p in prods})
print(f"Done. {res['ok']} new photos, {res['none']} products have no KeHE image, {res['error']} could not be checked (re-run to retry).")
print(f"{total} of {len(prods)} products now have photos. Run: python3 build.py")
