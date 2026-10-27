"""Turns a KeHE inventory CSV into products_all.json for the site.
Usage: python3 process_inventory.py inventory.csv   (needs: pip install pandas)
Edit the settings below, then run `python3 build.py`."""
import pandas as pd, re, json, sys, collections
SRC = sys.argv[1] if len(sys.argv) > 1 else "inventory.csv"
PRICE_COL = "RETAIL"          # which price column to show: RETAIL = "DC 33 - RETAIL" (KeHE suggested retail). Change/mark up as you like.
PRETTY = {"bobsredmill":"Bob's Red Mill","amys":"Amy's Kitchen","raos":"Rao's","lesserevil":"LesserEvil","skinnypop":"SkinnyPop","hu":"Hu Kitchen","healthade":"Health-Ade","sanj":"San-J","tajin":"Tajín","lilyssweets":"Lily's Sweets","gimme":"GimMe Organic","organicville":"Organic Ville","safecatch":"Safe Catch","reeds":"Reed's","virgils":"Virgil's","bobosoatbars":"Bobo's Oat Bars","bachans":"Bachan's","briannas":"Brianna's","justins":"Justin's","angies":"Angie's BOOMCHICKAPOP","marysgonecrackers":"Mary's Gone Crackers","mikeshothoney":"Mike's Hot Honey","waterloosparklingwater":"Waterloo Sparkling Water","roarbeverages":"Roar Organic","rishitea":"Rishi Tea","quinn":"Quinn Snacks","partakefoods":"Partake Foods","chomps":"Chomps","yellowbirdsauce":"Yellowbird Sauce","pacificfoods":"Pacific Foods","imagine":"Imagine Foods","woodstock":"Woodstock Foods","edwardsons":"Edward & Sons","katz":"Katz Gluten-Free","elmhurst":"Elmhurst 1925","guayaki":"Guayaki Yerba Mate","unreal":"Unreal Snacks","rebblinc":"REBBL","boninemaman":"Bonne Maman","bonnemaman":"Bonne Maman","betterthanbouillon":"Better Than Bouillon","bragg":"Bragg","huyfong":"Huy Fong","dalmatia":"Dalmatia","gauchoranch":"Gaucho Ranch","inglehoffer":"Inglehoffer","goldendipt":"Golden Dipt","marmite":"Marmite","primalkitchen":"Primal Kitchen","chosenfoods":"Chosen Foods","siete":"Siete Foods","truff":"Truff","nativeforest":"Native Forest","muirglen":"Muir Glen","skyvalley":"Sky Valley","wildplanet":"Wild Planet","simplemills":"Simple Mills","hippeas":"Hippeas","endangeredspecies":"Endangered Species Chocolate","barnana":"Barnana","latejuly":"Late July","jovial":"Jovial Foods","enjoylife":"Enjoy Life Foods","smartsweets":"SmartSweets","alterEco".lower():"Alter Eco","theochocolate":"Theo Chocolate","beanitos":"Beanitos","belvoir":"Belvoir Fruit Farms","harmlessharvest":"Harmless Harvest","zevia":"Zevia","spindrift":"Spindrift","olipop":"Olipop","poppi":"Poppi","liquiddeath":"Liquid Death","califia":"Califia Farms","oatly":"Oatly","vitacoco":"Vita Coco","nixie":"Nixie Sparkling Water","traditionalmedicinals":"Traditional Medicinals","veetee":"Veetee Rice","kingarthur":"King Arthur Baking","lundberg":"Lundberg Family Farms","banza":"Banza","ancientharvest":"Ancient Harvest","explorecuisine":"Explore Cuisine","lotusfoods":"Lotus Foods","daiya":"Daiya","violife":"Violife"}
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("é","e").replace("í","i"))
d = pd.read_csv(SRC, dtype=str, encoding="utf-8").fillna("")
d.columns = ["DC","ITEM","UPC","BRAND","DESC","SIZE","UOM","UOS","WHLS","DISC","RETAIL","PROMO","CAT1","CAT2","CAT3"]
d = d.apply(lambda c: c.str.strip())
d["NB"] = d.BRAND.map(norm); d = d[d.NB.isin(PRETTY)]
BAD1 = {"FROZEN","REFRIGERATED","VITAMINS","HERBS","GENERAL MERCHANDISE","BULK","PET SUPPLIES","HEALTH BODY CARE","STORE SUPPLIES","PRODUCE","SEASONAL"}
d = d[~d.CAT1.str.upper().isin(BAD1)]
c2 = d.CAT2.str.upper(); d = d[~(c2.str.startswith(("CSF","REF")) | c2.isin(["CHEESE","YOGURT"]))]
d = d[~d.DESC.str.upper().str.contains(r"\b(?:WINE|BEER|SAKE)\b") | d.DESC.str.upper().str.contains("VINEGAR")]
d = d[~d.UOM.str.upper().isin(["DS","PL"]) & ~d.DESC.str.upper().str.contains(r"\b(?:DSP|PLT|PALT|HLF PLT)\b|\d+P$")]
d = d[~d.DESC.str.upper().str.contains(r"DNU|DISCONT|\bDNR\b|\*")]   # drop discontinued / do-not-use items
d = d[d.NB != "angostura"].drop_duplicates("UPC")
d["P"] = pd.to_numeric(d[PRICE_COL].str.replace(r"[^0-9.]", "", regex=True), errors="coerce"); d = d[d.P > 0]
UOM = {"FO":"fl oz","BG":"bags","GA":"gal","PC":"pc","CP":"ct","OZ":"oz","LB":"lb","FZ":"fl oz","FLOZ":"fl oz","CT":"ct","GM":"g","G":"g","ML":"ml","LT":"L","L":"L","PT":"pt","QT":"qt","GAL":"gal"}
AB = {"ORG":"Organic","GF":"Gluten Free","CHOC":"Chocolate","W/":"with","CHKN":"Chicken","VEG":"Vegetable","VEGGIE":"Vegetable","SWT":"Sweet","UNSWT":"Unsweetened","STRAWB":"Strawberry","BLUEB":"Blueberry","RASPB":"Raspberry","VAN":"Vanilla","CRM":"Cream","PNUT":"Peanut","NAT":"Natural","FLV":"Flavor","ORIG":"Original","SPKLG":"Sparkling","BBQ":"BBQ","RTD":"RTD","GMO":"GMO","NON":"Non","N/A":"","DRK":"Dark","RSTD":"Roasted","DRSSNG":"Dressing","ALMND":"Almond","ALMD":"Almond","WHT":"White","BTR":"Butter","BTTR":"Butter","BRWN":"Brown","BRWNRCE":"Brown Rice","SQZ":"Squeeze","DK":"Dark","MLK":"Milk","SLT":"Salt","SLTD":"Salted","SSLT":"Sea Salt","SEASLT":"Sea Salt","SSALT":"Sea Salt","YRBAMTE":"Yerba Mate","SPRKL":"Sparkling","SPRK":"Sparkling","SPRKLG":"Sparkling","GNGR":"Ginger","GRN":"Green","WHL":"Whole","GRLC":"Garlic","SNK":"Snack","CHS":"Cheese","CHDR":"Cheddar","PB":"Peanut Butter","PNT":"Peanut","CRML":"Caramel","CRMY":"Creamy","CCNT":"Coconut","CCNUT":"Coconut","NTRL":"Natural","ORGNL":"Original","BLK":"Black","BLCK":"Black","WHTE":"White","WTR":"Water","WLD":"Wild","STRWBRY":"Strawberry","HNY":"Honey","AVCDO":"Avocado","APPL":"Apple","ITAL":"Italian","BN":"Bean","VNGRT":"Vinaigrette","CHC":"Chocolate","LMN":"Lemon","ORNG":"Orange","CRNBERRY":"Cranberry","CRNCHY":"Crunchy","CSHW":"Cashew","SSME":"Sesame","SLTD":"Salted","MLTIGRN":"Multigrain","UNBLCH":"Unbleached","BSMATI":"Basmati","APRCT":"Apricot","RSPBRRY":"Raspberry","RSPBRY":"Raspberry","WW":"Whole Wheat","TMO":"Tamari","BOOMCHKA":"Boomchickapop","EVOO":"Extra Virgin Olive Oil","HMLYN":"Himalayan","PPPR":"Pepper","NS":"No Sugar","DF":"Dairy Free","BEV":"Beverage","TORT":"Tortilla","GRND":"Ground","SUG":"Sugar","LS":"Low Sodium","RTE":"Ready to Eat","SNKS":"Snacks","SPRKLNG":"Sparkling","MAC":"Mac &","CKE":"Cookie","CRKR":"Cracker","CHCLT":"Chocolate","CHOCLT":"Chocolate","VNLA":"Vanilla","BLBRY":"Blueberry","BLUBRY":"Blueberry","BRY":"Berry","PNUT":"Peanut","MNT":"Mint","MSTRD":"Mustard","MYO":"Mayo","LNTL":"Lentil","LNTLS":"Lentils","CHKPEA":"Chickpea","CKN":"Chicken","BF":"Beef","TRKY":"Turkey","SLMN":"Salmon","TNA":"Tuna","MSHRM":"Mushroom","TMTO":"Tomato","TMT":"Tomato","PTATO":"Potato","SWTPTO":"Sweet Potato","PNAPL":"Pineapple","MNGO":"Mango","PK":"Pack"}
def title(s):
    out=[]
    for w in re.split(r"\s+", s.upper()):
        w = AB.get(w, w)
        out.append(w if w in ("BBQ","RTD","GMO") else (w.capitalize() if w.isupper() or w.islower() else w))
    t = re.sub(r"\s+"," "," ".join(out)).strip()
    return re.sub(r"\b(\d+)(pk|pc|ct)\b", lambda m: m.group(1)+" "+m.group(2), t)
