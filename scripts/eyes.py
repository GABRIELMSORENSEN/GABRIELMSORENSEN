"""Original animated eyes: almond masks, eyelids, rolling irises and gothic frame."""
import io
from PIL import Image
from playwright.sync_api import sync_playwright
from art import ASSETS,svg,frame,label,PURPLE,MUTED,WHITE

def eye(cx,cy,index,color):
 # Eye-opening masks keep the iris behind the eyelids during a full roll.
 shape='M-116 0 Q-55 -68 0 -49 Q59 -49 116 0 Q48 61 0 47 Q-61 55 -116 0Z'
 begin=[0,1.1,2.4][index]
 return f'''<defs><clipPath id="eye-{index}"><path d="{shape}"/></clipPath><radialGradient id="iris-{index}"><stop stop-color="#e8d4fa"/><stop offset=".35" stop-color="{color}"/><stop offset=".7" stop-color="#68327d"/><stop offset="1" stop-color="#160c22"/></radialGradient><linearGradient id="sclera-{index}" x2="0" y2="1"><stop stop-color="#796484"/><stop offset=".5" stop-color="#d4c5dd"/><stop offset="1" stop-color="#8e759b"/></linearGradient></defs>
 <g transform="translate({cx} {cy})">
 <path d="M-143 0 H-129 M129 0 H143 M0 -77 V-66 M0 67 V77" stroke="#7c4c92"/>
 <path d="M-125 -9 Q-60 -88 22 -70 Q82 -57 125 -8" stroke="#392344" fill="none"/>
 <g><animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 .015;1 1;1 1" keyTimes="0;.28;.305;.33;1" dur="6s" begin="{begin}s" repeatCount="indefinite"/>
 <path d="{shape}" fill="url(#sclera-{index})" stroke="#0c0712" stroke-width="5"/>
 <g clip-path="url(#eye-{index})">
 <path d="M-110 -1 L-87 2 L-74 -8 M103 0 L88 5 L75 -6 M-77 29 L-58 22" stroke="#a8668f" opacity=".5" fill="none" stroke-width="1.2"/>
 <g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;-35 -8;-18 -35;0 -50;25 -32;38 -8;0 0;0 0" keyTimes="0;.17;.31;.4;.49;.58;.67;.8;1" dur="6s" begin="{begin}s" repeatCount="indefinite"/>
 <circle r="43" fill="url(#iris-{index})" stroke="#24132c" stroke-width="3"/>
 <circle r="31" stroke="{color}" stroke-opacity=".6" fill="none"/>
 <path d="M0 -35 V-20 M18 -30 L11 -18 M30 -17 L17 -10 M35 0 H20 M29 19 L17 11 M17 30 L10 18 M0 35 V20 M-17 30 L-10 18 M-30 18 L-18 11 M-35 0 H-20 M-29 -18 L-17 -11 M-17 -30 L-10 -18" stroke="#e6bafa" stroke-opacity=".45" stroke-width="1"/>
 <ellipse rx="11" ry="28" fill="#09050d"/><ellipse cx="-16" cy="-16" rx="7" ry="5" fill="#f8edff" opacity=".9"/><circle cx="17" cy="13" r="3" fill="#e2c4f5" opacity=".75"/>
 </g></g>
 <path d="M-121 -2 Q-48 -69 11 -51 Q79 -47 121 -2 M-116 1 Q-46 64 10 48 Q81 42 116 1" stroke="#4e2b60" stroke-width="3" fill="none"/>
 <path d="M-116 -1 L-129 -12 M-96 -18 L-104 -33 M-70 -37 L-73 -50 M92 -18 L104 -34 M113 -5 L129 -17" stroke="#80608e" stroke-width="2"/>
 </g>
 <path d="M-117 0 Q0 -6 117 0" stroke="{color}" opacity="0"><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;.28;.305;.33;1" dur="6s" begin="{begin}s" repeatCount="indefinite"/></path>
 </g>'''

def main():
 body='<ellipse cx="640" cy="134" rx="570" ry="130" fill="url(#aura)"/>'
 body+=label('UNSEEN PRESENCES / RE:ZERO INSPIRED',43,48,PURPLE,12,2)
 body+=label('NÃO DESVIE O OLHAR.',946,48,MUTED,12,2)
 for i,cx in enumerate([246,640,1034]):body+=eye(cx,143,i,['#bf8df5','#df6a9c','#bf8df5'][i])
 body+=label('THE SHADOWS ARE WATCHING',461,251,MUTED,13,3)+frame(1280,280)
 source=svg(1280,280,body,'Olhos nas sombras: três olhos piscam em momentos diferentes e reviram lentamente')
 (ASSETS/'eyes.svg').write_text(source,encoding='utf-8')
 frames=[]
 with sync_playwright() as p:
  b=p.chromium.launch();page=b.new_page(viewport={'width':960,'height':210})
  page.set_content('<body style="margin:0">'+source.replace('width="1280" height="280"','width="960" height="210"')+'</body>')
  for i in range(90):
   page.evaluate('(t)=>{let s=document.querySelector("svg");s.pauseAnimations();s.setCurrentTime(t)}',i/15)
   frames.append(Image.open(io.BytesIO(page.screenshot())).convert('RGB'))
  b.close()
 frames[0].save(ASSETS/'eyes-still.png')
 palette=frames[0].quantize(colors=128)
 out=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
 out[0].save(ASSETS/'eyes.gif',save_all=True,append_images=out[1:],duration=67,loop=0,optimize=True,disposal=2)
 print('EYES',len(out),'frames', (ASSETS/'eyes.gif').stat().st_size,'bytes')

if __name__=='__main__':main()
