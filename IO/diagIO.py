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
        captionstyle=match.group('whatever')
        arrlist.append((direction[0],direction[1],match.group('name'),style,captionstyle))
    while(ar_re.search(cell)):
        match=ar_re.search(cell)
        cell=cell[:match.start()] + cell[match.end():]
        direction=countDir(match.group('target'))
        style=match.group('style')
        captionstyle=match.group('whatever')
        arrlist.append((direction[0],direction[1],match.group('name'),style,captionstyle))
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
                    mrphs[(i,j,i+ar[0],j+ar[1])]=[(ar[2],ar[3],ar[4])]
                else:
                    mrphs[(i,j,i+ar[0],j+ar[1])].append((ar[2],ar[3],ar[4]))
            objs[(i,j)].gridpos=(i,j)
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
                    newmorph=Morphism(objs[(i1,j1)],objs[(i2,j2)])
                else:
                    try:
                        newmorph=Morphism(objs[(i1,j1)],objs[(i2,j2)],morph[0].strip())
                    except ValueError:              #name already taken?
                        newname=morph[0].strip()+r"'"
                        for safety_counter in xrange(1000):#this is to avoid an infinite loop
                            try:                           #if ValueError is caused by something other than name collision
                               newmorph=Morphism(objs[(i1,j1)],objs[(i2,j2)],newname)
                               break                
                            except ValueError:
                                newname=newname+r"'"
                        raise ValueError
                newmorph.style=morph[1]
                newmorph.latex=morph[0]
                newmorph.captionstyle=morph[2]
    return D
                        
def diagBuild(diag):
    '''takes a string in tikz-cd compatible LaTeX and returns a Diagram object constructed from it'''
    '''see http://www.jmilne.org/not/Mtikz.pdf for some examples of tikz-cd syntax'''
    '''input must not include the \begin{tikzcd} and \end{tikzcd} tags'''
    brd=breakMatrix(diag)
    return processCellMatrix(brd[0],brd[1],brd[2])

def Grid(D):
    '''returns (n,k,grid) where grid is an n*k grid represented by a dict where (i,j) |--> object at (i,j)th position in grid'''
    grid=dict()
    maxi=0
    maxj=0
    for obj in D.Objects:
        try:
            maxi=max(obj.gridpos[0],maxi)
            maxj=max(obj.gridpos[1],maxj)
            grid[obj.gridpos]=obj
        except:
            pass
    return (maxi,maxj,grid)

def norm(v):
    return v[0]*v[0]+v[1]*v[1]

def spiral(v):
    w=v
    incr=1
    turn=0
    drn=[1,0]
    while True:
        for s in xrange(incr):
            w=(w[0]+drn[0],w[1]+drn[1])
            yield w
        temp=drn[0]
        drn[0]=-drn[1]
        drn[1]=temp
        turn=turn+1
        if (turn % 2)==0:
            incr+=1
            
def badness(pos,neighbours):
    return sum([norm(pos-nb) for nb in neighbours])

def getNewPos(grid,meanpos):
    for pos in spiral(meanpos):
        if pos[0] >=-1 and pos[1] >= -1 and not(grid.has_key(pos)):
            return pos
        

def gridShift(D,down,right):
    for obj in D.Objects:
        if hasattr(obj,'gridpos'):
            obj.gridpos=(obj.gridpos[0]+down,obj.gridpos[1]+right)
        
def Display(obj, D):
    neighbours=[]
    Sum=(0,0)
    for x in D.Graph.neighbors(obj):
        try:
            Sum = (Sum[0]+x.gridpos[0],Sum[1]+x.gridpos[1])
        except:
            pass
    meanpos=(int(round(Sum[0])),int(round(Sum[1])))
    obj.gridpos=getNewPos(Grid(D)[2],meanpos)
    if obj.gridpos[0]<0:
        gridShift(D,1,0)
    if obj.gridpos[1]<0:
        gridShift(D,0,1)
    if not(hasattr(obj,'latex')):
        obj.latex=obj.name

def DisplayMorphism(m):
    if not(hasattr(m,'latex')):
        m.latex=m.name
    m.hide=False

def HideMorphism(m):
    m.hide=True

def Hide(obj):
    del obj.gridpos

def DisplayAll(D):
    for x in D.Objects:
        Display(x,D)

def DisplayAllMorphisms(D):
    for m in D.MorphismList:
        DisplayMorphism(m)

    
def direction(morph):
    '''returns the vector corresponding to the morphism'''
    right=morph.target.gridpos[1]-morph.source.gridpos[1]
    down=morph.target.gridpos[0]-morph.source.gridpos[0]
    if(right>0):
        if(down>0):
            return "r"*right+"d"*down
        else:
            return "r"*right+"u"*(-down)
    else:
        if(down>0):
            return "l"*(-right)+"d"*down
        else:
            return "l"*(-right)+"u"*(-down)
            
def latexDiag(D):
        (maxi,maxj,grid)=Grid(D)
        mrphs=dict()
        for morph in D.MorphismList:
            if hasattr(morph,'hide') and morph.hide==True:
                continue            #morphism is hidden
            if not(hasattr(morph.source,'gridpos')):
               continue             #source object is hidden
            if not(hasattr(morph.target,'gridpos')):
               continue             #target object is hidden
            i=morph.source.gridpos[0]
            j=morph.source.gridpos[1]
            try:
                mrphs[(i,j)].append(morph)
            except:
                mrphs[(i,j)]=[morph]
        out=""
        for i in xrange(maxi+1):
            for j in xrange(maxj+1):
                if grid.has_key((i,j)):
                    out=out+grid[(i,j)].latex + " "
                    if mrphs.has_key((i,j)):
                        offset=-(len(mrphs[(i,j)])-1)*0.5
                        for morph in mrphs[(i,j)]:
                            if direction(morph)=='':
                                continue               #we do not draw identities on the graph. TODO: draw a loop if the user really wants it
                            out=out+" "+r"\arrow"
                            out+=r"["
                            try:
                                out=out+morph.style+r","
                            except:
                                pass
                            out+=r"shift left="+str(offset)+r"]"
                            try:
                                out+=r"{"+direction(morph)+r"}"
                            except BaseException as E:
                                raise E
                            try:
                                out+=morph.captionstyle+r","
                            except:
                                pass
                            try:
                                out+=r"{"+morph.latex+"}"
                            except:
                                pass
                            offset=offset+1           #to dodge other arrows
                out=out+r" &"
            out=out+"\\\\ \n"
        return out
                
        

def test_diagBuild():
    Dtest=r"&A\arrow[dotted]{ldd}[swap]{f}\arrow{rd}[description]{c}\arrow{rrd}[description]{d}\arrow{rrrd}[description]{e}\\&B\arrow{ld}\arrow{r}&C\arrow{r}&D\arrow{r}&E\\F"
    D=diagBuild(Dtest)
    assert D.Graph.nodes().__repr__()=="[A, C, B, E, D, F]"
    assert D.Graph.edges().__repr__()=="[(A, C), (A, E), (A, D), (A, F), (C, D), (B, C), (B, F), (D, E)]"
    newm=Morphism(D['E'],D['F'])
    newm.style="dotted"
    Object(D,'G')
    Display(D['G'],D)
    Morphism(D['G'],D['A'])
    print latexDiag(D)
    return D
