import requests
import re
import threadpool
from model import Duanzi

duanzi_uri = 'http://duanziwang.com/'

def get_duanzi(page_id):
    r = requests.get(duanzi_uri + page_id)
    if r.status_code == 404:
        return None

    p = re.compile(r'<div.*?entry-content.*?>(.*?)</div>', re.S)
    duanzis = p.findall(r.text)
    
    if(len(duanzis) == 0):
        return None

    p = re.compile(r'<p>(.*?)</p>', re.S)
    duanzi_array = p.findall(duanzis[0])

    for duanzi in duanzi_array:
        d = Duanzi()
        d.page = int(page_id)
        duanzi = duanzi.replace('<br />;', '')
        d.content = duanzi.encode('utf-8')
        d.save()

def get_new():
    r = requests.get(duanzi_uri)
    p = re.compile(r'id="post-(\d*?)"')
    latest = int(p.findall(r.text)[0])
    begin = Duanzi.objects.order_by('-page').first()
    if begin == None:
        begin = 0
    
    array = [((), {'page_id':str(i)}) for i in range(begin, latest)]

    pool = threadpool.ThreadPool(5)
    p_requests = threadpool.makeRequests(get_duanzi, array)
    [pool.putRequest(req) for req in p_requests]
    pool.wait()
    print 'finished'
get_new()    
