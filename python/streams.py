
with open('hasstreams.txt', 'r') as f:
    hasstreams = set()
    f.readline()
    for line in f:
        hasstreams.add(line.strip())

def stream_check(s):
    return s in hasstreams
