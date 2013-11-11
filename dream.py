import urllib2
import re

class Dream(object):
    dream_url = "http://www.51jiemeng.com/"
    def get_all_objects(self):
        try:
            response = urllib2.urlopen(self.dream_url)
        except:
            print 'open url error!'

        html = response.read()

        p = re.compile(r'href="http://jiemeng.onlylady.com(.*?)">(.*?)</a>')
        objects = p.findall(html)
        print objects

a = Dream()
a.get_all_objects()
