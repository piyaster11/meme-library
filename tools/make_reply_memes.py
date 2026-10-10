"""Generate square 1:1 (1080x1080) reply memes using each meme's ORIGINAL English wording (no translation).
Classic meme style: Anton (Impact-like), white text, black outline, top/bottom.
Usage: python3 tools/make_reply_memes.py
Edit REPLIES: (id, template_in_img, crop(x0,y0,x1,y1 fractions) or None, top_text, bottom_text, [occasions], 'search keywords incl. Thai')
Search keywords are only stored in data/memes.json, never drawn on the image."""
import json,os
from PIL import Image,ImageDraw,ImageFont
FONT=os.path.join(os.path.dirname(__file__),'fonts','Anton-Regular.ttf')
L=(0,0,.5,1);TL=(0,0,.5,.5);BL=(0,.5,.5,1)
REPLIES=[
('this-is-fine','this-is-fine',L,'','THIS IS FINE',['work','monday'],'fine ok ไม่เป็นไร ไม่ไหว deadline เดดไลน์'),
('one-does-not-simply','one-does-not-simply',None,'ONE DOES NOT SIMPLY','',['work','disagree'],'no simply ไม่ง่าย ยาก'),
('not-sure-if','futurama-fry',None,'NOT SURE IF...','',['shocked'],'not sure confused งง สงสัย'),
('surprised-pikachu','surprised-pikachu',None,'','',['shocked'],'surprised shocked ตกใจ อึ้ง what อะไรนะ'),
('hide-the-pain','hide-the-pain-harold',None,'','HIDE THE PAIN',['work','sad','sorry'],'pain fine ok ฝืนยิ้ม เศร้า'),
('i-am-once-again-asking','bernie-i-am-once-again-asking-for-your-support',None,'','',['broke','payday'],'money broke เงินหมด ขอเงิน'),
('sad-pablo','sad-pablo-escobar',(0,0,1,.5),'','',['sad'],'sad lonely เศร้า เหงา รอ'),
('is-this-a-pigeon','is-this-a-pigeon',None,'','IS THIS A PIGEON?',['shocked'],'confused งง what อะไร'),
('roll-safe','roll-safe-think-about-it',None,'','CAN\'T BE LATE IF YOU DON\'T SHOW UP',['work'],'think smart คิด ฉลาด ได้ ok'),
('captain-now','i-m-the-captain-now',None,'','',['work'],'boss captain หัวหน้า'),
('none-of-my-business','but-that-s-none-of-my-business',None,'','BUT THAT\'S NONE OF MY BUSINESS',['agree'],'gossip ไม่ยุ่ง เผือก tea'),
('trade-offer','trade-offer',None,'','',['work','agree'],'deal offer ดีล ข้อเสนอ ok'),
('always-has-been','always-has-been',None,'WAIT, IT\'S ALL...?','ALWAYS HAS BEEN',['agree','shocked'],'wait always จริง เดี๋ยวก่อน'),
('change-my-mind','change-my-mind',None,'','CHANGE MY MIND',['disagree'],'opinion เถียง เห็นด้วย ไม่'),
('getting-paid','you-guys-are-getting-paid',None,'','YOU GUYS ARE GETTING PAID?',['payday','broke','work'],'paid salary เงินเดือน เงินหมด'),
('oprah-you-get-a','oprah-you-get-a',(0,0,1,.5),'YOU GET A CAR!','',['happy','birthday','payday'],'gift give แจก ของขวัญ'),
('absolute-cinema','absolute-cinema',None,'','ABSOLUTE CINEMA',['happy','agree'],'great amazing เก่ง ปัง เยี่ยม'),
('panik','panik-kalm-panik',(.4,0,1,.34),'','PANIK',['shocked','work'],'panic แพนิค ตกใจ'),
('kalm','panik-kalm-panik',(.4,.33,1,.67),'','KALM',['happy'],'calm ใจเย็น ok สบาย'),
('evil-kermit','evil-kermit',None,'','DO IT',['love','food'],'temptation ทำเลย จัดไป'),
('one-day-skeleton','waiting-skeleton',None,'ME WAITING','FOR YOUR REPLY',['sad','love'],'waiting รอ ตอบ reply later'),
('ight-imma-head-out','sleeping-shaq',None,'','',['happy'],'sleep good night ฝันดี นอน'),
('nobody-got-time','y-all-got-any-more-of-that',None,'Y\'ALL GOT ANY MORE OF THAT','',['food','happy'],'more อีก หิว food'),
('scientist','you-know-i-m-something-of-a-scientist-myself',None,'YOU KNOW, I\'M SOMETHING OF','A SCIENTIST MYSELF',['work'],'smart เก่ง ฉลาด'),
('thats-the-same-picture','they-re-the-same-picture',None,'','THEY\'RE THE SAME PICTURE',['agree'],'same เหมือน จริงดิ'),
('spiderman-pointing','spiderman-pointing-at-spiderman',None,'','',['agree'],'same you เหมือนกัน จริงดิ'),
('epic-handshake','epic-handshake',None,'','',['agree','thanks'],'agree เห็นด้วย deal ok ขอบคุณ'),
('monkey-puppet','monkey-puppet',None,'','',['shocked','sorry'],'awkward เอ่อ อึดอัด'),
('leo-cheers','leonardo-dicaprio-cheers',None,'','',['birthday','newyear','songkran','loykrathong','thanks','friday'],'cheers congrats ยินดีด้วย ชนแก้ว ขอบคุณ'),
('laughing-leo','laughing-leo',None,'','',['happy'],'lol 555 ขำ haha'),
('megamind-no','megamind-no-bitches',None,'','NO B*TCHES?',['sad','love'],'no single โสด'),
('fine-yoda','star-wars-yoda',None,'','',['work'],'wise yoda ฉลาด'),
('skeptical-kid','third-world-skeptical-kid',None,'SO YOU\'RE TELLING ME...','',['shocked','disagree'],'really จริงดิ สงสัย'),
('wolverine-remember','wolverine-remember',None,'','REMEMBER?',['sad','love'],'remember จำได้ไหม'),
('gus-fring','gus-fring-we-are-not-the-same','','','WE ARE NOT THE SAME',['disagree'],'different ไม่เหมือน'),
('drake-no','drake-hotline-bling',TL,'','',['disagree','no'],'no nope ไม่ ไม่เอา'),
('drake-yes','drake-hotline-bling',BL,'','',['agree','happy'],'yes ok ได้ จัดไป เอา'),
('woman-yelling','woman-yelling-at-cat',(0,0,.5,1),'','',['disagree','shocked'],'angry โกรธ พูดมาได้'),
('confused-cat','woman-yelling-at-cat',(.5,0,1,1),'','',['shocked'],'confused cat งง แมว'),
('grandma-internet','grandma-finds-the-internet',None,'','',['happy','shocked'],'internet ยาย ok'),
('distracted-bf','distracted-boyfriend',None,'','',['love'],'love รัก แฟน'),
('bike-fall','bike-fall',None,'','',['sad','sorry'],'fail พัง ขอโทษ ซวย'),
]
def fit(d,t,maxw,size):
    while size>30:
        f=ImageFont.truetype(FONT,size)
        if d.textlength(t,font=f)<=maxw: return f
        size-=4
    return f
