"""Draws the hero and category illustrations as SVG files (no extra software needed)."""
from art import *
R,M,G,N,C,T,P,K="#B5382B","#E1A730","#2F6B4A","#2C4A6B","#FFF8EA","#C8643B","#6B3A5B","#2B2B28"
S={}
S["pantry"]=scene("#E8E2D6",jar(230,430,150,210,R,G,C)+jar(420,430,130,170,M,K,C)+box(600,430,125,215,C,N)+jar(780,430,120,235,"#7A4B2A",M,C)+bag(950,430,150,190,"#D9C9A3",G))
S["sauces"]=scene("#EBD3BE",bottle(220,430,95,260,R,C,C)+bottle(370,430,85,235,G,M,C)+bottle(510,430,110,200,M,R,C)+jar(690,430,150,160,"#8A2D1F",C,C)+bottle(890,430,90,250,T,K,C))
S["snacks"]=scene("#F0D9D2",bag(220,430,170,235,M,C)+bag(440,430,160,215,P,C)+bar(650,430,95,200,"#5A3622")+box(790,430,130,190,T,C)+cookie(990,405,34)+cookie(1060,408,30)+cookie(1020,355,30))
S["beverages"]=scene("#D3E0E4",can(220,430,95,200,N,C)+can(340,430,95,200,T,C)+bottle(480,430,105,270,G,K,C)+can(640,430,95,200,M,K)+can(760,430,95,200,P,C)+bottle(900,430,100,255,"#3F7F8A",C,C))
S["grains"]=scene("#DCE4CF",sack(210,430,200,250,C,"#D9B97B")+box(470,430,115,205,M,R)+bag(650,430,170,225,"#C8A26B",C)+jar(880,430,140,200,"#D9B97B",G,C)+"".join(f'<path d="M{1090+i*28} 430 Q{1100+i*28} 330 {1090+i*28} 250" stroke="#B8923E" stroke-width="5" fill="none"/>' for i in range(3)))
def shelf(b,items): return items+f'<rect x="60" y="{b+6}" width="1080" height="22" rx="8" fill="#B98A5A"/>'
H1=shelf(500,jar(110,500,150,200,R,G,C)+jar(300,500,125,165,M,K,C)+bottle(470,500,90,250,T,C,C)+bottle(600,500,85,225,G,M,C)+box(740,500,120,205,C,N)+jar(910,500,130,215,"#7A4B2A",M,C))
H2=shelf(860,bag(110,860,160,215,P,C)+bag(310,860,150,195,M,C)+can(500,860,90,190,N,C)+can(620,860,90,190,T,C)+sack(760,860,180,230,C,"#D9B97B")+bar(980,860,90,190,"#5A3622"))
S["hero"]=f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1100" viewBox="0 0 1200 1100"><rect width="1200" height="1100" fill="#F1E4BF"/><circle cx="600" cy="540" r="470" fill="#fff" opacity=".4"/>{H1}{H2}</svg>'

def write_svgs(folder="images"):
    import os
    os.makedirs(folder, exist_ok=True)
    for n, svg in S.items(): open(os.path.join(folder, n + ".svg"), "w", encoding="utf-8").write(svg)
