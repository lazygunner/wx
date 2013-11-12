import urllib2
import re
import chardet
import threadpool

class Dream(object):
    dream_url = "http://www.51jiemeng.com/"
    page_url = "http://jiemeng.onlylady.com"
    xml_enter = "&#x0D;&#x0A;"
    
    def parse_page(self, page):
        try:
            response = urllib2.urlopen(self.page_url + page[0])
        except:
            print 'open page url error!'

        content = response.read()
        charset = chardet.detect(content)

        encode = charset['encoding']
        encode_content = ''
        if encode == 'utf-8' or encode == 'UTF-8':
            encode_content = content
        else :
            encode_content = content.decode('gb2312','ignore').encode('utf-8')
        p = re.compile(ur'</h3></div>(.*)<p><br',re.S)
        results = p.findall(encode_content)

        p = re.compile(ur'<p>(.*?)</p>')
        result_array = p.findall(results[0])

        result_string = result_array[0]
        for i in result_array[1:]:
            result_string = result_string + self.xml_enter + i




    def get_all_objects(self):
        try:
            response = urllib2.urlopen(self.dream_url)
        except:
            print 'open url error!'

        content = response.read()

        p = re.compile(r'href="' + self.page_url + '([^\s]*?)">(.*?)</a>')
        object_pages = p.findall(content)
        
        self.parse_page(object_pages[0])

        pool = threadpool.ThreadPool(5)
        requests = threadpool.makeRequests(parse_page, object_pages)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        if _debug:
            print 'finished all threads.'

a = Dream()
a.get_all_objects()
