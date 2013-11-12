import urllib2
import re
import chardet
import threadpool

from model import DreamObject


dream_url = "http://www.51jiemeng.com/"
page_url = "http://jiemeng.onlylady.com"
xml_enter = "&#x0D;&#x0A;"


def parse_page(object_url, object_name):
    print object_url
    print object_name
    try:
        response = urllib2.urlopen(page_url + object_url)
    except:
        print 'open page url error!'
        return

    content = response.read()
    charset = chardet.detect(content)
    encode = charset['encoding']
    encode_content = ''
    if encode == 'utf-8' or encode == 'UTF-8':
        encode_content = content
    else :
        encode_content = content.decode('gb2312','ignore').encode('utf-8')
    p = re.compile(ur'</h3></div>(.*)<p>.*?<script',re.S)
    results = p.findall(encode_content)
    

    p = re.compile(ur'<p>(.*?)</p>')
    result_array = p.findall(results[0])

    result_string = result_array[0]
    for i in result_array[1:]:
        if ('copy' not in i):
            result_string = result_string + xml_enter + i

    dream = DreamObject()
    dream.dream_name = object_name
    print object_name
    dream.dream_content = result_string
    print result_string

    dream.save()

class Dream(object):
    


    def get_all_objects(self):
        try:
            response = urllib2.urlopen(dream_url)
        except:
            print 'open url error!'
            return

        content = response.read()
        
        charset = chardet.detect(content)

        encode = charset['encoding']
        encode_content = ''
        if encode == 'utf-8' or encode == 'UTF-8':
            encode_content = content
        else :
            encode_content = content.decode('gb2312','ignore').encode('utf-8')

        p = re.compile(r'href="' + page_url + '([^\s]*?)">(.*?)</a>')
        object_pages = p.findall(encode_content)
        dream_objects = []
        for object_page in object_pages:
            dream_objects.append(((), {'object_url': object_page[0], 'object_name': object_page[1] }))
        
        #parse_page(object_pages[0])

        pool = threadpool.ThreadPool(5)
        requests = threadpool.makeRequests(parse_page, dream_objects)
        [pool.putRequest(req) for req in requests]
        pool.wait()

a = Dream()
a.get_all_objects()
