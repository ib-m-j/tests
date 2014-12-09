import array
import sys

class Bits:
    def __init__(self):
        self.value = 0
        self.fill = 8

    def append(self, v):
        if v<0 or v>3:
            sys.exit(0)
        self.value =  self.value | (v<<(self.fill-2))
        self.fill = self.fill - 2
        return self.fill

    def reset(self):
        self.value = 0
        self.fill = 8

    def read(self):
        if self.fill <= 8:
            res = (self.value & 0b11000000)>>6
            self.value = self.value << 2 & 0b11111111
            self.fill = self.fill + 2
            return res

res = Bits()

toadd = [1,2,0,3,1,2,3,2,1,0,0,0,2,1,0,3,2,1,0]

def makehash(values):
    res = []
    count = 0
    extra = 0
    for v in values:
        if count == 4:
            print('{:0>8b}'.format(extra))
            res.append(extra)
            count = 0
            extra = 0
        extra = extra | (v<<(6 - 2* count))
        count +=1
    if count < 4:
        print('{:0>8b}'.format(extra))
        res.append(extra)



    return bytes(res)

def readhash(hash):
    res = []
    for c in hash:
        for shift in range(6,-2,-2):
            res.append((c>>shift) & 0b11)
    return res


hash = makehash(toadd)
print(hash)

res = readhash(hash)
print(res)