def draw(d,t,y,anchor):
    if not t: return
    f=fit(d,t,1020,120)
    d.text((540,y),t,font=f,anchor=anchor,fill='white',stroke_width=max(4,f.size//14),stroke_fill='black')
def make(r):
    id_,tpl,crop,top,bot,occ,kw=r
    im=Image.open(f'img/{tpl}.jpg').convert('RGB')
    if crop:
        w,h=im.size;im=im.crop((int(crop[0]*w),int(crop[1]*h),int(crop[2]*w),int(crop[3]*h)))
    w,h=im.size;s=min(w,h);im=im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s)).resize((1080,1080),Image.LANCZOS)
    d=ImageDraw.Draw(im);draw(d,top,25,'ma');draw(d,bot,1055,'md')
    out=f'img/reply/{id_}.jpg';im.save(out,quality=72,optimize=True)
    cap=' / '.join(x for x in (top,bot) if x) or ORIG.get(id_,tpl.replace('-',' ').title())
    name=tpl.replace('-',' ').title()
    return dict(id='reply-'+id_,name=name,name_th='',caption_original=cap,type='reply',ratio='1:1',
      tags=['reply','ตอบแชท',name.lower(),cap.lower()]+kw.split(),occasions=['reply']+occ,rank=0,img=out,
      source='Template via Imgflip ('+tpl+'); original meme wording, no translation')
ORIG={'i-am-once-again-asking':'I am once again asking for your financial support','trade-offer':'Trade offer','captain-now':'Look at me. I\'m the captain now','ight-imma-head-out':'I sleep','surprised-pikachu':'Surprised Pikachu'}
if __name__=='__main__':
    M=[m for m in json.load(open('data/memes.json')) if m.get('type')!='reply']
    R=[make(r) for r in REPLIES]
    for i,m in enumerate(R): m['rank']=1000+i
    json.dump(M+R,open('data/memes.json','w'),ensure_ascii=False,indent=1);print(len(R),'reply memes')
