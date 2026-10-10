"""Generate 1:1 reply memes (1080x1080) from img/ templates and append to data/memes.json.
Usage: python3 tools/make_reply_memes.py   (needs Pillow with raqm + Kanit-Bold.ttf)
Edit REPLIES below: (id, template, crop(x0,y0,x1,y1 as 0-1 fractions) or None, caption_th, caption_en, occasions, keywords)"""
import json,os
from PIL import Image,ImageDraw,ImageFont
FONT=os.environ.get('FONT','/usr/share/fonts/truetype/sand-box/google/Kanit/Kanit-Bold.ttf')
T=(0,0,.5,.5);B=(0,.5,.5,1)
REPLIES=[
('noted','roll-safe-think-about-it',None,'ได้ครับ / ได้ค่ะ','Noted',['work'],'noted ok ได้ รับทราบ yes'),
('lol','laughing-leo',None,'555+','LOL',['happy'],'lol haha ขำ ตลก 555'),
('wait','megamind-peeking',None,'เดี๋ยวก่อน','Wait...',['shocked'],'wait hold on เดี๋ยว'),
('thanks','tuxedo-winnie-the-pooh',(0,.5,.55,1),'ขอบคุณครับ','Thank you',['thanks'],'thanks thank you ขอบคุณ'),
('confused','is-this-a-pigeon',None,'งง','Confused',['shocked'],'confused งง what huh'),
('ok-go','drake-hotline-bling',B,'OK จัดไป','Let\'s go!',['agree','happy'],'ok yes go จัดไป เอา'),
('nope','drake-hotline-bling',T,'ไม่เอา','Nope',['disagree','no'],'no nope ไม่ ไม่เอา'),
('cant','this-is-fine',(0,0,.5,1),'ไม่ไหวแล้ว','I can\'t anymore',['work','sad','monday'],'tired cant ไม่ไหว เหนื่อย'),
('fighting','buff-doge-vs-cheems',(0,0,.5,1),'สู้ๆ','Fighting!',['work','happy'],'fighting สู้ cheer you can do it'),
('sorry','sad-pablo-escobar',(0,0,1,.5),'ขอโทษนะ','Sorry',['sorry','sad'],'sorry ขอโทษ apology'),
('so-true','spiderman-pointing-at-spiderman',None,'จริงดิ','So true',['agree'],'true same จริง ใช่ เหมือนกัน'),
('what','surprised-pikachu',None,'อะไรนะ!?','What?!',['shocked'],'what อะไร huh'),
('shocked','surprised-pikachu',None,'ตกใจหมดเลย','Shocked',['shocked'],'shocked omg ตกใจ wow'),
('agree','epic-handshake',None,'เห็นด้วย','Agree',['agree'],'agree yes เห็นด้วย deal'),
('later','sleeping-shaq',None,'เดี๋ยวตอบนะ','Reply later',['work'],'later busy เดี๋ยวตอบ'),
('omw','running-away-balloon',(0,0,1,.5),'กำลังไป!','On my way',['work'],'omw coming กำลังไป on my way'),
('hungry','inhaling-seagull',(0,.5,1,1),'หิวแล้ว','Hungry',['food'],'hungry หิว food กิน'),
('broke','bernie-i-am-once-again-asking-for-your-support',None,'เงินหมด','I\'m broke',['broke','payday'],'broke money เงินหมด จน'),
('payday','oprah-you-get-a',(0,0,1,.5),'เงินเดือนออก!','Payday!',['payday','happy'],'payday salary เงินเดือน'),
('congrats','leonardo-dicaprio-cheers',None,'ยินดีด้วย','Congrats!',['birthday','happy','newyear'],'congrats ยินดีด้วย cheers'),
('cheers','leonardo-dicaprio-cheers',None,'ชนแก้ว!','Cheers!',['friday','newyear','songkran','loykrathong'],'cheers party ปาร์ตี้ ชน'),
('hbd','oprah-you-get-a',(0,.5,1,1),'สุขสันต์วันเกิด','Happy birthday',['birthday'],'birthday hbd วันเกิด'),
('good-night','sleeping-shaq',None,'ฝันดีนะ','Good night',['love'],'good night ฝันดี นอน sleep'),
('good-morning','sleeping-shaq',None,'อรุณสวัสดิ์','Good morning',['monday','work'],'good morning อรุณสวัสดิ์ ตื่น'),
('meeting','boardroom-meeting-suggestion',(0,0,1,.5),'ประชุมอยู่','In a meeting',['work'],'meeting busy ประชุม'),
('ack','one-does-not-simply',None,'รับทราบ','Acknowledged',['work','agree'],'acknowledged noted รับทราบ ok'),
('great-job','leonardo-dicaprio-cheers',None,'เก่งมาก!','Great job!',['work','happy'],'great job good เก่ง ปัง'),
('calm','hide-the-pain-harold',None,'ใจเย็นๆ','Calm down',['work'],'calm relax ใจเย็น'),
('how-dare','woman-yelling-at-cat',(.5,0,1,1),'พูดมาได้','How dare you',['disagree','shocked'],'how dare พูดมาได้ ประชด'),
('bored','squidward-window',None,'เบื่อ','Bored',['sad','monday'],'bored เบื่อ'),
('love-you','distracted-boyfriend',None,'รักนะ','Love you',['love'],'love รัก รักนะ'),
('monday','waiting-skeleton',None,'วันจันทร์อีกแล้ว','Monday again',['monday','sad','work'],'monday จันทร์'),
('friday','tuxedo-winnie-the-pooh',(0,.5,.55,1),'ศุกร์แล้วจ้า','Friday!',['friday','happy'],'friday ศุกร์ weekend'),
('deadline','this-is-fine',(0,0,.5,1),'เดดไลน์พรุ่งนี้','Deadline tomorrow',['work'],'deadline เดดไลน์ งาน'),
('panic','panik-kalm-panik',None,'แพนิค','Panic',['shocked','work'],'panic แพนิค'),
('thinking','roll-safe-think-about-it',None,'คิดก่อนนะ','Let me think',['work'],'think คิด hmm'),
('suspicious','monkey-puppet',(.5,0,1,1),'เอ่อ...','Awkward...',['shocked','sorry'],'awkward เอ่อ อึดอัด แอบมอง'),
('trade','trade-offer',None,'ข้อเสนอ','Deal?',['work','agree'],'deal offer ดีล ข้อเสนอ'),
('no-way','evil-kermit',None,'ไม่จริงอ่ะ','No way',['disagree','shocked'],'no way ไม่จริง'),
('sad','grant-gustin-over-grave',None,'เศร้าเลย','So sad',['sad'],'sad เศร้า ร้องไห้ อกหัก'),
('welcome','epic-handshake',None,'ยินดีครับ','You\'re welcome',['thanks'],'welcome ยินดี ไม่เป็นไร'),
('lets-eat','y-all-got-any-more-of-that',None,'กินอะไรดี?','What to eat?',['food'],'eat food กิน หิว'),
]
def fit(d,text,maxw,size):
    while size>20:
        f=ImageFont.truetype(FONT,size)
        if d.textlength(text,font=f)<=maxw: return f
        size-=4
    return f
