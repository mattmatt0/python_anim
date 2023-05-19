def readFile(filePath):
    return [list(map(int, n.split(' '))) for n in open(filePath,'r').read().split('\n')[:-1]]
