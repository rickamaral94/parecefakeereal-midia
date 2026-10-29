"""Render autoral do carrossel; Pillow + fonte Inter (INTER_FONT opcional)."""
from pathlib import Path
import os, json, math, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONT = next((p for p in [os.environ.get('INTER_FONT',''),
    '/usr/share/fonts/opentype/inter/Inter-Bold.otf',
    '/workspace/parecefakeereal-tools/inter/Inter Variable/Single axis/Inter-roman.ttf']
    if p and Path(p).is_file()), None)
if not FONT:
    raise SystemExit('Defina INTER_FONT para uma fonte Inter local.')
CARD = Path(os.environ.get('PFR_CARD', str(ROOT.parents[1] / 'marca/card_final_carrossel.jpg')))
W,H=1080,1350
BG='#0B0D13'; WHITE='#F5F6F8'; YELLOW='#FFC440'; MUTED='#A6ADBD'; PANEL='#151B29'

SLIDES = [
 ('Este metal pode\nderreter na mão.', 'Como isso acontece sem fogo?', 'cover'),
 ('Cada metal tem\nseu limite.', 'O ponto de fusão do gálio fica perto da temperatura de um dia quente.', 'limit'),
 ('A virada é\na 29,8 °C.', 'Essa é, aproximadamente, a temperatura em que o gálio puro começa a derreter.', 'temperature'),
 ('Calor pode\nvir da mão.', 'Com calor suficiente, o metal recebe energia até começar a mudar de estado.', 'heat'),
 ('Derreter não é\nlembrar a forma.', 'Aqui o sólido vira líquido. É diferente da memória de forma do nitinol.', 'change'),
 ('Não é em\nqualquer mão.', 'Temperatura, quantidade de metal e tempo de contato importam. Pode demorar.', 'caveat'),
 ('Então…', 'O gálio derrete perto de 29,8 °C; por isso, pode derreter sem fogo.\nÉ uma mudança de estado.', 'conclusion'),
]

def font(size,bold=False):
    f=ImageFont.truetype(FONT,size)
    try:
        axes=f.get_variation_axes()
        values=[a['default'] for a in axes]
        for i,a in enumerate(axes):
            if b'Weight' in a['name']: values[i]=850 if bold else 500
        f.set_variation_by_axes(values)
    except (OSError,AttributeError): pass
    return f

def text(d,xy,s,size=44,color=WHITE,bold=False,maxwidth=920,leading=1.23):
    x,y=xy; f=font(size,bold); lines=[]
    for paragraph in s.split('\n'):
        line=''
        for word in paragraph.split():
            trial=(line+' '+word).strip()
            if d.textlength(trial,font=f)>maxwidth:
                if not line: raise ValueError('Palavra não cabe: '+word)
                lines.append(line); line=word
            else: line=trial
        lines.append(line)
    for line in lines:
        box=d.textbbox((x,y),line,font=f)
        assert box[0]>=0 and box[2]<=W-60 and box[3]<=H-45,(s,box)
        d.text((x,y),line,font=f,fill=color)
        y+=int(size*leading)
    return y

def arrow(d,x1,y1,x2,y2,color=YELLOW,width=9):
    d.line((x1,y1,x2,y2),fill=color,width=width)
    a=math.atan2(y2-y1,x2-x1)
    p=[(x2,y2)]+[(x2-25*math.cos(a+t),y2-25*math.sin(a+t)) for t in [-.55,.55]]
    d.polygon(p,fill=color)

def cube(d,x,y,s=180):
    t=int(s*.35)
    d.polygon([(x,y),(x+s,y),(x+s,y+s),(x,y+s)],fill='#AEB9CC')
    d.polygon([(x,y),(x+t,y-t),(x+s+t,y-t),(x+s,y)],fill='#DEE6F2')
    d.polygon([(x+s,y),(x+s+t,y-t),(x+s+t,y+s-t),(x+s,y+s)],fill='#6B7891')
    for u in [.25,.5,.75]:
        d.line((x+int(s*u),y,x+int(s*u),y+s),fill='#8492AB',width=2)

def droplet(d,x,y,r=100):
    points=[(x,y-int(r*1.6))]
    for i in range(61):
        a=math.pi+math.pi*i/60
        points.append((x+r*math.cos(a),y-r*math.sin(a)))
    d.polygon(points,fill='#B7C5DA')
    d.ellipse((x-r,y-r*.35,x+r,y+r),fill='#B7C5DA')
    d.arc((x-r*.62,y-r*.15,x+r*.62,y+r*.7),10,120,fill='#EDF4FF',width=8)

