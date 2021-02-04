class node:
    def __init__(self,_r,_c):
        self.right=self
        self.left=self
        self.up=self
        self.down=self
        self.r=_r
        self.c=_c
        self.remove=False
        self.n=0
    def disconnectH(self):
        left=self.left
        right=self.right
        if(left):left.right=right
        if(right):right.left=left
        return self
    def reconnectH(self):
        left=self.left
        right=self.right
        if(left):left.right=self
        if(right):right.left=self
    def disconnectV(self):
        up=self.up
        down=self.down
        if(up):up.down=down
        if(down):down.up=up
    def reconnectV(self):
        up=self.up
        down=self.down
        if(up):up.down=self
        if(down):down.up=self
    def addUp(self,no):
        if(not no):return
        up=self.up
        no.up=up
        if(up):up.down=no # for trace
        self.up=no
        no.down=self
    def addLeft(self,no):
        if(not no):return
        left=self.left
        no.left=left
        if(left):left.right=no # for trace
        self.left=no
        no.right=self
    def notHead(self):
        if(self.r==-1):return False
        if(self.c==-1):return False
        return True
    def isHead(self):
        if(self.r==-1):return True
        if(self.c==-1):return True
        return False
    def isPivot(self):
        if(self.r!=-1):return False
        if(self.c!=-1):return False
        return True
    def notPivot(self):
        if(self.r!=-1):return True
        if(self.c!=-1):return True
        return False

class SparseMatrix:
    def __init__(self,condition_count):
        self.__cons=[node(-1,c) for c in range(condition_count)]
        self.__pivot=node(-1,-1)
        self.__sels={}
        for con in self.__cons:
            self.__pivot.addLeft(con)
        

    def set(self,_r,_cons):
        self.__pivot.addUp(node(_r,-1))
        if(_r in self.__sels):
            now=self.__sels[_r].right
            while(now.notHead()):
                now.disconnectV()
                now.c.n-=1
                now=now.right

        self.__sels[_r]=self.__pivot.up
        for c in _cons:
            now=node(self.__pivot.up,self.__cons[c])
            self.__cons[c].n+=1
            self.__pivot.up.addLeft(now)
            self.__cons[c].addUp(now)

    def sets(self,dict):
         for key in dict:
            self.set(key,dict[key])

    def __fill(headc):
        headc.remove=True
        headc.disconnectH()
        now=headc.down
        while(now.notHead()):
            now.r.remove=True
            left=now.left
            while(left.notHead()):
                left.disconnectV()
                left=left.left
            right=now.right
            while(right.notHead()):
                right.disconnectV()
                right=right.right
            now=now.down

    def __unfill(headc):
        headc.remove=False
        headc.reconnectH()
        now=headc.up
        while(now.notHead()):
            now.r.remove=False
            left=now.left
            while(left.notHead()):
                left.reconnectV()
                left=left.left
            right=now.right
            while(right.notHead()):
                right.reconnectV()
                right=right.right
            now=now.up

    def __select(headr):
        now=headr.right
        while(now.notHead()):
            SparseMatrix.__fill(now.c)
            now=now.right

    def __unselect(headr):
        now=headr.left
        while(now.notHead()):
            SparseMatrix.__unfill(now.c)
            now=now.left

    def dance(self):
        self.__solutions=[]
        self.__dance([])
        return self.__solutions.copy()
        
    def __dance(self,path):
        tmp=self.__pivot.right
        if(tmp.isPivot()):
            self.__solutions.append(path.copy())
            return
        now=tmp.down
        if(now.isHead()):
            return
        while(now.notHead()):
            SparseMatrix.__select(now.r)
            path.append(now.r.r)
            self.__dance(path)
            path.pop()
            SparseMatrix.__unselect(now.r)
            now=now.down

    def select(self,*key_sels):
        for key_sel in key_sels:
            no=self.__sels[key_sel]
            if(not no.remove):SparseMatrix.__select(no)

    def fill(self,*icons):
        for icon in icons:
            no=self.__cons[icon]
            if(not no.remove):SparseMatrix.__fill(no)

    def sort(self):
        newpivot=node(-1,-1)
        pivot=self.__pivot
        while(pivot.right.notPivot()):
            now=pivot.right
            best=now
            while(now.notPivot()):
                if(now.n<best.n):
                    best=now
                now=now.right
            newpivot.addLeft(best.disconnectH())
        newpivot.addLeft(pivot)
        newpivot.disconnectH()