def cat(c):
    c = c.upper()
    if re.search(r"TEA|SODA|WATER|JUICE|BEV|COFFEE|ENERGY|COCKTAIL|DRINK", c): return "beverages"
    if re.search(r"CONDIMENT|DRESSING|SAUCE|SALSA|DIP", c): return "sauces"
    if re.search(r"CHIPS|PRETZEL|CRACKER|NUT SEED|RICE CAKE|JERKY|BAR|CHOCOLATE|CONFE|COOKIE|DESSERT|SNACK|POPCORN", c): return "snacks"
    if re.search(r"BAKING|FLOUR|CEREAL|PASTA|GRAIN|BEANS|RICE|PANCAKE|BREAKFAST", c): return "grains"
    return "pantry"
def shape(c2, n):  # index into [jar,bottle,can,bag,box,sack,bar]
    t = (c2 + " " + n).upper()
    if re.search(r"CHOCOLATE|CONFE", t): return 6
    if re.search(r"SODA|SPARKLING|ENERGY|SOUP|CANNED|TUNA|BEANS", t): return 2
    if re.search(r"DRESSING|SAUCE|OIL|VINEGAR|JUICE|BEVERAGE|SYRUP|HONEY", t): return 1
    if re.search(r"JAM|SPREAD|BUTTER|SALSA|DIP|OLIVE|PICKLE|SPICE|SEASONING|MAYO|MUSTARD|KETCHUP", t): return 0
    if re.search(r"CHIPS|POPCORN|PRETZEL|JERKY|NUTS|TRAIL|GRANOLA|FRUIT SNACK", t): return 3
    if re.search(r"FLOUR|RICE|GRAIN|OAT|BEANS|LENTIL|QUINOA", t): return 5
    return 4
rows = []
for r in d.itertuples():
    sz = f"{r.SIZE} {UOM.get(r.UOM.upper().replace(' ',''), r.UOM.lower())}".strip()
    nm = title(r.DESC); br = PRETTY[r.NB]
    rows.append({"u":r.UPC,"i":r.ITEM,"b":br,"n":nm,"s":sz,"p":round(float(r.P),2),"c":cat(r.CAT2),"h":shape(r.CAT2, r.DESC),"k":sum(map(ord,br))%8})
by = collections.defaultdict(list)
for x in sorted(rows, key=lambda x:(x["b"],x["n"])): by[x["b"]].append(x)
out, i = [], 0     # interleave brands so the first page shows variety
while any(by.values()):
    for b in sorted(by):
        if by[b]: out.append(by[b].pop(0))
import csv
with open("my_products_upcs.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["KeHE item","UPC","brand","product","size"]); [w.writerow([x["i"],x["u"].zfill(12),x["b"],x["n"],x["s"]]) for x in out]
json.dump(out, open("products_all.json","w"), ensure_ascii=False, separators=(",",":"))
print(len(out), "products,", len({x["b"] for x in out}), "brands")
print(collections.Counter(x["c"] for x in out)); print(sorted(d.UOM.unique())[:30])