def thermometer(d,x,y,h=360):
    d.rounded_rectangle((x,y,x+62,y+h),31,fill='#253047',outline='#8D9CB5',width=4)
    d.rounded_rectangle((x+20,y+65,x+42,y+h),11,fill=YELLOW)
    d.ellipse((x-23,y+h-35,x+85,y+h+73),fill=YELLOW)

def scene(d,kind):
    if kind=='cover':
        d.ellipse((140,575,930,1150),fill=PANEL)
        cube(d,185,740,190); arrow(d,490,835,610,835); droplet(d,805,835,110)
        text(d,(170,1080),'GÁLIO',size=42,bold=True,color=YELLOW)
    elif kind=='limit':
        d.rounded_rectangle((80,600,1000,1110),36,fill=PANEL)
        d.line((175,905,905,905),fill='#55617A',width=10)
        d.line((175,905,590,905),fill=YELLOW,width=10)
        for x in [175,590,905]: d.ellipse((x-12,893,x+12,917),fill=WHITE)
        text(d,(130,955),'FRIO',size=30,color=MUTED)
        text(d,(775,955),'CALOR',size=30,color=MUTED)
        text(d,(325,710),'29,8 °C',size=88,bold=True,color=YELLOW)
    elif kind=='temperature':
        thermometer(d,180,630)
        text(d,(345,740),'29,8',size=154,bold=True,color=YELLOW)
        text(d,(355,925),'°C',size=64,color=MUTED)
    elif kind=='heat':
        cube(d,690,765,175)
        for y in [780,850,920]: arrow(d,200,y,560,y)
        text(d,(190,1060),'CALOR',size=34,color=YELLOW)
    elif kind=='change':
        d.rounded_rectangle((80,625,1000,1135),35,fill=PANEL)
        cube(d,155,805,165); arrow(d,470,870,610,870); droplet(d,820,870,90)
        text(d,(135,1040),'SÓLIDO',size=34,bold=True)
        text(d,(730,1040),'LÍQUIDO',size=34,bold=True)
    elif kind=='caveat':
        for n,y in enumerate([670,835,1000]):
            d.rounded_rectangle((80,y,1000,y+112),24,fill=PANEL)
            text(d,(110,y+34),['Temperatura','Quantidade','Tempo'][n],size=34,color=WHITE)
            d.line((440,y+56,920,y+56),fill='#3B465C',width=10)
            d.ellipse((490+n*150,y+34,534+n*150,y+78),fill=YELLOW)
    elif kind=='conclusion':
        d.ellipse((290,730,790,1170),fill=PANEL)
        droplet(d,540,965,125)

def main():
    records=[]; thumbs=[]
    for i,(title,body,kind) in enumerate(SLIDES,1):
        im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
        text(d,(80,62),'@parecefakeereal',size=30,color=MUTED)
        text(d,(930,62),f'{i}/8',size=30,color=MUTED,maxwidth=100)
        d.line((80,130,210,130),fill=YELLOW,width=7)
        end=text(d,(80,180),title,size=78,bold=True)
        end=text(d,(80,end+35),body,size=45,maxwidth=900)
        assert end<650,(i,end)
        scene(d,kind)
        text(d,(80,1254),'Diagrama sem escala',size=24,color=MUTED)
        text(d,(815,1254),'NIST, 2005',size=24,color=MUTED,maxwidth=210)
        extra={'cover':'GÁLIO','limit':'FRIO CALOR 29,8 °C','temperature':'29,8 °C',
               'heat':'CALOR','change':'SÓLIDO LÍQUIDO','caveat':'Temperatura Quantidade Tempo','conclusion':''}[kind]
        visible=f'{title} {body} {extra} @parecefakeereal {i}/8 Diagrama sem escala NIST, 2005'
        count=len(visible.split()); assert count<=30,(i,count)
        path=ROOT/f'{i:02}.jpg';im.save(path,quality=94,subsampling=0)
        records.append({'slide':i,'title':title,'body':body,'diagram':kind,'visible_words':count,
                        'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        thumb=im.copy();thumb.thumbnail((270,338));thumbs.append(thumb)
    shutil.copyfile(CARD,ROOT/'08.jpg')
    card=Image.open(ROOT/'08.jpg'); assert card.size==(W,H)
    card.thumbnail((270,338));thumbs.append(card)
    sheet=Image.new('RGB',(1080,676),BG)
    for i,thumb in enumerate(thumbs):sheet.paste(thumb,((i%4)*270,(i//4)*338))
    sheet.save(ROOT/'preview.jpg',quality=90)
    (ROOT/'slides.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'slides':8,'words':[r['visible_words'] for r in records],'size':[W,H]}))

if __name__=='__main__':main()
