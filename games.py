#coding:utf-8
import random

class Game(object):
    state = 'before_start'
    name = ''
    point = 0


class GuessNum(Game):
    name = 'guess_num'
    num = 0
    count = 0
    def __init__(self, num=0, count=0, state='before_start'):
        self.num = num
        self.count = count
        self.state = state

    def before_start(self):
        self.state = 'before_start'

    def start(self):
        self.state = 'start'
        self.num = random.randint(0,9999)
    
    def restart(self):
        self.count = 0
        self.num = 0
        self.start()
    
    def game_routine(self,guess = 0):
        if self.state == 'before_start':
            self.start()
            return u'好吧开始猜吧！'
        elif self.state == 'start':
            if guess > self.num:
                self.count = self.count + 1
                if (guess - self.num) > 1000:
                    return u'也太大了，请不要不暴露你的体重！'
                return '大了！不过也快了！'
            elif guess < self.num:
                self.count = self.count + 1
                if (self.num - guess) > 1000:
                    return u'忒小了，请不要暴露你的尺寸！'
                return u'小了，不过接近了！'
            else:
                self.count = self.count + 1
                self.state = 'finished'
                return u'恭喜你!猜对了!一共用了%d次' % self.count
        else:
            self.restart()
            return u'好吧开始猜吧！！'



