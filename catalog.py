# Loads products.json (made by process_inventory.py). To add photos, drop files named <UPC>.jpg|png|webp into images/products/ and re-run build.py.
import json, os, re
from urllib.parse import quote
from art import product_svg
HERE = os.path.dirname(os.path.abspath(__file__))
CATS = [("pantry","Pantry staples"),("sauces","Condiments and sauces"),("snacks","Snacks, sweets and bakery"),("beverages","Beverages"),("grains","Grains, baking and dairy alternatives")]
COL = {"pantry":"#E8E2D6","sauces":"#EBD3BE","snacks":"#F0D9D2","beverages":"#D3E0E4","grains":"#DCE4CF"}
SHAPES = ["jar","bottle","can","bag","box","sack","bar"]
PAL = [("#B5382B","#F2E8C9"),("#E1A730","#B5382B"),("#2F6B4A","#FFF8EA"),("#2C4A6B","#E1A730"),("#6B3A5B","#FFF8EA"),("#C8643B","#2B2B28"),("#3F7F8A","#FFF8EA"),("#7A4B2A","#E1A730")]
ONLY_WITH_IMAGES = True   # the site lists only products that have a photo
PRODUCTS = json.load(open(os.path.join(HERE,"products_all.json"),encoding="utf-8"))
_d = os.path.join(HERE,"images","products")
IMGS = {os.path.splitext(f)[0]:f for f in os.listdir(_d)} if os.path.isdir(_d) else {}
for p in PRODUCTS: p["m"] = IMGS.get(p["u"],"")
TOTAL = len(PRODUCTS)
if ONLY_WITH_IMAGES and any(p["m"] for p in PRODUCTS): PRODUCTS = [p for p in PRODUCTS if p["m"]]
elif ONLY_WITH_IMAGES: print("No product photos found yet, so every product is listed. Run fetch_kehe_images.py first.")
else: pass
def write_json():
    json.dump([{k:v for k,v in p.items() if v != ""} for p in PRODUCTS], open(os.path.join(HERE,"products.json"),"w",encoding="utf-8"), ensure_ascii=False, separators=(",",":"))
def sprites():
    out = ""
    for sh in SHAPES:
        for k,(body,acc) in enumerate(PAL):
            inner = re.sub(r"^<svg[^>]*>|</svg>$","",product_svg(sh,body,acc))
            out += f'<symbol id="{sh}-{k}" viewBox="0 0 240 240">{inner}</symbol>'
    return f'<svg xmlns="http://www.w3.org/2000/svg">{out}</svg>'
def card(p,email):
    esc = lambda s: s.replace("&","&amp;").replace("'","&#39;").replace('"',"&quot;")
    if p.get("m"): pic = f"<div class='pic photo'><img src='/images/products/{p['m']}' alt='{esc(p['b']+' '+p['n'])}' loading='lazy'></div>"
    else: pic = f"<div class='pic' style='--c:{COL[p['c']]}'><svg viewBox='0 0 240 240' aria-hidden='true'><use href='/sprites.svg#{SHAPES[p['h']]}-{p['k']}'/></svg></div>"
    href = f"/product/{p['u']}.html"
    mail = f"mailto:{email}?subject=" + quote(f"Inquiry: {p['b']} {p['n']} ({p['u']})")
    return f"<article class='card' data-cat='{p['c']}'><a class='pic-link' href='{href}' tabindex='-1' aria-hidden='true'>{pic}</a><div class='info'><p class='brand'>{esc(p['b'])}</p><h3><a href='{href}'>{esc(p['n'])}</a></h3><p class='size'>{esc(p['s'])}</p><span class='price'>${p['p']:.2f}</span><a class='ask' href='{mail}'>Ask about availability</a></div></article>"
