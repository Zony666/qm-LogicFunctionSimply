# step：
# 	1、将最小项转化成二进制编码表
# 	2、将二进制编码表写入合并表
# 	3、合并合并表
# 	4、如果无法继续合并则继续，否则返回step3
# 	5、通过列表法选择最小乘积项
# 	6、将剩余乘积项化简
# 	7、如果无法继续化简则继续，否则返回step6
# 	8、输出化简后的最小项
import numpy as np
import sys

class qm():
    # num_virable:变量名个数，varname:变量名列表，minterms:最小项代号，irrterms:无关项代号   
    def __init__(self,num_virable,varname:list,minterms:list,irrterms:list=None):
        # T记录合并过程产生的表
        self.T=[]
        self.varname=varname
        self.irr=irrterms
        # G0初始表
        self.G0={}
        self.mins=minterms
        # 初始化表
        if irrterms:
            allterms=self.trans2bin(num_virable,minterms+irrterms)
        else:
            allterms=self.trans2bin(num_virable,minterms)
        for minterm in allterms:
            num1=self.get1num(minterm[1])
            if num1 not in self.G0.keys():
                self.G0[num1]=[]
            # 0 待定，1已合并，-1 未合并
            self.G0[num1].append([[minterm[0]],minterm[1],0])  
    #合并产生新表
    def __merge__(self,G):
        newg = {}
        t=[]
        num=0
        gids=list(G.keys())
        gids.sort()
        for gid in gids[0:-1]:
            if gid+1 not in gids:
                for minc in G[gid]:
                    minc[2]=-1
                continue
            for minc in G[gid]:
                for minn in G[gid+1]:
                    minvec=self.cmp1d(minc[1],minn[1])
                    if minvec:
                        minc[2]=1
                        minn[2]=1

                        num=self.get1num(minvec)
                        if num not in newg.keys():
                            newg[num]=[]
                        newg[num].append([minc[0]+minn[0],minvec,0])  
                        newg[num]=self.delrepeat(newg[num])  
                    else:
                        if minc[2]==0:
                            minc[2]=-1
                        continue
        return newg
    # 判断合并是否结束
    def judge(self,tg:dict):
        num=0
        tnum=0
        for gid in tg.keys():
            for minc in tg[gid]:
                tnum+=1
                if minc[2]==-1:
                    num+=1
        if num==tnum:
            return False
        else:
            return True
    # 删除重复项
    def delrepeat(self,g:list):
        gc=g.copy()
        ng=[]
        for i in range(len(gc)):
            gc[i][0]=set(gc[i][0])
        for d in gc:
            if d not in ng:
                ng.append(d)
        for i in range(len(ng)):
            ng[i][0]=list(ng[i][0])
               
        return ng
    # 合并过程
    def combine(self):
        g1=self.__merge__(self.G0)
        self.T.append(self.G0)
        t=g1.copy()
        if self.judge(self.G0):
            while True:
                n=self.__merge__(t)
                self.T.append(t)
                if len(n)==0:
                    break
                if self.judge(t):
                    t=n
                else:
                    break
    # 转二进制
    def trans2bin(self,num_virable,vals:list):
        res=[]
        for val in vals:
            v=bin(int(val)).replace('0b','')
            r=v.zfill(num_virable)
            res.append([val,r])
        return res
    # 获取‘1’的数量
    def get1num(self,bindata):
        num=0
        for i in bindata:
            if i=='1':
                num+=1
        return num
    # 比较两二进制数据不同
    def cmp1d(self,bindata1,bindata2):
        num=0
        nbindata=''
        for i,data in enumerate(bindata1):
            if bindata2[i]!=data:
                num+=1
                nbindata+='-'
            else:
                nbindata+=data
        if num==1:
            return nbindata
    # 素项表构造并划线
    def getPrimeTable(self):
        primeterm=[]
        # print(self.T)
        for t in self.T:
            if t:
                for gid in t.keys():
                    for minc in t[gid]:
                        if minc[2]==-1 or minc[2]==0:
                            if self.irr:
                                if not set(minc[0])<set(self.irr):
                                    primeterm.append(minc[0:2])
        # print(primeterm)
        allprimin=[]
        for t in primeterm:
            allprimin+=t[0]
        
        prinum={}
        s=set(allprimin)
        for i in s:
            c=allprimin.count(i)
            prinum[i]=c
        # print(prinum)
        # 单项位置
        pric=[]
        prir=[]
        if 1 in prinum.values():
            for d in range(len(prinum)):
                if list(prinum.values())[d]==1:
                    minv=list(prinum.keys())[d]
                    if minv in self.mins:
                        pric.append(self.mins.index(minv))
                    
                    for i in range(len(primeterm)):
                        if minv in primeterm[i][0]:
                            prir.append(i)
        # print(pric,prir)
        else:
            pass
        
        # 素项表
        primet=np.zeros([len(primeterm),len(self.mins)])
        for i in range(len(primeterm)):
            for j in range(len(self.mins)):
                for t in primeterm[i][0]:
                    if t==self.mins[j]:
                        primet[i][j]=1
        # print(primet)
        prirs=set(prir)
        for r in prirs:
            for i in range(len(self.mins)):
                if primet[r][i]==1:
                    for j in range(len(primeterm)):
                        if primet[j][i]==1:
                            primet[j][i]=2
        # print(primet)
        ltr=[]
        for i in range(len(primeterm)):
            for j in range(len(self.mins)):
                if primet[i][j]==1:
                    if 2 in primet[i,:]:
                        ltr.append(i)
                        for k in range(len(primeterm)):
                            if primet[k][j]==1:
                                primet[k][j]=2
        # print(primet)
        ridx=list(prirs)+ltr
        r=[]
        for i in ridx:
            r.append(primeterm[i][1])
        return r
    # 替换变量字符
    def translate(self,r:list[str]):
        res=''
        fname=[s+'\'' for s in self.varname]
        name=self.varname     
        for ri in r:
            tri=''
            for i in range(len(ri)):
                if ri[i]=='0':
                    
                    tri+=fname[i]
                if ri[i]=='1':
                   
                    tri+=name[i]    
                if ri[i]=='-':
                    tri+=''
            res+=('+'+tri)
        return res[1:]      
    # 输出化简结果
    def simply(self):
        self.combine()
        r=self.getPrimeTable()
        return r


if __name__ =='__main__':      

    args=sys.argv[1:]
    if args[0]:
        if args[0]=='help':
            print('qm.py 变量个数 变量名称 最小项下标-----(,分隔)')
            exit()
        else:
            varname=args[0].split(',')
            varnum=len(varname)
    if len(args)<2:
        print('请输入完整参数（help 查看使用帮助）')
        exit()
    if args[1]:
        mins=args[1]
        mins=mins.split(',')
        minw=[int(i) for i in mins]
        minterm=minw
    
    if len(args)==3:
        irrt=args[2]
        irrt=irrt.split(',')
        irret=[int(i) for i in irrt]
        irreleventTerm=irret
        g=qm(varnum,varname,minterm,irreleventTerm)       
    else:
        g=qm(varnum,varname,minterm)
        
    print(g.translate(g.simply()))

