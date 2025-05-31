import sys
from src.ThreeSat2Mine import ThreeSat2Mine


# 論理式の詳細の入力
var_num=input("Input the number of variables : ") # 変数の数(種類)を入力
cla_num=input("Input the number of clauses : ") # 節の数を入力

if(int(var_num)<=0 or int(cla_num)<=0): #変数,節の数は最小1
    print('----------------------------------\n')
    print("please input at least 1 for variables and clauses")
    print('\n----------------------------------\n')
    sys.exit()

cla_list=[] #最終的な式の出力用

#ブロック設置用インスタンス生成&メソッド実行
T2M=ThreeSat2Mine(var_num,cla_num) 
T2M.setVariables()
T2M.setClauses()

for i in range(int(cla_num)):
    
    print('please input clause',i+1)
    
    #節に含まれる変数の情報を入力する
    var_list=[]
    try:
        v1,v2,v3=(int(x) for x in input().split())
    
    except ValueError: #3変数が同時に入力されない場合の例外処理
        del T2M
        print('----------------------------------\n')
        print("please input 3 integers at the same time")
        print('\n----------------------------------\n')
        sys.exit()
    
    #入力された整数(変数)が正の数ならその変数を真とし,負なら偽とする
    if(v1>0 and v1<=int(var_num)):
        var_list.append([v1,True])
    elif(v1<0 and -v1<=int(var_num)):
        var_list.append([v1,False])
    else:
        del T2M
        print('----------------------------------\n')
        print("please input in range of variable")
        print('\n----------------------------------\n')
        sys.exit()
        
    if(v2>0 and v2<=int(var_num)):
        var_list.append([v2,True])
    elif(v2<0 and -v2<=int(var_num)):
        var_list.append([v2,False])
    else:
        del T2M
        print('----------------------------------\n')
        print("please input in range of variable")
        print('\n----------------------------------\n')
        sys.exit()
        
    if(v3>0 and v3<=int(var_num)):
        var_list.append([v3,True])
    elif(v3<0 and -v3<=int(var_num)):
        var_list.append([v3,False])   
    else:
        del T2M
        print('----------------------------------\n')
        print("please input in range of variable")
        print('\n----------------------------------\n')
        sys.exit()           
    
    T2M.setLogic(i,var_list[0],var_list[1],var_list[2])  
    
    cla_list.append([v1,v2,v3])

T2M.setRedStone()
del T2M

#最終的な式の出力(確認用)

print('----------------------------------\n')

for i in range(int(cla_num)):
    
    print('(',end='')
    
    for j in range(3):
        
        if(j!=2):
            if cla_list[i][j]<=0:
                print('¬x{0}'.format(-cla_list[i][j]),'∨',end=' ')
            
            else:
                print('x{0}'.format(cla_list[i][j]),'∨',end=' ')
                
        else:
            if cla_list[i][j]<=0:
                print('¬x{0}'.format(-cla_list[i][j]),end='')
            
            else:
                print('x{0}'.format(cla_list[i][j]),end='')
            
    if i!=int(cla_num)-1:
        print(')','∧',end=' ')
        
    else:
        print(')',end=' ')
        
print('\n\n----------------------------------\n')