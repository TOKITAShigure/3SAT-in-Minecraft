from src import app
from flask import render_template,request
from src import ThreeSat2Mine


#マクロ変数(定数)定義
global DEFAULT
global CLA_INPUT
DEFAULT=0 #規定値
CLA_INPUT=1 #節の入力フェーズ


#ページ管理用変数
global procedure
procedure=DEFAULT


#入力される変数の数と節の数
global var_num
global cla_num
var_num=DEFAULT
cla_num=DEFAULT


#webバックエンド定義
@app.route('/',methods=['GET','POST'])
def index():
    global procedure
    global var_num
    global cla_num
     
    #何も入力がない場合 規定状態
    if(request.method=='GET'):       
        return render_template('index.html',var_num=0,cla_num=0,result='')
    
    if(request.method=='POST'):
        
        #変数の数と節の入力
        if(procedure==DEFAULT):
            var_num=request.form['var_num']
            cla_num=request.form['cla_num']
            procedure=CLA_INPUT
            return render_template('index.html',var_num=int(var_num),cla_num=int(cla_num),result='')
        
        #節の情報の入力
        elif(procedure==CLA_INPUT):
            cla_list=[]

            #ブロック設置用インスタンス生成&メソッド実行
            T2M=ThreeSat2Mine.ThreeSat2Mine(var_num,cla_num) 
            T2M.setVariables()
            T2M.setClauses()
        
            for i in range(int(cla_num)):
                var_list=[]
            
                v1=request.form['clause'+str(i+1)+'_1']
                v1=int(v1)
                v2=request.form['clause'+str(i+1)+'_2']
                v2=int(v2)
                v3=request.form['clause'+str(i+1)+'_3']
                v3=int(v3)
                
            
                #入力された整数(変数)が正の数ならその変数を真とし,負なら偽とする
                if(v1>0 and v1<=int(var_num)):
                    var_list.append([v1,True])
                elif(v1<0 and -v1<=int(var_num)):
                    var_list.append([v1,False])
                
                if(v2>0 and v2<=int(var_num)):
                    var_list.append([v2,True])
                elif(v2<0 and -v2<=int(var_num)):
                    var_list.append([v2,False])
                
                if(v3>0 and v3<=int(var_num)):             
                    var_list.append([v3,True])
                elif(v3<0 and -v3<=int(var_num)):
                    var_list.append([v3,False])
                
                T2M.setLogic(i,var_list[0],var_list[1],var_list[2]) 
            
                cla_list.append([v1,v2,v3])
            
        
            T2M.setRedStone()
            del T2M
            
            #最終的な式の出力
            formula=''
            
            for i in range(int(cla_num)):
        
                formula+='('
    
                for j in range(3):
        
                    if(j!=2):
                        if cla_list[i][j]<=0:
                            formula+=('¬x'+str(-cla_list[i][j])+' ∨ ')
            
                        else:
                            formula+=('x'+str(cla_list[i][j])+' ∨ ')
                
                    else:
                        if cla_list[i][j]<=0:
                            formula+=('¬x'+str(-cla_list[i][j]))
            
                        else:
                            formula+=('x'+str(cla_list[i][j]))
            
                if i!=int(cla_num)-1:
                    formula+=(') ∧ ')
        
                else:
                    formula+=(') ')
                    
            #入力が終わった場合,値を規定値に戻す
            procedure=DEFAULT
            var_num=DEFAULT
            cla_num=DEFAULT
            return render_template('index.html',var_num=int(var_num),cla_num=int(cla_num),result=formula) 
        
        #エラー処理
        else:
            var_num=DEFAULT
            cla_num=DEFAULT
            procedure=DEFAULT
            
            return render_template('index.html',var_num=0,cla_num=0,result='Error')