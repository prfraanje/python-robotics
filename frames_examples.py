# some examples for the use of the frames.py module
from frames import *

# calculation rotation matrices, done by so3 (behind the scenes
# transformations.py is being used
Rz = so3(30)              # rotation about z-axis (=[0,0,1]), is default
Ry = so3(30,axis=[0,1,0]) # rotation about y-axis

is_so3(Rz)  # should return True
is_so3(Ry)  # should return True
is_so3(np.random.randn(3,3)) # arbitrary 3x3 matrix, returns False most times

# before working with frames always create a scene with the display command
# the display command is rewritten in frames.py and allows you to easily
# change the camera position

scene = display(title='Frames examples',center=(0,0,0),forward=(0,0,-1),up=(0,1,0),background=visual.color.background,range=5)
scene.fov = 0.01 # mimic orthographic projection
scene.camera(center=[0,0,0],forward = [-1,-1,-1],up=[0,0,1])

#
# show frames:
F0 = frame(label='0') # always give a label to a frame
F0.rot                # rotation matrix of frame 0
                      # this is always relative to the world
                      # coordinate system, by default
                      # frame is not rotated or shifted
F0.dis                # displacement relative to the world


# illustration of rotation about current and fixed axes:
F1 = F0*Rz*Ry         # rotation around current axis z and y
F1.label='1'

F1.dis = [1,0,0]      # shift, to better distinguish from F2

F2 = Ry*Rz*F0         # rotation around fixed axis of F0
F2.label='2'
F2.dis = [1.5,0,0]     # shift, to better distinguish from F1


# homogeneous transformations:
# calculation of homogeneous matrices, done by se3 (behind the scenes
# transformations.py is being used
H03 = se3(dis=[0,1,0],angle=30,axis=[0,1,0]) # displacement of [3,3,0] and
                                             # rotation about y-axis of 30 degrees
print('H03.hom = ',H03.hom)     # returns homogeneous transformation matrix
print('H03.rot = ',H03.rot)     # returns just the rotation part
print('H03.dis = ',H03.dis)     # returns just the displacement part

is_se3(H03) # should return true
is_se3(np.random.randn(4,4)) # only for a very lucky shot it will return True
F3 = F0 * H03
F3.label='3'

