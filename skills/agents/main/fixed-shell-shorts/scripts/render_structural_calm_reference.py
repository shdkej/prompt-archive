#!/usr/bin/env python3
"""Create a visual reference canvas for the fixed-shell shorts design system."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'references' / 'structural-calm-reference.png'
W,H=1080,1920
FONT=Path('/home/ubuntu/.openclaw/agents/main/agent/codex-home/skills/canvas-design/canvas-fonts')
DISPLAY=str(FONT/'NationalPark-Bold.ttf'); MONO=str(FONT/'GeistMono-Regular.ttf')
KOR='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; KORB='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def ft(path,size): return ImageFont.truetype(path,size,index=0)
def centered(d,t,y,font,color):
    b=d.multiline_textbbox((0,0),t,font=font,align='center'); d.multiline_text(((W-(b[2]-b[0]))/2,y),t,font=font,fill=color,align='center')
im=Image.new('RGB',(W,H),'#0C0C0A'); d=ImageDraw.Draw(im)
bone='#F4F0E8'; muted='#99958D'; paper='#F8FAF8'; ink='#171717'; grid='#DDE3DD'
# measured shell
d.text((72,78),'SERIES / 001',font=ft(MONO,22),fill=muted)
centered(d,'STRUCTURAL',170,ft(DISPLAY,76),bone); centered(d,'CALM',255,ft(DISPLAY,76),bone)
d.line((72,408,1008,408),fill='#4A4741',width=2); d.rectangle((64,482,1016,1410),outline=bone,width=3)
# central paper specimen: object -> relation -> result
d.rectangle((72,490,1008,1402),fill=paper)
for x in range(72,1008,48): d.line((x,490,x,1402),fill=grid,width=1)
for y in range(490,1402,48): d.line((72,y,1008,y),fill=grid,width=1)
d.text((126,552),'ONE OBJECT / ONE RELATION / ONE RESULT',font=ft(MONO,18),fill='#6F746F')
d.rounded_rectangle((148,800,414,1070),radius=28,outline=ink,width=4)
d.rounded_rectangle((666,780,932,1090),radius=28,fill=ink)
d.line((438,936,640,936),fill=ink,width=5); d.polygon([(640,936),(614,920),(614,952)],fill=ink)
d.rounded_rectangle((467,900,611,972),radius=18,fill=paper,outline=ink,width=3)
d.text((486,923),'RELATION',font=ft(MONO,17),fill=ink)
d.text((215,906),'FORM',font=ft(DISPLAY,42),fill=ink); d.text((730,902),'RESULT',font=ft(MONO,22),fill=bone)
d.line((72,1538,1008,1538),fill='#4A4741',width=2); centered(d,'LESS, BUT CLEARER.',1626,ft(DISPLAY,38),bone); centered(d,'A fixed shell, a changing proof.',1700,ft(MONO,20),muted)
im.save(OUT)
