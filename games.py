import rand

class Game(object):
    state = 'before_start'
    name = ''
    point = 0


class GuessNum(Game):
    self.name = 'guess_num'
    num = 0
    count = 0

    def before_start():
        self.state = 'before_start'

    def start():
        self.state = 'start'
        self.num = rand(9999)
    
    def restart():
        self.count = 0
        self.num = 0
        self.start()
    
    def game_routine(guess = 0):
        
        if self.state == 'before_start':
            self.start()
            return 'Please guess your number!'
        elif self.state == 'start':
            if guess > self.num:
                count = count + 1
                return 'big'
            elif guess < self.num:
                count = count + 1
                return 'small'
            else:
                
                state = 'finished'
                return 'Congraduations!'
        else:
            self.restart()
            return 'Please guess your number!'



