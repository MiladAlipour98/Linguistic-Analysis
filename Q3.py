import re
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')

doc = {
    'text': "به گزارش خبرگزاری مهر،  به نقل از روسیا الیوم، عبدالله دوم پادشاه اردن و  شیخ محمد بن زائد آل نهیان رئیس امارات متحده عربی روز چهارشنبه239  پیرامون روابط دوجانبه و اوضاع منطقه رایزنی کردند. بر اساس این گزارش، شاه اردن و رئیس امارات در این دیدار که در کاخ@ الشاطی در چارچوب هماهنگی و رایزنی بین دو طرف برگزار گردید، بر عمق link  روابط تاریخی بین دو کشور و اهتمام نسبت به تحکیم آن در زمینه‌های مختلف تاکید کردند.بررسی دورنمای همکاری‌های دوجانبه و راهکارهای #توسعه آن و تاکید بر تداوم هماهنگی و رایزنی پیرامون موضوعات مختلف دارای اهمیت مشترک در راستای منافع دو کشور از دیگر محورهای مورد بحث در این دیدار اعلام شده است. #شاه اردن و رئیس امارات همچنین بر ضرورت تشدید commonتلاش‌ها برای احیای فرصت‌های تحقق صلح بر اساس راهکار دو دولتی و توقف تمام اقدامات غیرقانونی رژیم صهیونیستی که به آن ضربه می‌زند، تاکید کردند.@mehrnewsلینک خبر: https://www.mehrnews.com/news/5673991/"
}

resp = es.index(index="qus3", id=1, document=doc)
print(resp['result'])


res = es.get(index="qus3", id=1)
data = res['_source']
content = data['text']

def extract_hashtags(text):
    hashtag_list = []
    sw=0
    for word in text.split():  
        if word[0] == '#':       
            sw=1
            hashtag_list.append(word[1:])
    if sw==1: 
       return hashtag_list
    if sw==0: 
       return 0

def english(text):
    w=[]
    sw=0
    words=text.split()
    for word in words:
       line = re.sub(r"[^A-Za-z ]", "", word.strip())
       if line!="":
           sw=1
           w.append(line)
    if sw==1: 
       return w
    if sw==0: 
       return 0

def extract_mention(text):
    sw=0
    mention_list = []
    for word in text.split():    
        if word[0] == '@':       
            sw=1
            mention_list.append(word[1:])
    if sw==1: 
       return mention_list
    if sw==0: 
       return 0
  
def Find(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)
    if url!=[]:
       return [x[0] for x in url]
    else :
        return 0
    
a=[]
b=[]
c=[]
k=[]
x=Find(str(content))
a.append(x)
x=extract_hashtags(str(content))
b.append(x)
x=extract_mention(str(content))
c.append(x)
x=english(str(content))
k.append(x)

print('links :')
for i in a:
      print (i)
print('Hashtags(#) :')
for i in b:
      print (i)
print('Mentions(@) :')
for i in c:
      print (i)
print('English :')
for i in k:
      print (i)

 
num=0
num+=1
doc = {
 'links':a,
 'Hashtags(#)':b,
 'Mentions(@)':c,
 'English':k
     }

resp = es.index(index="qus3-edited", id=num, document=doc)
print(resp['result'])