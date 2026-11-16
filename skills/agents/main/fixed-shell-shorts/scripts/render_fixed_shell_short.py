#!/usr/bin/env python3
"""Render a fixed-shell 9:16 short from central still images without camera motion."""
import argparse
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, X, Y, CW, CH = 1080, 1920, 72, 510, 936, 860
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def f(size, bold=True): return ImageFont.truetype(BOLD if bold else REG, size, index=0)
def centered(d, text, y, ft, color):
    b = d.multiline_textbbox((0, 0), text, font=ft, align='center'); d.multiline_text(((W-(b[2]-b[0]))/2, y), text, font=ft, fill=color, align='center')
def make_shell(path, a):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); cream='#F5F1E8'; muted='#AAA59C'
    d.rectangle((0,0,W,462),fill='#080807'); d.rectangle((0,1410,W,H),fill='#080807'); d.rectangle((64,486,1016,1394),outline=cream,width=3)
    d.text((72,76),a.top_label,font=f(28),fill=muted); centered(d,a.hook,182,f(76),cream); centered(d,a.subtitle,288,f(46,False),muted); d.line((72,1538,1008,1538),fill='#3B3832',width=2); centered(d,a.bottom_label,1620,f(38),cream); im.save(path)
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def main():
    p=argparse.ArgumentParser(); p.add_argument('--screens',required=True); p.add_argument('--top-label',required=True); p.add_argument('--hook',required=True); p.add_argument('--subtitle',default=''); p.add_argument('--bottom-label',required=True); p.add_argument('--duration',type=float,default=3); p.add_argument('--output',required=True); a=p.parse_args()
    screens=[Path(x).expanduser().resolve() for x in a.screens.split(',')]
    if not screens or any(not x.is_file() for x in screens): raise SystemExit('Every --screens item must be an existing image file.')
    out=Path(a.output).expanduser().resolve(); out.parent.mkdir(parents=True,exist_ok=True); frames=round(a.duration*30)
    with tempfile.TemporaryDirectory(prefix='fixed-shell-') as td:
        td=Path(td); overlay=td/'shell.png'; make_shell(overlay,a); clips=[]
        for i,screen in enumerate(screens,1):
            clip=td/f'cut-{i:02d}.mp4'; clips.append(clip); graph=(f"[0:v]scale={CW}:{CH}:force_original_aspect_ratio=increase,crop={CW}:{CH},fps=30,format=rgba[s];[1:v]format=rgba[o];color=c=#080807:s={W}x{H}:d={a.duration},format=rgba[b];[b][s]overlay={X}:{Y}[m];[m][o]overlay=0:0,format=yuv420p")
            run(['ffmpeg','-y','-loop','1','-i',str(screen),'-loop','1','-i',str(overlay),'-filter_complex',graph,'-t',str(a.duration),'-r','30','-c:v','libx264','-pix_fmt','yuv420p',str(clip)])
        manifest=td/'concat.txt'; manifest.write_text(''.join(f"file '{x}'\n" for x in clips)); run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy',str(out)])
if __name__=='__main__': main()
