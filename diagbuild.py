from Diagram import *
import re

def breakMatrix(inp):
    '''breaks up the input LaTeX matrix into an n*k array of strings'''
    n=0
    maxk=0
    matr=[]
    for line in inp.split(r"\\"):
        matr.append([])
        n=n+1
        k=0
        for cell in line.split(r"&") :
            k=k+1
            if maxk < k:
                maxk=k
            matr[n-1].append(cell)
    return (n,maxk,matr)

def countDir(string):
    return (string.count('d')-string.count('u'),string.count('r')-string.count('l'))

uob=r"(?<!\\)\{" #unescaped opening brace {
ucb=r"(?<!\\)\}" #unescaped closing brace }
uosb=r"(?<!\\)\[" #unescaped opening square brace [
ucsb=r"(?<!\\)\]" #unescaped closing square brace ]
    
arrow_re=re.compile(r"\\arrow(" + uosb + r"(?P<style>.*?)"  +ucsb +")?"+uob + r"(?P<target>.+?)"+ucb + "(" + uosb + r"(?P<whatever>.*?)"  +ucsb + ")?" + "(" + uob + r"(?P<name>.*?)"+ucb+")?")
ar_re=re.compile(r"\\ar("       + uosb + r"(?P<style>.*?)"  +ucsb +")?"+uob + r"(?P<target>.+?)"+ucb + "(" + uosb + r"(?P<whatever>.*?)"  +ucsb + ")?" + "(" + uob + r"(?P<name>.*?)"+ucb+")?")

def parseCell(cell):
    '''returns (objName,[(r1,d1,morphName1,style1),(r2,d2,morphName2,style2),...])'''
    '''expects format such as \Pi \ar[left hook]{r}{\alpha}'''
    arrlist=[]
    while(arrow_re.search(cell)):
        match=arrow_re.search(cell)
        cell=cell[:match.start()] + cell[match.end():]
        direction=countDir(match.group('target'))
        style=match.group('style')
        arrlist.append((direction[0],direction[1],match.group('name'),style))
    while(ar_re.search(cell)):
        match=ar_re.search(cell)
        cell=cell[:match.start()] + cell[match.end():]
        direction=countDir(match.group('target'))
        style=match.group('style')
        arrlist.append((direction[0],direction[1],match.group('name'),style))
    return (cell.strip(),arrlist)
        
        
def processCellMatrix(n,k,cells):
    '''expects rectangular n*k array of LaTeX as list of lists, builds a diagram and constructs it'''

    D=Diagram()
    objs=dict()
    mrphs=dict()
    for i in xrange(n):
        for j in xrange(k):
            try:
                celldata=parseCell(cells[i][j])
            except:
                continue
            if len(celldata[0])==0:
                continue
            newname=celldata[0]
            for safety_counter in xrange(1000):
                try:
                    objs[(i,j)]=Object(D,newname)
                    break
                except AssertionError:
                    newname=newname+r"'"
            assert objs.has_key((i,j))
            for ar in celldata[1]:
                if not mrphs.has_key((i,j,i+ar[0],j+ar[1])):
                    mrphs[(i,j,i+ar[0],j+ar[1])]=[(ar[2],ar[3])]
                else:
                    mrphs[(i,j,i+ar[0],j+ar[1])].append((ar[2],ar[3]))
    #now that all objects exist we can construct morphisms
    for (i1,j1,i2,j2) in mrphs:
        if mrphs.has_key((i1,j1,i2,j2)):
            try:
                assert objs.has_key((i1,j1))
                assert objs.has_key((i2,j2))
            except:
                print "Arrow from cell " + (i1,j1) + " to cell " + (i2,j2) + " is invalid."
        if mrphs.has_key((i1,j1,i2,j2)):
            for morph in mrphs[(i1,j1,i2,j2)]:
                if morph[0]==None:               #unnamed morphism
                    Morphism(objs[(i1,j1)],objs[(i2,j2)])
                else:
                    try:
                        Morphism(objs[(i1,j1)],objs[(i2,j2)],morph[0].strip())
                    except ValueError:              #name already taken?
                        newname=morph[0].strip()+r"'"
                        print newname
                        for safety_counter in xrange(1000):#this is to avoid an infinite loop
                            try:                           #if ValueError is caused by something other than name collision
                               newmorph=Morphism(objs[(i1,j1)],objs[(i2,j2)],newname)
                               break                
                            except ValueError:
                                newname=newname+r"'"
                        raise ValueError
                            
    return D
                        
def diagBuild(diag):
    '''takes a string in tikz-cd compatible LaTeX and returns a Diagram object constructed from it'''
    '''see http://www.jmilne.org/not/Mtikz.pdf for some examples of tikz-cd syntax'''
    '''input must not include the \begin{tikzcd} and \end{tikzcd} tags'''
    brd=breakMatrix(diag)
    return processCellMatrix(brd[0],brd[1],brd[2])

def test_diagBuild():
    Dtest=r"&A\arrow[left hook]{ldd}[swap]{f}\arrow{rd}[description]{c}\arrow{rrd}[description]{d}\arrow{rrrd}[description]{e}\\&B\arrow{ld}\arrow{r}&C\arrow{r}&D\arrow{r}&E\\F"
    D=diagBuild(Dtest)
    assert D.Graph.nodes().__repr__()=="[A, C, B, E, D, F]"
    assert D.Graph.edges().__repr__()=="[(A, C), (A, E), (A, D), (A, F), (C, D), (B, C), (B, F), (D, E)]"
    return D
