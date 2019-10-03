import http.client
import codecs
import re
import os.path

resultlink = re.compile(
    '<a href="([a-zA-Z/]+Resultat[0-9]+.html)"',re.IGNORECASE)
anylink = re.compile('<a href="([\w]+.html)',re.IGNORECASE)


class Crawler:
    def __init__(self, connection, url, searchFor = anylink):
        self.connection = connection
        self.path = os.path.dirname(url).replace('\\', '/')
        self.file = os.path.basename(url)
        self.url = url
        self.searchFor = searchFor

    def search(self):
        #print("requesting", self.url)
        self.connection.request("GET", self.url)
        r1 = self.connection.getresponse()
        #print(r1.status, r1.reason)
        data = codecs.decode(r1.read(),'latin-1')
        #print(data)
        allLinks = self.searchFor.findall(data)
        #print('found links:', allLinks)
        res = []
        for link in allLinks:
            newLink =os.path.normpath(
                os.path.join(self.path, link)).replace('\\','/')
            res.append(newLink)
        self.children =  res
        return res
        
    def getChildTree(self, taken):
        self.search()
        res = [self]
        for link in self.children:
            if not link in taken:
                taken.append(link)
                childTree = Crawler(self.connection, link).getChildTree(taken)
                res.append(childTree)
        return res


def printTreeLink(tree, level):
    res = ''
    if level == 0:
        pass
        #print(tree[0])
    if isinstance(tree[0], Crawler):
        res = res + '{}{}\n'.format('  '*level, os.path.basename(tree[0].url))
    else:
        res = res + printTreeLink(tree[0], level + 1)
    if len(tree) > 1:
        res = res + printTreeLink(tree[1:], level)
    return res


def getAllFiles():
    conn = http.client.HTTPConnection("islevbridge.dk")
    resultFiles = Crawler(
        conn, "/Resultat/Klub1/KlubTurn.html", resultlink).search()
    print('found ',len(resultFiles), 'resultFiles')
    resultFiles.sort()
    resLinks = resultFiles[25:50]


    tree = []
    taken = []
    for link in resLinks:
        print(link)
        tree.extend(Crawler(conn, link).getChildTree(taken))

    print(printTreeLink(tree, 0))

    #f = open('allIslev.txt','w')
    #
    #f.write(printTreeLink(tree, 0))
    #f.close()
    
def readLog():
    f = open('allIslev.txt', 'r')
    data = f.readlines()
    #print(data)
    f.close()
    print(len(data))
    
    files = []
    record = []
    for line in data:
        #print(line)
        if line[0] != ' ':
            if len(record) > 0:
                #print('appending record')
                files.append(record)
            record = [line.strip()]
        if 'MultiBord' in line:
            record.append(line.strip())
        if 'CG1' in line:
            record.append(line.strip())
    
    print(len(record))
    for rec in files:
        print(rec)
                        
    


if __name__ == '__main__':
    #getAllFiles()
    readLog()
