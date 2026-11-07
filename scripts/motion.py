"""Render original vector animation to a self-contained GIF for GitHub."""
import io,math
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
from art import svg,frame,label,clock,PURPLE,MUTED,WHITE,ASSETS

def main():
 body=frame(1280,112)+clock(640,56,33)
 body+=label('RETURN',110,63,WHITE,20,6)+label('REBUILD',370,63,PURPLE,20,6)+label('REPEAT',824,63,WHITE,20,6)+label('↻',1128,64,PURPLE,25,0)
 body+='<path d="M245 56 H314 L321 46 L328 66 L335 56 H350 M960 56 H1030 L1037 46 L1044 66 L1051 56 H1100" stroke="#7a4a9a" fill="none"/>'
 body+='<circle cx="245" cy="56" r="2" fill="#eecfff"><animate attributeName="cx" values="245;350;245" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".2;.9;.2" dur="4s" repeatCount="indefinite"/></circle>'
 text=svg(1280,112,body,'Return / Rebuild / Repeat — ritual de recomeço')
 (ASSETS/'loop.svg').write_text(text,encoding='utf-8')
 frames=[]
 with sync_playwright() as p:
  browser=p.chromium.launch();page=browser.new_page(viewport={'width':960,'height':84},device_scale_factor=1)
  page.set_content('<html><body style="margin:0;background:#09080f">'+text.replace('width="1280" height="112"','width="960" height="84"')+'</body></html>')
  for i in range(48):
   page.evaluate('(t)=>{let s=document.querySelector("svg");s.pauseAnimations();s.setCurrentTime(t)}',i/12)
   im=Image.open(io.BytesIO(page.screenshot())).convert('RGB');frames.append(im)
  browser.close()
 frames[0].save(ASSETS/'loop-still.png')
 palette=frames[0].quantize(colors=96)
 out=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
 out[0].save(ASSETS/'loop.gif',save_all=True,append_images=out[1:],duration=84,loop=0,optimize=True,disposal=2)
 print('MOTION_GIF',len(frames),'frames', (ASSETS/'loop.gif').stat().st_size,'bytes')

if __name__=='__main__':main()
