from hazm import Normalizer
from hazm import sent_tokenize, Stemmer, word_tokenize, POSTagger, Lemmatizer
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')

doc = {
    'text': "به گزارش ورزش سه، النصر عربستان فردا در شرایطی در چارچوب هفته دوازدهم لیگ عربستان در سال 2023  میزبان الطایی خواهد بود که ساعاتی قبل خبری مبنی بر محرومیت دو جلسه‌ای کریستیانو رونالدو منتشر شد تا مشخص شود در صورت بخشیده نشدن این جریمه، این بازیکن نمی‌تواند زردپوشان عربستانی را در دو بازی آینده مقابل الطایی و الاهلی همراهی کند.اما این تنها مانع پیش روی النصر برای استفاده از رونالدو نیست و این باشگاه پس از پرداخت حق‌الزحمه 1 میلیون یورویی جولیانو دی پائولا، بازیکن برزیلی سابق و روی ویتوریا، مربی پرتغالی سابق خود و همچنین پرداخت حقوق بازیکنان و عوامل باشگاه، شرایط لازم برای دریافت گواهی صلاحیت مالی برای ثبت قرارداد بازیکن را دریافت خواهد کرد."
}


resp = es.index(index="qus4", id=1, document=doc)
print(resp['result'])


res = es.get(index="qus4", id=1)
data = res['_source']
content = data['text']

a=[]
normalizer = Normalizer()
print('normalize: ',normalizer.normalize(content))
a.append(normalizer.normalize(content))

stemmer = Stemmer()
lemmatizer = Lemmatizer()

# ger = POSTagger ( model = 'resources/postagger.model' )

for i in a:
    print('sentences: ',sent_tokenize(i))

    print('words: ',word_tokenize(i))
    
    f=''
    g=''
    for j in word_tokenize(i):
        print(stemmer.stem(j))
        f+= str(stemmer.stem(j))
        f+=', '
        print(lemmatizer.lemmatize(j))
        g+= str(lemmatizer.lemmatize(j))
        g+=', '

    # h=tagger.tag(word_tokenize(i))

doc1 = {
 'normalize':normalizer.normalize(content)
     }
doc2 = {
 'sentences':sent_tokenize(i)
     }
doc3 = {
 'words':word_tokenize(i)
     }
doc4 = {
 'verbs':f,
 'roots':g
     }
# doc5 = {
#  'tags':h
#      }
 
resp = es.index(index="q4-a", id=1, document=doc1)
print(resp['result'])
resp = es.index(index="q4-b", id=2, document=doc2)
print(resp['result'])
resp = es.index(index="q4-c", id=3, document=doc3)
print(resp['result'])
resp = es.index(index="q4-d", id=4, document=doc4)
print(resp['result'])
# resp = es.index(index="e", id=5, document=doc5)
# print(resp['result'])
