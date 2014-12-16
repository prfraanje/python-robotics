from links import *

scene = display(title='UR 5',center=(0,0,0),forward=(-1,-1,-1),up=(0,0,1),background=visual.color.background,range=5)
scene.fov = 0.01 # mimic orthographic projection

scale = 1;
F0 = frame([0,0,0],label='O',scale=scale)

# two link planar
a1     = 0 # link length
alpha1 = 90 # link twist
d1     = .089159 # link offset (controllable)
theta1 = 0 # joint angle (controllable)
joint1 = 'r'

a2     = -0.42500 # link length
alpha2 = 0 # link twist
d2     = 0 # link offset (controllable)
theta2 = -90 # joint angle (controllable)
joint2 = 'r'

a3     = -0.39225 # link length
alpha3 = 0 # link twist
d3     = 0.0 # link offset (controllable)
theta3 = 0 # joint angle (controllable)
joint3 = 'r'

a4     = 0 # link length
alpha4 = 90 # link twist
d4     = 0.10915 # link offset (controllable)
theta4 = -90 # joint angle (controllable)
joint4 = 'r'

a5     = 0 # link length
alpha5 = 90 # link twist
d5     = 0.09465 # link offset (controllable)
theta5 = 0 # joint angle (controllable)
joint5 = 'r'

a6     = 0 # link length
alpha6 = 0 # link twist
d6     = 0.0823  # link offset (controllable)
theta6 = 0 # joint angle (controllable)
joint6 = 'r'

q1 = 30 
q2 = 30 
q3 = 30 
q4 = 30 
q5 = 30 
q6 = 30 

scale = 0.5

L1 = link(F0,a=a1,alpha=alpha1,d=d1,theta=theta1,q=q1,joint=joint1,label='L1',scale=scale,unit='deg')
L2 = link(L1.frame,a=a2,alpha=alpha2,d=d2,theta=theta2,q=q2,joint=joint2,label='L2',scale=scale,unit='deg')
L3 = link(L2.frame,a=a3,alpha=alpha3,d=d3,theta=theta3,q=q3,joint=joint3,label='L3',scale=scale,unit='deg')
L4 = link(L3.frame,a=a4,alpha=alpha4,d=d4,theta=theta4,q=q4,joint=joint4,label='L4',scale=scale,unit='deg')
L5 = link(L4.frame,a=a5,alpha=alpha5,d=d5,theta=theta5,q=q5,joint=joint5,label='L5',scale=scale,unit='deg')
L6 = link(L5.frame,a=a6,alpha=alpha6,d=d6,theta=theta6,q=q6,joint=joint6,label='L6',scale=scale,unit='deg')

scene.camera(F0,forward=[-1,-1,-1],up=[0,0,1])
