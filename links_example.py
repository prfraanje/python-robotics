from links import * 
from time import sleep

scene = display(title='Test visualization',center=(0,0,0),forward=(0,0,-1),up=(0,1,0),background=visual.color.background,range=2)
scene.fov = 0.01 # mimic orthographic projection

#scene.camera(center=[0,0,0],forward = [-1,-1,-1],up=[0,0,1])

scale = 1;
F0 = frame([0,0,0],label='0, joint 1',scale=scale)

# single parameters: 
#L1 = link(F0,a=0,alpha=90,d=1,theta=0,q=30,joint='r',label='1, joint 2',scale=1,unit='deg') 
#L1.frame.axis.visible = True 
#L2 = link(L1.frame,a=1,alpha=90,d=0,theta=60,q=0,joint='r',label='2, joint 3',scale=1,unit='deg') 
#L3 = link(L2.frame,a=0,alpha=00,d=0,theta=0,q=1,joint='p',label='2, joint 3',scale=1,unit='deg') 


L1 = link(F0,a=1,alpha=-90,d=0,theta=0,q=45,joint='r',label='1, joint 2',scale=1,unit='deg') 


L2 = link(L1.frame,a=1,alpha=0,d=0,theta=0,q=.5,joint='p',label='2, joint 3',scale=1,unit='deg') 



