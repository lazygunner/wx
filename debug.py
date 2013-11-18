
def save_text(text):
    file = open('debug.txt', 'a+')
    file.write(text)
    file.write('\n')
    file.close
