#3sat問題をMinecraftに移植するコード
#コンストラクタによってインスタンスを生成した後は,必ず setVariables -> setClauses -> setLogic -> setRedStone -> デストラクタ の順に実行してください
#不正な入力の場合は,デストラクタを起動してプログラムを終了してください
#設計部分において,プレイヤーの移動できるマスについては床,できないマスについては壁と呼称します


import amulet
import os
import shutil
from amulet.api.block import Block
from amulet_nbt import StringTag
from dataclasses import dataclass


#変数ガジェット用構造体
@dataclass
class Var_Gad():
    origin_x:int 
    true_z:int
    false_z:int
    
    
#節ガジェット用構造体
@dataclass
class Cla_Gad():
    origin_x:int
    true_x:list
    false_x:list
    true:list
    false:list

    
class ThreeSat2Mine():
    #バージョンと使用するワールドの宣言
    game_version=("java",(1,21,5)); #Minecraft Java Edition ver 1.21.5
    
    
    #使用するブロックを宣言
    plank=Block("minecraft","oak_planks")
    plate=Block("minecraft","stone_pressure_plate")
    door_up=Block("minecraft","iron_door",{"half":StringTag("upper"),"facing":StringTag("east")})
    door_lo=Block("minecraft","iron_door",{"half":StringTag("lower"),"facing":StringTag("east")})
    red_x=Block("minecraft","redstone_wire",{"east":StringTag("side")})
    red_z=Block("minecraft","redstone_wire",{"north":StringTag("side")})
    red_blo=Block("minecraft","redstone_block")
    rep_pz=Block("minecraft","repeater",{"facing":StringTag("south")})
    rep_mz=Block("minecraft","repeater",{"facing":StringTag("north")})
    rep_x=Block("minecraft","repeater",{"facing":StringTag("east")})
    piston_mz=Block("minecraft","piston",{"facing":StringTag("north")})
    piston_pz=Block("minecraft","piston",{"facing":StringTag("south")})
    
    
    #先端のガジェットのx座標
    current_x=0
    
    
    #ガジェット構造体格納用リスト
    var_list=[]
    cla_list=[]
    
    
    #コンストラクタ
    def __init__(self,var_num,cla_num):
        self.var_num=var_num
        self.cla_num=cla_num
                
        #ディレクトリ内に 'OutputWorld' フォルダを生成する
        if 'OutputWorld' in [d for d in os.listdir('./')]:
            shutil.rmtree('./OutputWorld') #すでに出力フォルダがある場合は削除
            
        #ディレクトリ内の 'InputWorld' を変更するワールドのフォルダとする
        shutil.copytree('./InputWorld','./OutputWorld') 
        self.level=amulet.load_level("OutputWorld") 
        
        
    #デストラクタ
    def __del__(self):
        #デストラクタが宣言されない場合,変更が保存されないので注意
        self.level.save()
        self.level.close()
        
        
    #変数ガジェット生成メソッド
    def setVariables(self):
        for i in range(int(self.var_num)):
            
            self.var_list.append(Var_Gad(origin_x=i*13,true_z=(i+1)*-8,false_z=(i+1)*8+9))
            self.current_x+=13
            
            #基本の壁と床の設置
            for j in range(13): #x軸13マス
                
                for k in range(9): #z軸9マス
                    
                    if(j==0 or j==6 or j==12): #x軸方向の壁設置 
                        
                        if(k==2 or k==6):  
                             
                            if(j==0): #x軸が0マス目の場合,変数ガジェットの入り口とする
                                self.level.set_version_block(self.var_list[i].origin_x+j,0,k,"minecraft:overworld",self.game_version,self.plank)
                                
                            elif(j==6 or j==12): #そのマスが入り口でない場合,感圧版と鉄の扉を設置する  
                                self.level.set_version_block(self.var_list[i].origin_x+j,0,k,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.var_list[i].origin_x+j,1,k,"minecraft:overworld",self.game_version,self.door_lo)
                                self.level.set_version_block(self.var_list[i].origin_x+j,2,k,"minecraft:overworld",self.game_version,self.door_up)
                                self.level.set_version_block(self.var_list[i].origin_x+j-1,1,k,"minecraft:overworld",self.game_version,self.plate)
                                
                        else: #通常の壁設置
                            for l in range(3):
                                self.level.set_version_block(self.var_list[i].origin_x+j,l,k,"minecraft:overworld",self.game_version,self.plank)
                                
                    elif( (k==0 or k==8) or (j>=7 and k==4) ): #z軸方向の壁設置
                        
                        #レッドストーン回路用のピストン設置
                        if(j==11):
                            
                            if(k==0):
                                self.level.set_version_block(self.var_list[i].origin_x+j,0,k,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.var_list[i].origin_x+j,1,k,"minecraft:overworld",self.game_version,self.piston_mz)
                                self.level.set_version_block(self.var_list[i].origin_x+j,2,k,"minecraft:overworld",self.game_version,self.plank)
                                
                            elif(k==8):
                                self.level.set_version_block(self.var_list[i].origin_x+j,0,k,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.var_list[i].origin_x+j,1,k,"minecraft:overworld",self.game_version,self.piston_pz)
                                self.level.set_version_block(self.var_list[i].origin_x+j,2,k,"minecraft:overworld",self.game_version,self.plank)
                                
                            elif(k==4): #通常の壁設置
                                for l in range(3):
                                    self.level.set_version_block(self.var_list[i].origin_x+j,l,k,"minecraft:overworld",self.game_version,self.plank)
                        
                        else: #通常の壁設置
                            for l in range(3):
                                    self.level.set_version_block(self.var_list[i].origin_x+j,l,k,"minecraft:overworld",self.game_version,self.plank) 
                                    
                    else: #壁ではない床設置
                        self.level.set_version_block(self.var_list[i].origin_x+j,0,k,"minecraft:overworld",self.game_version,self.plank)
                                         
                    
    #節ガジェット生成メソッド   
    def setClauses(self):
        for i in range(int(self.cla_num)):
            
            self.cla_list.append(Cla_Gad(origin_x=self.current_x,true_x=[self.current_x+7,self.current_x+9,self.current_x+11],false_x=[self.current_x+7,self.current_x+9,self.current_x+11],true=[],false=[]))
            self.current_x+=13
            
            for j in range(13): #x軸13マス
                
                for k in range(9): #z軸9マス
                    
                    #基本の壁と床の設置
                    if(j==0 or j==6 or j==12): #x軸方向の壁設置
                        if( (j==0 or j==12) and (k==2 or k==6) ): #x軸0,13マス目は節ガジェット入り口および出口とする
                            self.level.set_version_block(self.cla_list[i].origin_x+j,0,k,"minecraft:overworld",self.game_version,self.plank)
                            
                        elif(j==6 and k==4): #ガジェット内の座標(6,4)だった場合,鉄の扉を設置する
                            self.level.set_version_block(self.cla_list[i].origin_x+j,0,k,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.cla_list[i].origin_x+j,1,k,"minecraft:overworld",self.game_version,self.door_lo)
                            self.level.set_version_block(self.cla_list[i].origin_x+j,2,k,"minecraft:overworld",self.game_version,self.door_up)
                            
                        else: #通常の壁設置
                            for l in range(3):
                                self.level.set_version_block(self.cla_list[i].origin_x+j,l,k,"minecraft:overworld",self.game_version,self.plank)
                                
                    elif(k==0 or k==8): #z軸方向の壁設置
                        if(j==9):#レッドストーン回路用の穴を作る
                            if(k==0):
                                self.level.set_version_block(self.cla_list[i].origin_x+j,0,k,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.cla_list[i].origin_x+j,1,k,"minecraft:overworld",self.game_version,self.rep_mz)
                                self.level.set_version_block(self.cla_list[i].origin_x+j,2,k,"minecraft:overworld",self.game_version,self.plank)  
                                
                            elif(k==8):
                                self.level.set_version_block(self.cla_list[i].origin_x+j,0,k,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.cla_list[i].origin_x+j,1,k,"minecraft:overworld",self.game_version,self.rep_pz)
                                self.level.set_version_block(self.cla_list[i].origin_x+j,2,k,"minecraft:overworld",self.game_version,self.plank)
                            
                        else: #通常の壁設置
                            for l in range(3):
                                self.level.set_version_block(self.cla_list[i].origin_x+j,l,k,"minecraft:overworld",self.game_version,self.plank)
                                
                    else: #壁ではない床設置
                        self.level.set_version_block(self.cla_list[i].origin_x+j,0,k,"minecraft:overworld",self.game_version,self.plank)
                        
                    #レッドストーン回路部設置
                    if(k==0): #true側の入力      
                        if(j==0):
                            pass
                    
                        elif(j==7 or j==11):   
                            for l in range(3):
                                self.level.set_version_block(self.cla_list[i].origin_x+j,0,-l-2,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.cla_list[i].origin_x+j,1,-l-2,"minecraft:overworld",self.game_version,self.red_z)
                            
                        elif(j==8 or j==10):
                            self.level.set_version_block(self.cla_list[i].origin_x+j,0,-2,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.cla_list[i].origin_x+j,1,-2,"minecraft:overworld",self.game_version,self.red_z)
                        
                        elif(j==9):
                            for l in range(-1,-5,-1):
                                self.level.set_version_block(self.cla_list[i].origin_x+j,0,l,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.cla_list[i].origin_x+j,1,l,"minecraft:overworld",self.game_version,self.red_z)
                            
                    if(k==8): #false側の入力   
                        if(j==7 or j==11):
                            for l in range(3):
                                self.level.set_version_block(self.cla_list[i].origin_x+j,0,k+l+2,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.cla_list[i].origin_x+j,1,k+l+2,"minecraft:overworld",self.game_version,self.red_z)
                            
                        elif(j==8 or j==10):
                            self.level.set_version_block(self.cla_list[i].origin_x+j,0,k+2,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.cla_list[i].origin_x+j,1,k+2,"minecraft:overworld",self.game_version,self.red_z)
                        
                        elif(j==9):
                            for l in range(1,5,+1):
                                self.level.set_version_block(self.cla_list[i].origin_x+j,0,k+l,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.cla_list[i].origin_x+j,1,k+l,"minecraft:overworld",self.game_version,self.red_z)
                      
                    #レッドストーン設置      
                    if(j==9)and(k>=1 and k<=7):
                        self.level.set_version_block(self.cla_list[i].origin_x+j,1,k,"minecraft:overworld",self.game_version,self.red_z)
                    
                    if(k==4)and(j>=7)and(j<=9):
                        self.level.set_version_block(self.cla_list[i].origin_x+j,1,k,"minecraft:overworld",self.game_version,self.red_x)
      
                        
    #節の設定メソッド
    def setLogic(self,num,v1,v2,v3):      
        if(v1[1]==True):
            self.cla_list[num].true.append(v1[0])   
        else: 
            self.cla_list[num].false.append(v1[0])
            
        if(v2[1]==True):
            self.cla_list[num].true.append(v2[0])
        else:
            self.cla_list[num].false.append(v2[0])
            
        if(v3[1]==True):
            self.cla_list[num].true.append(v3[0])
        else:
            self.cla_list[num].false.append(v3[0])
            
            
    #レッドストーン(制御)部分生成メソッド
    def setRedStone(self):
        #変数ガジェットから最後の節ガジェットまでレッドストーンダストを伸ばす
        for i in range(int(self.var_num)):
            
            j=7
            
            #z軸方向
            while j<self.var_list[i].false_z: #false側

                if(j==8):
                    j+=1
                    continue
                
                elif(j==9):
                    self.level.set_version_block(self.var_list[i].origin_x+11,0,j,"minecraft:overworld",self.game_version,self.plank)
                    self.level.set_version_block(self.var_list[i].origin_x+11,1,j,"minecraft:overworld",self.game_version,self.red_blo)
                    j+=1
                    
                
                elif(j==10):
                    self.level.set_version_block(self.var_list[i].origin_x+11,0,j,"minecraft:overworld",self.game_version,self.plank)
                    j+=1
        
                else:
                    
                    cross_flag=False
                    
                    for k in self.var_list: #交差するかの判定
                        
                        if(j+1==k.false_z): 
                            cross_flag=True
                            break
                    
                    if(cross_flag and j+1!=self.var_list[i].false_z): #交差
                        self.level.set_version_block(self.var_list[i].origin_x+11,1,j,"minecraft:overworld",self.game_version,self.plank)
                        self.level.set_version_block(self.var_list[i].origin_x+11,2,j,"minecraft:overworld",self.game_version,self.red_z)
                        
                        self.level.set_version_block(self.var_list[i].origin_x+11,2,j+1,"minecraft:overworld",self.game_version,self.plank)
                        self.level.set_version_block(self.var_list[i].origin_x+11,3,j+1,"minecraft:overworld",self.game_version,self.red_z)
                        
                        self.level.set_version_block(self.var_list[i].origin_x+11,1,j+2,"minecraft:overworld",self.game_version,self.plank)
                        self.level.set_version_block(self.var_list[i].origin_x+11,2,j+2,"minecraft:overworld",self.game_version,self.red_z) 
                        j+=3
         
                    
                    else: #通常
                        if(j!=0 and (j-21)%8==0): #リピーター
                            self.level.set_version_block(self.var_list[i].origin_x+11,0,j,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.var_list[i].origin_x+11,1,j,"minecraft:overworld",self.game_version,self.rep_pz)
                            j+=1
                            
                        else: #通常
                            self.level.set_version_block(self.var_list[i].origin_x+11,0,j,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.var_list[i].origin_x+11,1,j,"minecraft:overworld",self.game_version,self.red_z)
                            j+=1
                  
            j=1
                          
            while j>self.var_list[i].true_z: #true側
                
                if(j==0):
                    j-=1
                    continue
                
                elif(j==-1):
                    self.level.set_version_block(self.var_list[i].origin_x+11,0,j,"minecraft:overworld",self.game_version,self.plank)
                    self.level.set_version_block(self.var_list[i].origin_x+11,1,j,"minecraft:overworld",self.game_version,self.red_blo)
                    j-=1
                    
                elif(j==-2):
                    self.level.set_version_block(self.var_list[i].origin_x+11,0,j,"minecraft:overworld",self.game_version,self.plank)
                    j-=1
                        
                else:
                    cross_flag=False
                    
                    for k in self.var_list: #交差するかの判定
                        
                        if(j-1==k.true_z): 
                            cross_flag=True
                            break
                        
                    if(cross_flag and j-1!=self.var_list[i].true_z): #交差    
                        self.level.set_version_block(self.var_list[i].origin_x+11,1,j,"minecraft:overworld",self.game_version,self.plank)
                        self.level.set_version_block(self.var_list[i].origin_x+11,2,j,"minecraft:overworld",self.game_version,self.red_z)
                        
                        self.level.set_version_block(self.var_list[i].origin_x+11,2,j-1,"minecraft:overworld",self.game_version,self.plank)
                        self.level.set_version_block(self.var_list[i].origin_x+11,3,j-1,"minecraft:overworld",self.game_version,self.red_z)
                        
                        self.level.set_version_block(self.var_list[i].origin_x+11,1,j-2,"minecraft:overworld",self.game_version,self.plank)
                        self.level.set_version_block(self.var_list[i].origin_x+11,2,j-2,"minecraft:overworld",self.game_version,self.red_z)   
                        j-=3
                        
                    else: #通常          
                        if((j+4)%8==0):
                            self.level.set_version_block(self.var_list[i].origin_x+11,0,j,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.var_list[i].origin_x+11,1,j,"minecraft:overworld",self.game_version,self.rep_mz)
                            j-=1
                            
                        else:
                            self.level.set_version_block(self.var_list[i].origin_x+11,0,j,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.var_list[i].origin_x+11,1,j,"minecraft:overworld",self.game_version,self.red_z)
                            j-=1
                    
            #x軸方向
            for j in range(self.current_x):
                
                if((self.var_list[i].origin_x+j-15)%13==0):
                    self.level.set_version_block(self.var_list[i].origin_x+11+j,0,self.var_list[i].true_z,"minecraft:overworld",self.game_version,self.plank)
                    self.level.set_version_block(self.var_list[i].origin_x+11+j,1,self.var_list[i].true_z,"minecraft:overworld",self.game_version,self.rep_x)
                    self.level.set_version_block(self.var_list[i].origin_x+11+j,0,self.var_list[i].false_z,"minecraft:overworld",self.game_version,self.plank)  
                    self.level.set_version_block(self.var_list[i].origin_x+11+j,1,self.var_list[i].false_z,"minecraft:overworld",self.game_version,self.rep_x) 
                    
                else:
                    self.level.set_version_block(self.var_list[i].origin_x+11+j,0,self.var_list[i].true_z,"minecraft:overworld",self.game_version,self.plank)
                    self.level.set_version_block(self.var_list[i].origin_x+11+j,1,self.var_list[i].true_z,"minecraft:overworld",self.game_version,self.red_x)
                    self.level.set_version_block(self.var_list[i].origin_x+11+j,0,self.var_list[i].false_z,"minecraft:overworld",self.game_version,self.plank)  
                    self.level.set_version_block(self.var_list[i].origin_x+11+j,1,self.var_list[i].false_z,"minecraft:overworld",self.game_version,self.red_x)  
            
        #節ガジェットから変数の銅線に向けてレッドストーンダストを伸ばす        
        for i in range(int(self.cla_num)):
            
            used_num=0 #その節ガジェットに通した変数ガジェットの銅線の数(最大3)
            
            #false側
            if not self.cla_list[i].false: #false変数がない場合,スルー
                pass
            
            else:
                for j in self.cla_list[i].false:
                
                    k=13
                
                    while k<self.var_list[-j-1].false_z:
                        
                        cross_flag=False
                    
                        for l in self.var_list: #交差するかの判定
                        
                            if(k+1==l.false_z): 
                                cross_flag=True
                                break
                            
                        if(cross_flag and k+1!=self.var_list[-j-1].false_z): #交差
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],1,k,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],2,k,"minecraft:overworld",self.game_version,self.red_z)
                            
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],2,k+1,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],3,k+1,"minecraft:overworld",self.game_version,self.red_z)
                            
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],1,k+2,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],2,k+2,"minecraft:overworld",self.game_version,self.red_z)
                            
                            k+=3
                            
                        else: #通常
                            
                            if(k!=0 and (k-21)%8==0): #リピーター    
                                self.level.set_version_block(self.cla_list[i].false_x[used_num],0,k,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.cla_list[i].false_x[used_num],1,k,"minecraft:overworld",self.game_version,self.rep_mz)
                                k+=1
                                
                            else: #通常
                                self.level.set_version_block(self.cla_list[i].false_x[used_num],0,k,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.cla_list[i].false_x[used_num],1,k,"minecraft:overworld",self.game_version,self.red_z)
                                k+=1
                    
                    used_num+=1
                    
            #true側
            if not self.cla_list[i].true: #true変数がない場合,スルー
                pass
            
            else:
                for j in self.cla_list[i].true:
                    
                    k=-4
                    
                    while k>self.var_list[j-1].true_z:
                        
                        cross_flag=False
                        
                        for l in self.var_list: #交差するかの判定
                             
                            if(k-1==l.true_z):   
                                cross_flag=True
                                break
                            
                        if(cross_flag and k-1!=self.var_list[j-1].true_z): #交差
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],1,k,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],2,k,"minecraft:overworld",self.game_version,self.red_z)
                            
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],2,k-1,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],3,k-1,"minecraft:overworld",self.game_version,self.red_z)
                            
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],1,k-2,"minecraft:overworld",self.game_version,self.plank)
                            self.level.set_version_block(self.cla_list[i].false_x[used_num],2,k-2,"minecraft:overworld",self.game_version,self.red_z)           
                            k-=3
                        
                        else: #通常
                            if(k!=0 and (k+4)%8==0): #リピーター
                                self.level.set_version_block(self.cla_list[i].false_x[used_num],0,k,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.cla_list[i].false_x[used_num],1,k,"minecraft:overworld",self.game_version,self.rep_pz)
                                k-=1
    
                            else: #通常  
                                self.level.set_version_block(self.cla_list[i].false_x[used_num],0,k,"minecraft:overworld",self.game_version,self.plank)
                                self.level.set_version_block(self.cla_list[i].false_x[used_num],1,k,"minecraft:overworld",self.game_version,self.red_z)
                                k-=1
                                                
                    used_num+=1