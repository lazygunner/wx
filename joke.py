import requests
import re
import threadpool
from model import Duanzi

duanzi_uri = 'http://xiaohua.zol.com.cn/new/'

def get_duanzi(page_id):
    r = requests.get(duanzi_uri + page_id + '.html')
    if r.status_code == 404:
        return None

    p = re.compile(r'<div.*?summary-text.*?>(.*?)</div>', re.S)
    duanzis = p.findall(r.text)
    
    if(len(duanzis) == 0):
        return None

    for duanzi in duanzis:
        duanzi=duanzi.replace('<p>', '')
        duanzi=duanzi.replace('</p>', '\n')
        duanzi=duanzi.replace('&nbsp;', ' ')
        print duanzi
        d = Duanzi()
        d.page = int(page_id)
        duanzi = duanzi.replace('<br />', '')
        d.content = duanzi.encode('utf-8')
        d.save()

def get_new():
    
    array = [((), {'page_id':str(i)}) for i in range(1, 1251)]

    pool = threadpool.ThreadPool(5)
    p_requests = threadpool.makeRequests(get_duanzi, array)
    [pool.putRequest(req) for req in p_requests]
    pool.wait()
    print 'finished'
get_new()    
