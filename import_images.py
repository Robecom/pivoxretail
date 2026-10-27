"""Match a folder of product images (for example a bulk download from KeHE) to your products automatically.
Matching works on the UPC (also GTIN-13/14 forms) or the KeHE item number found anywhere in the file name.
Usage:   python3 import_images.py "path/to/folder"      (zip files in the folder are unpacked automatically)
Then:    python3 build.py
Tip: pip install pillow  -> images are resized and converted to web-friendly JPGs. Without it, only jpg/png/webp are copied as-is."""
import json, os, re, sys, shutil, tempfile, zipfile
try: from PIL import Image
except ImportError: Image = None
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "images", "products"); os.makedirs(OUT, exist_ok=True)
if len(sys.argv) < 2: sys.exit(__doc__)
SRC = sys.argv[1]; EXT = (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff")
prods = json.load(open(os.path.join(HERE, "products_all.json"), encoding="utf-8"))
full, p11 = {}, {}
for p in prods:
    u12 = p["u"].zfill(12); full[u12.lstrip("0")] = p["u"]; p11[u12[:11]] = p["u"]
    if p.get("i"): full[p["i"].lstrip("0")] = p["u"]
def match(name):
    for run in re.findall(r"\d{6,14}", name):
        k = run.lstrip("0")
        if k in full: return full[k]
        if len(run) >= 13 and run[-12:].lstrip("0") in full: return full[run[-12:].lstrip("0")]
        if len(run) == 14 and run[1] == "0" and run[2:13] in p11: return p11[run[2:13]]
    return None
def score(path):  # lower = better "front of pack" guess
    n = os.path.basename(path).lower(); s = 0
    if re.search(r"front|a1c1|main|primary|[_\-\. ]1[_\-\.]|[_\-]01\b|[_\-]1\.", n): s -= 1
    if re.search(r"back|nutri|ingred|a1c7|a7|side|left|right|top|bottom|[_\-][2-9]\.", n): s += 1
    return (s, n)
work = tempfile.mkdtemp(); files = []
for root, _, names in os.walk(SRC):
    for f in names:
        fp = os.path.join(root, f)
        if f.lower().endswith(".zip"):
            try: zipfile.ZipFile(fp).extractall(os.path.join(work, str(len(files)) + f))
            except zipfile.BadZipFile: print("Skipping bad zip:", f)
        elif f.lower().endswith(EXT): files.append(fp)
for root, _, names in os.walk(work):
    files += [os.path.join(root, f) for f in names if f.lower().endswith(EXT)]
best, unmatched = {}, []
for fp in files:
    upc = match(os.path.basename(fp)) or match(os.path.basename(os.path.dirname(fp)))
    if not upc: unmatched.append(os.path.basename(fp)); continue
    if upc not in best or score(fp) < score(best[upc]): best[upc] = fp
saved = 0
for upc, fp in best.items():
    for old in os.listdir(OUT):
        if os.path.splitext(old)[0] == upc: os.remove(os.path.join(OUT, old))
    try:
        if Image:
            im = Image.open(fp)
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[-1]); im = bg
            im.convert("RGB").resize((1, 1)) ; im = im.convert("RGB"); im.thumbnail((900, 900))
            im.save(os.path.join(OUT, upc + ".jpg"), quality=86, optimize=True)
        elif fp.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            shutil.copy(fp, os.path.join(OUT, upc + os.path.splitext(fp)[1].lower()))
        else: print("Install pillow to convert:", os.path.basename(fp)); continue
        saved += 1
    except Exception as e: print("Could not read", os.path.basename(fp), e)
shutil.rmtree(work, ignore_errors=True)
have = {os.path.splitext(f)[0] for f in os.listdir(OUT)}
print(f"{len(files)} image files found, {saved} products matched and saved, {len(unmatched)} files matched no product.")
print(f"{sum(p['u'] in have for p in prods)} of {len(prods)} products now have photos.")
if unmatched: print("Examples of unmatched files:", ", ".join(unmatched[:5]))
