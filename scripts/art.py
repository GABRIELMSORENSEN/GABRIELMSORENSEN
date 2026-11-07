"""Original vector motion system. No JavaScript or remote images inside SVGs."""
from pathlib import Path
from html import escape
import math,random
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
INK='#09080f';WHITE='#eee9f3';MUTED='#9b91ad';PURPLE='#ad79ff';RED='#e04a65'

def svg(w,h,body,label):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(label)}</title><desc id="desc">Arte original G4T0XX. Tema escuro, molduras góticas, névoa e relógios inspirados em Re:Zero.</desc><defs><radialGradient id="aura"><stop stop-color="#743bad" stop-opacity=".42"/><stop offset="1" stop-color="#09080f" stop-opacity="0"/></radialGradient><linearGradient id="edge"><stop stop-color="#452b65"/><stop offset=".5" stop-color="#b685f6"/><stop offset="1" stop-color="#452b65"/></linearGradient><linearGradient id="fade"><stop stop-color="#09080f"/><stop offset="1" stop-color="#1c1127"/></linearGradient></defs><style>text{{font-family:'Courier New',monospace}}.serif{{font-family:Georgia,'Times New Roman',serif}}.small{{font-size:11px;letter-spacing:2px;fill:{MUTED}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style><rect width="100%" height="100%" fill="{INK}"/>{body}</svg>'''

def frame(w,h):
 out=f'<rect x="12" y="12" width="{w-24}" height="{h-24}" fill="none" stroke="#32243f"/><rect x="20" y="20" width="{w-40}" height="{h-40}" fill="none" stroke="#1e1828"/>'
 for x,y,sx,sy in [(12,12,1,1),(w-12,12,-1,1),(12,h-12,1,-1),(w-12,h-12,-1,-1)]:
  out+=f'<g transform="translate({x},{y}) scale({sx},{sy})"><path d="M0 48 V0 H48 M7 31 V7 H31 M0 0 L21 21 M11 25 Q30 30 25 11" stroke="{PURPLE}" stroke-width="1" fill="none"/><path d="M4 42 L10 36 L16 42 L10 48 Z" fill="#543460"/></g>'
 return out

def label(text,x,y,color=MUTED,size=11,spacing=2):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" letter-spacing="{spacing}">{escape(str(text))}</text>'

def clock(cx,cy,r):
 out=f'<g transform="translate({cx} {cy})"><circle r="{r*1.35}" fill="url(#aura)"/><g fill="none" stroke="#6f497f"><circle r="{r}" stroke-opacity=".55"/><circle r="{r-10}" stroke-opacity=".2"/><circle r="{r-36}" stroke-opacity=".25" stroke-dasharray="2 13"/></g>'
 for i in range(60):
  a=i*math.pi/30;d=15 if i%5==0 else 5
  out+=f'<path d="M{math.sin(a)*(r-13):.1f} {-math.cos(a)*(r-13):.1f} L{math.sin(a)*(r-13-d):.1f} {-math.cos(a)*(r-13-d):.1f}" stroke="#80608d" stroke-opacity=".6"/>'
 for a,t in [(0,'XII'),(90,'III'),(180,'VI'),(270,'IX')]:
  rad=math.radians(a);out+=f'<text x="{math.sin(rad)*(r-47):.1f}" y="{-math.cos(rad)*(r-47)+4:.1f}" text-anchor="middle" fill="#897193" class="serif" font-size="17">{t}</text>'
 out+=f'<g stroke="{PURPLE}" fill="none"><path d="M0 18 L0 {-r*.68}" stroke-width="1.4"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="24s" repeatCount="indefinite"/></path><path d="M0 12 L0 {-r*.43}" stroke-width="3"><animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="72s" repeatCount="indefinite"/></path></g><circle r="4" fill="{WHITE}"/></g>'
 return out

def hero():
 random.seed(66)
 body='<ellipse cx="985" cy="270" rx="380" ry="330" fill="url(#aura)"/>'
 body+=clock(980,280,211)
 # Original witch-like silhouette, ribbons and spectral hands. No traced anime artwork.
 body+='''<g fill="#100b19" stroke="#281a35" stroke-width="1.5"><path d="M847 493 Q866 396 915 356 Q875 296 910 223 Q922 173 980 170 Q1042 174 1053 232 Q1083 313 1043 358 Q1094 401 1116 493 Z"/><path d="M912 233 Q925 162 989 179 Q1049 185 1047 252 L1021 219 L1000 247 L979 215 L955 244 L936 215 Z" fill="#08060d"/><path d="M923 269 Q935 328 980 345 Q1026 327 1038 269 L1010 293 L977 278 L950 295 Z" fill="#160d20"/></g>
 <path d="M930 267 Q951 249 972 265 Q951 282 930 267 M989 265 Q1010 249 1031 267 Q1010 282 989 265" fill="#b38cda" opacity=".7"><animate attributeName="opacity" values=".45;.8;.45" dur="5s" repeatCount="indefinite"/></path>
 <path d="M916 376 Q798 373 743 429 L739 416 L765 384 L723 401 L721 387 L766 356 L709 375 L708 359 L777 326 Q803 312 803 333 L778 366 Q839 334 904 347 M1048 374 Q1141 351 1196 406 L1204 393 L1178 369 L1220 384 L1224 369 L1174 340 L1232 356 L1235 340 L1169 311 Q1146 303 1143 324 L1160 350 Q1101 325 1055 346" fill="#0c0812" stroke="#3d244a" stroke-width="2"/>
 <path d="M1102 89 L1058 142 L1091 170 L1056 218 M818 124 L866 155 L835 200 L873 240 M1133 397 L1099 437 L1138 462" stroke="#af4769" stroke-width="1" fill="none" opacity=".5"/>
 <path d="M865 509 Q984 437 1114 509" stroke="#683e82" stroke-width="1" fill="none"/>
 '''
 for i in range(50):
  x=random.randint(680,1210);y=random.randint(55,510);r=random.choice([.8,1,1.5])
  body+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{PURPLE}" opacity=".25"><animate attributeName="cy" values="{y};{y-24};{y}" dur="{5+i%7}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".1;.6;.1" dur="{3+i%5}s" repeatCount="indefinite"/></circle>'
 body+=label('PERSONAL ARCHIVE / GABRIEL SORENSEN',64,74,PURPLE)
 body+='<path d="M64 98 H498" stroke="#34233f"/>'
 body+=label('RE:ZERO INSPIRED  /  DARK FANTASY',64,127,MUTED,10,2)
 body+='<text x="59" y="253" fill="#f0e9f5" class="serif" font-size="111" letter-spacing="-6">G4T0XX<tspan fill="#d35473">.</tspan></text>'
 body+=label('RETURN BY DEATH.',65,301,WHITE,27,3)
 body+=label('REBUILD BY CODE.',65,338,PURPLE,27,3)
 body+='<path d="M65 369 H115" stroke="#ce4b6a" stroke-width="2"/>'
 body+=label('IA LOCAL · ANDROID · DESKTOP · VR',65,402,MUTED,13,1)
 body+=label('O fim de um loop. O início de outra criação.',65,429,MUTED,12,0)
 body+=label('SAVE POINT  /  01',65,493,RED,10,2)
 body+=label('ENTER THE ARCHIVE',901,513,PURPLE,10,3)
 body+=frame(1280,560)
 (ASSETS/'hero.svg').write_text(svg(1280,560,body,'G4T0XX — Return by Death. Rebuild by Code.'),encoding='utf-8')

def divider(name,number):
 body='<path d="M30 47 H390 M890 47 H1250" stroke="url(#edge)"/>'
 body+='<path d="M626 47 L640 33 L654 47 L640 61 Z" fill="#21132e" stroke="#8e60b1"/><circle cx="640" cy="47" r="4" fill="#c7a0ee"><animate attributeName="opacity" values=".3;1;.3" dur="4s" repeatCount="indefinite"/></circle>'
 body+=f'<text x="640" y="24" text-anchor="middle" fill="{MUTED}" font-size="10" letter-spacing="4">{escape(number)}</text><text x="640" y="88" text-anchor="middle" class="serif" fill="{WHITE}" font-size="28" letter-spacing="3">{escape(name)}</text>'
 return svg(1280,112,body,name)

PROJECTS=[
 ('POLIGON-ASSISTENT-AI','POLIGON','A voz encontra a visão.','Assistente desktop com IA, voz e tela.','PYTHON / IA / DESKTOP','01'),
 ('Forge-Mobile','FORGE','Um agente. Dois mundos.','Chat, memória e ferramentas no Android e PC.','JAVA / ANDROID / IA LOCAL','02'),
 ('GatoFocus-VR','GATOFOCUS VR','Além do que os olhos veem.','Estimativa de olhar para VRChat e SteamVR.','PYTHON / VRCHAT / OSC','03'),
 ('PORSUIT-REMOTE','PORSUIT REMOTE','O controle atravessa a distância.','PC pelo Android, VPN privada e Wake-on-LAN.','WINDOWS / ANDROID / REDE','04'),
 ('GATARME','GATARME','Nem todo recomeço pode esperar.','Alarmes Android para escalas de trabalho.','JAVA / ANDROID / ALARMES','05'),
 ('mania-chart-studio','MANIA CHART STUDIO','O caos também tem ritmo.','Editor local de charts osu!mania 4K.','PYTHON / ÁUDIO / OSU!MANIA','06'),
 ('g4-docs-editor','G4 DOCS EDITOR','Cada página guarda um fragmento.','Editor PDF local para desktop e web.','TYPESCRIPT / PDF / DESKTOP','07'),
 ('g4t0xx-portfolio','PORTFÓLIO','Um portal para o meu universo.','Interface com React, Vite e Framer Motion.','REACT / WEB / MOTION','08'),
]

def project_card(p,repo=None):
 slug,title,tag,desc,stack,num=p
 body='<ellipse cx="510" cy="90" rx="220" ry="190" fill="url(#aura)"/>'
 body+=f'<text x="516" y="149" text-anchor="middle" class="serif" fill="#2a1938" font-size="112">{num}</text>'
 body+=label('FRAGMENT '+num+'  /  PROJETO PÚBLICO',40,51,PURPLE,9,2)
 body+=f'<text x="39" y="102" class="serif" fill="{WHITE}" font-size="30" letter-spacing="1">{escape(title)}</text>'
 body+=label(tag,40,134,WHITE,17,0)
 body+=label(desc,40,161,MUTED,15,0)
 body+='<path d="M40 182 H580" stroke="#32223e"/>'
 body+=label(stack,40,207,PURPLE,13,1)
 body+=label('EXPLORAR ↗',469,207,MUTED,13,1)
 body+=frame(620,236)
 return svg(620,236,body,title+' — '+desc)

def footer():
 body=clock(640,104,64)+f'<text x="640" y="112" text-anchor="middle" class="serif" fill="{WHITE}" font-size="31" letter-spacing="4">RE:START</text>'
 body+=label('EU POSSO RECOMEÇAR. O QUE APRENDI VEM COMIGO.',340,205,MUTED,11,1)
 body+=label('G4T0XX  /  FIM DESTE LOOP',493,240,PURPLE,10,2)
 body+=frame(1280,276)
 return svg(1280,276,body,'Re:start — eu posso recomeçar; o que aprendi vem comigo.')

def main():
 ASSETS.mkdir(exist_ok=True);hero()
 for slug,name,num in [('projects','Fragmentos de outros mundos','01 / PROJETOS'),('metrics-section','O registro dos loops','02 / MÉTRICAS'),('inventory','Arsenal de criação','03 / FERRAMENTAS')]:
  (ASSETS/(slug+'.svg')).write_text(divider(name,num),encoding='utf-8')
 for p in PROJECTS:(ASSETS/('project-'+p[0]+'.svg')).write_text(project_card(p),encoding='utf-8')
 (ASSETS/'footer.svg').write_text(footer(),encoding='utf-8')
 body=clock(270,135,85)+label('THE COVENANT',54,50,PURPLE,12,3)
 body+='<text x="270" y="140" text-anchor="middle" fill="#eee9f3" class="serif" font-size="33">O PACTO</text>'
 body+=label('CRIAR. FALHAR. APRENDER.',81,255,WHITE,17,1)+label('RECOMEÇAR.',170,284,PURPLE,17,1)+frame(540,310)
 (ASSETS/'covenant.svg').write_text(svg(540,310,body,'O pacto — criar, falhar, aprender, recomeçar'),encoding='utf-8')
 body=label('CÓDIGO / SISTEMAS / MUNDOS',44,49,PURPLE,14,2)
 groups=[('01 / CÓDIGO','Python · Java · C#','TypeScript · JavaScript'),('02 / PLATAFORMAS','Android · Windows','React · Desktop · Web'),('03 / CRIAÇÃO','Unity · Blender · VRChat','Avatares · Áudio · Vídeo')]
 for i,(heading,line1,line2) in enumerate(groups):
  x=44+i*407
  body+=label(heading,x,102,PURPLE,13,2)+label(line1,x,145,WHITE,20,0)+label(line2,x,179,MUTED,17,0)
  if i<2:body+=f'<path d="M{x+375} 84 V194" stroke="#3c2848"/>'
 body+=frame(1280,232)
 (ASSETS/'arsenal.svg').write_text(svg(1280,232,body,'Arsenal de criação: código, plataformas e criação 3D'),encoding='utf-8')

if __name__=='__main__':main()
