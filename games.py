import random

class Game(object):
    state = 'before_start'
    name = ''
    point = 0


class GuessNum(Game):
    name = 'guess_num'
    num = 0
    count = 0

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
            return 'Please guess your number!'
        elif self.state == 'start':
            if guess > self.num:
                self.count = self.count + 1
                return 'big'
            elif guess < self.num:
                self.count = self.count + 1
                return 'small'
            else:
                
                selfstate = 'finished'
                return 'Congraduations!'
        else:
            self.restart()
            return 'Please guess your number!'



