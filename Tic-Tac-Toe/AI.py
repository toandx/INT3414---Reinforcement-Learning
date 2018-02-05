import numpy as np
import random
from env4 import TicTacToeEnv as env
SIZE=3
def boardToInt(x):
 res=0
 for i in range(0,SIZE*SIZE):
  res=res*3+x[i]
 return(res)
def intToBoard(x):
 res=[0]*SIZE*SIZE
 i=0
 while True:
  if (x==0):
   break
  i=i+1
  res[SIZE*SIZE-i]=x%3
  x=x//3
 return(res) 
class AI():
 def __init__(self,env,player):
  self.learning_rate=0.3
  self.discount_rate=0.9
  self.PLAYER=player
  self.env=env
  self.q=np.full((3**(SIZE*SIZE),SIZE*SIZE),0.0,dtype=np.float32)
  self.reward=0
  self.status=-1
  self.back_action=0
  self.back_state=0
 def reset(self):
  self.reward=0
  self.status=-1
  self.back_action=0
  self.back_state=0
 def nextState(self):
  if ((self.env.status>0) & (self.env.status!=self.PLAYER)): # if you loss
   state=self.back_state
   action=self.back_action
   board=intToBoard(state)
   board[action]=self.PLAYER
   next_state=boardToInt(board)
   next_board=board
   self.reward=-1
   max=0
   for i in range(0,SIZE*SIZE):
    if ((next_board[i]==0) & (self.q[next_state][max]<self.q[next_state][i])):
     max=i
    if (next_board[i]==0 & next_board[max]!=0):
     max=i
   self.q[state][action]+=self.learning_rate*(self.reward+self.discount_rate*self.q[next_state,max]-self.q[state][action])
   return(self.reward,True)
  if (self.env.status==0): # if you draw
   return(0,True)
  # if game continue
  board=self.env.board
  state=boardToInt(board)
  min=-1000
  action=0
  list=[]
  for i in range(0,SIZE*SIZE):
   if ((self.q[state][i]>min) & (board[i]==0)):
    min=self.q[state][i]
  for i in range(0,SIZE*SIZE):
   if ((self.q[state][i]==min) & (board[i]==0)):
    list=list+[i]
  action=random.choice(list)
  self.status=self.env.step(action)
  self.reward=1 if (self.status==self.PLAYER) else 0
  next_board=self.env.board
  next_state=boardToInt(next_board)
  max=0
  for i in range(0,SIZE*SIZE):
   if ((next_board[i]==0) & (self.q[next_state][max]<self.q[next_state][i])):
    max=i
   if (next_board[i]==0 & next_board[max]!=0):
    max=i
  self.q[state][action]+=self.learning_rate*(self.reward+self.discount_rate*self.q[next_state,max]-self.q[state][action])
  self.back_state=state
  self.back_action=action
  return(self.reward,True) if (self.status==0) else (self.reward,False)