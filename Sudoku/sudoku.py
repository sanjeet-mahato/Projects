import copy
def update(i,j,n):
    c[j][i]=n
    b[(i//3)*3+(j//3)][(i%3)*3+(j%3)]=n
def poss(i,j,n):
    flagpos=1
    if n in r[i]:
        flagpos=0
    if n in c[j]:
        flagpos=0
    if n in b[(i//3)*3+(j//3)]:
        flagpos=0
    if ordinates[0]==i and ordinates[1]==j and n in val:
        flagpos=0
    return flagpos
print("Enter the values line by line")
r=[]
c=[]
b=[]
stack=[]
val=[]
temp=[]
ordinates=[-1,-1]
count=0
for i in range(0,9,1):
    r.append([])
    c.append([])
    b.append([])
for i in range(0,9,1):
    s=input()
    for j in range(0,9,1):
        if s[j]==' ':
            r[i].append(0)
        else:
            r[i].append(int(s[j]))
            count+=1
        c[i].append(0)
        b[i].append(0)
for i in range(0,9,1):
    for j in range(0,9,1):
        update(i,j,r[i][j])
guess=0
popped=0
print("Please Wait...........................")
while(count<81):
    exe=0
    for i in range(0,9,1):
        for j in range(0,9,1):
            if(r[i][j]==0):
                flag=0
                poskey=0
                for key in range(1, 10, 1):
                    if poss(i,j,key)==1:
                        poskey=key
                    flag += poss(i, j, key)
                if poskey==0:
                    temp.clear()
                    temp.append(copy.deepcopy(stack.pop()))
                    r=temp[0][0]
                    count=temp[0][1]
                    ordinates=temp[0][2]
                    val=temp[0][3]
                    for x in range(0,9,1):
                        for y in range(0,9,1):
                            update(x,y,r[x][y])
                    popped=1
                    exe=1
                    continue;
                if flag == 1 or guess==1:
                    if popped == 0:
                        val.clear()
                        ordinates = [-1, -1]
                    else:
                        popped = 0
                    if guess == 1:
                        val.append(poskey)
                        ordinates.clear()
                        ordinates.append(i)
                        ordinates.append(j)
                        tempr=copy.deepcopy(r)
                        tempo=copy.deepcopy(ordinates)
                        tempval=copy.deepcopy(val)
                        stack.append([tempr,count,tempo,tempval])
                    r[i][j] = poskey
                    update(i, j, poskey)
                    exe = 1
                    count+=1
                    break
        if exe==1:
            break
    if exe==0:
        guess=1
    else:
        guess=0
print("          Solved Sudoku\n--------------------------------")
for i in range(0,9,1):
    if i%3==0 and i!=0:
        print()
    for j in range(0,9,1):
        if j%3==0 and j!=0:
            print(" ",end='')
        print(r[i][j]," ",end='')
    print()