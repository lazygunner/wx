# coding:utf-8
from model import *
import re


def replace_newline(ori_str):
    ori_str = ori_str.replace(u"&#x0D;&#x0A;", u"\n")
    ori_str = ori_str.replace(u'&mdash;', u'-')
    ori_str = ori_str.replace(u'&middot;', u'*')
    ori_str = ori_str.replace(u'&hellip;', u'')
    ori_str = ori_str.replace(u'<br />;', u'')
    ori_str = ori_str.replace(u'&nbsp;', u'')

    p = re.compile('<span.*?>(.*?)</span>')
    ori_str = p.sub(r'\1', ori_str)

    print ori_str
    return ori_str
    

def fix_all():
    objects = DreamObject.objects()
    for obj in objects:
        print obj.dream_content
        print '>'
        obj.dream_content = replace_newline(obj.dream_content)
        obj.save()

def test():
    s = u"【梦里的兄弟姐妹很团结】表示家庭和睦，经济稳定。　　\n【男人梦见姐妹】可能象征你内心有情感秘密。\n【女人梦见姐妹】还可能暗示你和家人不和。<span style=\"font-size: 12px;\">　　</span>\n<span style=\"font-size: 12px;\">【男人梦见兄弟】可能暗示你和家人不和。　　</span>\n<span style=\"font-size: 12px;\">【女人梦见兄弟】表示家庭团结。</span>\n【梦见自己和兄弟或姐妹出去游玩】可能预示你将因为志趣相投而结交新朋友，并有机会成为知己。\n【梦见家里兄弟姐妹聚集一起或共同旅行】可能预示家庭内将出现分歧，或面临困境。　　\n【梦见兄弟姐妹共处一条船上】预示家庭将要面临困境，蒙受损失。\n【梦见和自己和兄弟姐妹快乐地玩耍】可能提示你家中会有纠纷发生，要念及亲情友爱，融洽沟通；另一方面，也可能预示会有家人生病，需小心注意家人的身体健康。\n【梦见自己与兄弟姐妹合力做某些事情】表示工作或学习瞧去取得显著进步。　　\n【梦里兄弟姐妹聚集在一起分配家里财物】预示父母会遭遇变故，或家人将发生不吉利的事。\n【梦见自己和兄弟姐妹争吵】好事，预示你可能会得到意外之财，发财致富。\n【梦见自己和兄弟姐妹分别远离】预示在个人感情方面你将取得显著进展，在感情上对家庭的依赖将会减少，心中会有新的寄托。\n【梦见兄弟姐妹结婚】预示梦里结婚的那个兄弟姐妹，可能会发生不吉利的事。\n【梦中看到自己的兄弟穷困潦倒】处境落魄，意味着你可能会遇到不幸，或是经历严重的挫折、损失。\n【梦见兄弟姐妹死了】可能只是表示你现在和他们关系良好，相处愉快。\n【梦见兄弟姐妹发生交通意外】一方面，表示可能现在你周围存在竞争，你希望竞争者尽早消失；另一方面，也可能暗示梦里的兄弟姐妹，实际上真有可能发生事故。\n【梦见兄弟姐妹患病或肇事】预示家庭会遇到困境，经历忧患。"
    print s
    p = re.compile('<span.*?>(.*?)</span>')
    b = p.sub(r'\1', s)
    print b
#test()
fix_all()