def make(r):
    id_,tpl,crop,th,en,occ,kw=r
    im=Image.open(f'img/{tpl}.jpg').convert('RGB')
    if crop:
        w,h=im.size;im=im.crop((int(crop[0]*w),int(crop[1]*h),int(crop[2]*w),int(crop[3]*h)))
    w,h=im.size;s=min(w,h);im=im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s)).resize((1080,1080),Image.LANCZOS)
    d=ImageDraw.Draw(im)
    f=fit(d,th,1000,150);fe=fit(d,en,900,64)
    # Thai at bottom with English below
    bb=d.textbbox((540,0),th,font=f,anchor='ma')
    hth=bb[3]-bb[1]
    y_en=1080-40; d.text((540,y_en),en,font=fe,anchor='md',fill='white',stroke_width=5,stroke_fill='black')
    d.text((540,y_en-fe.size-20),th,font=f,anchor='md',fill='white',stroke_width=9,stroke_fill='black')
    out=f'img/reply/{id_}.jpg';im.save(out,quality=72,optimize=True)
    return dict(id='reply-'+id_,name=en,name_th=th,caption_th=th,caption_en=en,type='reply',ratio='1:1',
      tags=['reply','ตอบแชท']+kw.split(),occasions=['reply']+occ,rank=0,img=out,source='Template via Imgflip ('+tpl+'); caption by Meme Library')
if __name__=='__main__':
    M=[m for m in json.load(open('data/memes.json')) if m.get('type')!='reply']
    R=[make(r) for r in REPLIES]
    for i,m in enumerate(R): m['rank']=1000+i
    json.dump(M+R,open('data/memes.json','w'),ensure_ascii=False,indent=1);print(len(R),'reply memes')
