# Python Robotics toolbox (python-robotics)

robot kinematics with python-visual visualization

These python modules has been written for use in the course Robot Modeling
at the Hague University of Applied Sciences, by Rufus Fraanje
(p.r.fraanje@hhs.nl)

In this course, we use the book Robot Modeling and Control by Mark W. Spong, Seth Hutchinson, M. Vidyasagar, Wiley, 2005, some pieces of the code may resemble the notation and derivations from this (excellent) book.

## Dependencies
* the great [transformations](http://www.lfd.uci.edu/~gohlke/code/transformations.py.html) module by Christoph Gohlke
* the easy to use [python-visual module (also called vpython)](http://www.vpython.org/) for 3D visualization

## Description and examples
* [`frames.py`](https://github.com/prfraanje/python-robotics/blob/master/frames.py): construction and visualization of frames in 3D, and performing
              translations, rotations, homogeneous transformations

Examples:
```
>>> Rz  = so3(angle=30)   
>>> Ry  = so3(angle=60,axis=[0,1,0])
>>> Rzy = Rz*Ry           # new object, equivalent to Rzy = Rz * Ry
>>> F0 = frame(label='0') # build frame 0 with default settings
>>> F1 = Ry*Rz*F0         # rotation of F0 (note: premultiplication is
                          # rotation about fixed axes
>>> F2.label = '1'        # always set label, because this is not being done
                          # automatically 
>>> F2 = F0*Rz*Ry         # is possible as well, see documentation
                          # under __rmul__()
>>> F2.label = '2'        # always set label, because this is not being done
                          # automatically 
```
* [`links.py`](https://github.com/prfraanje/python-robotics/blob/master/links.py):  construction of joints with attached links and a frame located at
             the end of the link, specified on the basis of Denavit Hartenberg
             parameters
```
from links import * 
from time import sleep

scene = display(title='Test visualization',center=(0,0,0),forward=(0,0,-1),up=(0,1,0),background=visual.color.background,range=2)
scene.fov = 0.01 # mimic orthographic projection

scale = 1;
F0 = frame([0,0,0],label='0, joint 1',scale=scale)

# Two links specified by their Denavit-Hartenberg parameters: 
L1 = link(F0,a=1,alpha=-90,d=0,theta=0,q=45,joint='r',label='1, joint 2',scale=1,unit='deg') 
L2 = link(L1.frame,a=1,alpha=0,d=0,theta=0,q=.5,joint='p',label='2, joint 3',scale=1,unit='deg') 
L1.a = 1.5
print(L1.a)
L1.set_delayed(prop='q',incr=30,delay=2,niter=20):
print(L1.q)
```
* examples:  [frames_examples.py](https://github.com/prfraanje/python-robotics/blob/master/frames_examples.py) and [links_examples.py](https://github.com/prfraanje/python-robotics/blob/master/links_examples.py) give some examples for
              using [frames.py](https://github.com/prfraanje/python-robotics/blob/master/frames.py) and [links.py](https://github.com/prfraanje/python-robotics/blob/master/links.py), see also [ur5.py](https://github.com/prfraanje/python-robotics/blob/master/ur5.py) for a visualization
              of the Universal Robot UR5 robot, e.g. try
```
python ur5.py
```
 
## To do
The current focus has been on 3D visualization of frames, joints, links on the
basis of Denavit Hartenberg parameters. Inverse kinematics and (multibody) dynamics haven't been implemented yet. Documentation needs to be completed.

The code has been written with care, but may be improved. Any suggestions are
welcome. Feel free to use the code, but its use is without any guarantee.

## Acknowledgement
* [Matlab Robotic Toolbox](http://petercorke.com/Robotics_Toolbox.html) by
  Peter Corke, this is a great toolbox which was the inspiration for this
  toolbox. But note, python-robotics is not a translation of the Matlab Robotic
  Toolbox!

