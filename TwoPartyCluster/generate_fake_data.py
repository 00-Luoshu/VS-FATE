# and its running bash command is python generate.py filename size
# I put the file in fate/example/generate

import sys
import os

sourcepath="../data/"
# sourcepath=""
def generate(filename,size):
    sourcefile=os.path.join(sourcepath,filename)
    with open(sourcefile,'r') as rf:
        sourceContent=rf.read()
        sourceContent=sourceContent.rstrip("\n")
        sourceContent=sourceContent.split("\n")
        firstline=sourceContent[0]
        sourceContent=sourceContent[1:]
    with open(filename,'w') as wf:
        wf.write(firstline+"\n")
        for i in range(size):
            towrite=[]
            for content in sourceContent:
                item=content.split(",")
                item[0]=str(i+1)+"0101"+item[0]
                towrite.append(",".join(item))
                # towrite.append(item[0])
            towrite="\n".join(towrite)
            wf.write(towrite)
            wf.write("\n")
if __name__ == '__main__':
    name=sys.argv[1]
    size=sys.argv[2]
    generate(name,int(size))