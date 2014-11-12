class Dummy:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return 'value is {}\n'.format(self.val)



if __name__ == '__main__':
    d = eval('Dummy(5)')
    print(d)
 
