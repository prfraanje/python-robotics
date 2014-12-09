# This module frames.py provides a number of python classess
# for visualization of rotations and homogeneous 
# transformations
# 
# Dependencies:
# numpy:              for matrices, vectors and linear algebra
# transformations.py: to calculate rotation and homogenous transformations
# visual:             for 3D visualization

# Author:    Rufus Fraanje, p.r.fraanje@hhs.nl

 
from __future__ import division, print_function  # to improve compatibility with python 3

# select type of background 
#background_light = True # True for light background, False for dark background
background_light = False # True for light background, False for dark background

import visual                  # 3D visualization module: http://www.vpython.org 

if background_light:
    from color_palette_light import *
else:
    from color_palette_dark import *

import numpy as np             # numpy for matrix/vector calc.: http://numpy.scipy.org
import transformations as tf   # for all kind of rotations etc.: http://www.lfd.uci.edu/~gohlke/code/transformations.py.html


# definition of Special Orthogonal Group SE(3) of 
# (right handed) rotation matrices
# for more about classes in python: https://docs.python.org/2/tutorial/classes.html
# also see: http://anandology.com/python-practice-book/object_oriented_programming.html
class so3(object):
    def __init__(self,angle=0,axis=[0,0,1],unit='deg'):
        """initialization of object, rotation with angle around the vector axis,
           angle is specified in degrees (default) or radians (unit='rad')"""
        if unit == 'deg': angle = angle*np.pi/180
        # otherwise, angle is assumed to be in radians
        self.__rot = tf.rotation_matrix(angle,axis)[0:3,0:3]

# properties are excellent for quickly getting or setting values
# see more on this: https://docs.python.org/2/library/functions.html?highlight=property#property
    @property
    def rot(self):
        """return or set the rotation matrix, a 3x3 numpy array
        Example:
        >>> R1 = so3(np.pi/4,axis=[1,0,0],unit='rad') 
        >>> R2 = so3(60,axis=[1,0,0])           # by default unit is in degrees 
        >>> R1.rot
        >>> R2.rot
        >>> R1.rot = np.eye(3)                  # set rotation to identity
        >>> R2.rot = [[1,0,0],[0,1,0],[0,0,1]]  # set rotation to identity
        >>> R2.rot = [1,0,0,0,1,0,0,0,1]        # set rotation to identity
        """
        return self.__rot
    @rot.setter                                 # setter allows to set property
    def rot(self,R):
        R = np.array(R).reshape(3,3)
        if is_so3(R):
            self.__rot = R
        else:
            raise ValueError("(class {0.__class__.__name__}, rot): R is not in so3 (not symmetric and/or det(R)=1)".format(self))

    @property
    def T(self):
        """returns a new so3 object with transposed (i.e. inverse) rotation matrix"""
        ret = so3()
        ret.rot = self.rot.T
        return ret

# inverse of rotation matrix is equal to transpose, so does not need to be implemented
#    @property
#    def inv(self):
#        ret = so3()
#        ret.rot = np.linalg.inv(self.rot)
#        return ret

# calculation of determinant (in fact not necessary as well, because should be 1 always)
    @property
    def det(self):
        """returns the determinant of the rotation matrix (should be 1)"""
        return np.linalg.det(self.rot)

# the __repr__ method of a class defines how objects are shown in python, e.g. 
# >>> a = 2
# >>> a  # __repr__ functions of variable a is called, is same as:
# >>> print(a.__repr__()) # print the output string of the repr function of a
    def __repr__(self):
        """repr function, defines how object is shown in python interpreter"""
        string = "{0.__class__.__name__}: (rotation matrix)\n\n".format(self)
        string += "rot:\n"
        string += self.rot.__repr__()
        return string

# definition of the multiplication operator '*', in python one can define arithmatic
# operators, like '-', '+', '*', '/', etc. use with objects
# see e.g.: https://docs.python.org/2/reference/datamodel.html?highlight=init__#object.__mul__
    def __mul__(self,other):
        """multiplication of two so3 objects or a so3 object and a frame or
        point
        Example:
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
        """
        if isinstance(other,so3):
            rot = np.dot(self.rot,other.rot)
            ret = so3()
            ret.rot = rot
            return ret
        elif isinstance(other,frame) | isinstance(other,point):
           if other.label == "__replace_label__": # if label is this, then it's result of
                                       # earlier multiplication and should be made invisible
                other.visible = False  # this is to suppress visualization of intermediate frames
                                       # in e.g. F0 * R01 * R12, etc. 
           frame_new = frame(label="__replace_label__")
           frame_new.pos = [0,0,0]
           frame_new.rot = np.dot(self.rot,other.rot)
           return frame_new

    def __rmul__(self,other):
        """multiplication of two so3 objects or a so3 object and a frame or
        point
        Example:
        >>> R01 = so3(angle=30)                # z-axis rotation
        >>> R12 = so3(angle=30,axis=[1,0,0])   # x-axis rotation
        >>> F0 = frame(label='0')
        >>> F1 = F0*R01*R12 # first rotate about z-axis, then rotate new
                            # intermediate frame (F0*R01) about x-axis of (F0*R01)
        >>> F1.label = '1'  # always set label, because this is not being done
                            # automatically 
        """
        if isinstance(other,so3):
            rot = np.dot(other.rot,self.rot)
            ret = so3()
            ret.rot = rot
            return ret
        elif isinstance(other,frame) | isinstance(other,point):
            #frame_copy = other.copy("_rot")
            #frame_copy.frame_rel = other
            #frame_copy.pos = [0,0,0]
            #frame_copy.rot = self.rot
            #return frame_copy
            if other.label == "__replace_label__": # if label is this, then it's result of
                                       # earlier multiplication and should be made invisible
                other.visible = False  # this is to suppress visualization of intermediate frames
                                       # in e.g. F0 * R01 * R12, etc. 
            frame_new = frame(label="__replace_label__")
            #frame_new = frame(label="_new")
            frame_new.pos = [0,0,0]
            frame_new.rot = np.dot(other.rot,self.rot)
            return frame_new

            

# function to determine whether a matrix is a 3x3 right handed rotation matrix
def is_so3(R,info=False):
    """checks whether R is in so3, i.e., is a right handed rotation
    >>> is_so3(np.eye(3))          # returns true
    >>> is_so3(np.random.randn(3)) # generally returns False
    info can be set to True to make the function more verbous
    """
    if isinstance(R,so3):
        Rmat = R.rot
    else:
        Rmat = R
    det = np.linalg.det(Rmat)
    is_symmetric = np.allclose(np.dot(Rmat.T,Rmat),np.eye(3))
    if not(np.isclose(det,1)):
        if np.isclose(det,-1):
            if info: print("det(R)=-1, rotations in so3 should be right handed.")
            return False
        else:
            if info: print("det(R)={0} and not 1, so R is not a rotation matrix.".format(det))
            return False
    else:
        if is_symmetric:
            return True
        else:
            if info: print("R is not symmetric.")
            return False

# function to determine whether a matrix is a homogeneous transformation matrix:
def is_se3(H,info=False):
    """checks whether H is in se3, i.e., is a homogenous transformation,
    in fact, checks whether H[0:3,0:3] is a rotation with is_so3(H[0:3,0:3])
    and checks wether last row of H, i.e., H[3,:], equals [0,0,0,1]
    >>> is_se3(np.eye(4))          # returns True
    >>> is_se3(np.random.randn(3)) # generally returns False
    info can be set to True to make the function more verbous
    """
    if isinstance(H,se3):
        Hmat = H.hom
    else:
        Hmat = H
    Hmat = np.array(Hmat).reshape((4,4))
    check = True
    check &= (Hmat[3,:]==np.array([0,0,0,1])).all()
    if (not(check)) & info: print("Last row of H (H[3,:]) is not [0,0,0,1].")
    check &= is_so3(Hmat[0:3,0:3],info=info)
    return check


# definition of Special Euclidian Group SE(3) of 
# homogenous transformation matrices for rigid motions
class se3(object):
    def __init__(self,dis=[0,0,0],angle=0,axis=[0,0,1],unit='deg'):
        """initialization of object, dis = displacement, angle is the angle of
        rotation around the vector axis, unit is the unit of the angle."""
        self.__dis = np.array(dis).reshape((3,1))
        if unit == 'deg': angle = angle*np.pi/180.
        # otherwise, angle is assumed to be in radians
        self.__rot = tf.rotation_matrix(angle,axis)[0:3,0:3]

        self.__hom     = np.vstack( (np.hstack((self.__rot,self.__dis)), np.array([0,0,0,1]))) 
        self.__hom_inv = np.vstack( (np.hstack((self.__rot.T,-np.dot(self.__rot.T,self.__dis))), np.array([0,0,0,1]))) 

    @property
    def dis(self):
        return self.__dis
    @dis.setter
    def dis(self,dis):
        self.__dis = np.array(dis).reshape((3,1))
        self.__hom[0:3,3] = self.__dis.reshape(3)
        self.__hom_inv = np.vstack( (np.hstack((self.__rot.T,-np.dot(self.__rot.T,self.__dis))), np.array([0,0,0,1]))) 

    @property
    def rot(self):
        return self.__rot
    @rot.setter
    def rot(self,R):
        R = np.array(R).reshape((3,3))
        if is_so3(R):
            self.__rot = R
            self.__hom[0:3,0:3] = R
            self.__hom_inv = np.vstack( (np.hstack((self.__rot.T,-np.dot(self.__rot.T,self.__dis))), np.array([0,0,0,1]))) 
        else:
            raise ValueError("(class {0.__class__.__name__}, rot): R is not in so3 (not symmetric and/or det(R)=1)".format(self))

    @property
    def hom(self):
        return self.__hom
    @hom.setter
    def hom(self,H):
        H = np.array(H).reshape((4,4))
        if is_se3(H):
            self.__hom = H
            self.__dis = H[0:3,3].reshape((3,1))
            self.__rot = H[0:3,0:3]
            self.__hom_inv = np.vstack( (np.hstack((self.__rot.T,-np.dot(self.__rot.T,self.__dis))), np.array([0,0,0,1]))) 
        else:
            raise ValueError("(class {0.__class__.__name__}, hom): H is not in se3.".format(self))

    @property
    def hom_inv(self):
        return self.__hom_inv

    @property
    def T(self):
        ret = se3()
        ret.hom = self.hom.T
        return ret

    @property
    def inv(self):
        ret = se3()
        ret.hom = self.__hom_inv 
        return ret

    @property
    def det(self):
        return np.linalg.det(self.hom)

    def __repr__(self):
        string = "{0.__class__.__name__}: (homogenous transf. matrix)\n\n".format(self)
        string += "hom:\n"
        string += self.hom.__repr__()
        return string

    def __mul__(self,other):
        if isinstance(other,se3):
            hom = np.dot(self.hom,other.hom)
            ret = se3()
            ret.hom = hom
            return ret
        elif isinstance(other,frame) | isinstance(other,point):
            if other.label == "__replace_label__": # if label is this, then it's result of
                                       # earlier multiplication and should be made invisible
                other.visible = False  # this is to suppress visualization of intermediate frames
                                       # in e.g. F0 * R01 * R12, etc. 
            frame_new = frame(label="__replace_label__")
            #frame_new = frame(label="_new")
            frame_new.hom = np.dot(self.hom,other.hom)
            return frame_new

    def __rmul__(self,other):
        if isinstance(other,se3):
            hom = np.dot(other.hom,self.hom)
            ret = se3()
            ret.hom = hom
            return ret
        elif isinstance(other,frame) | isinstance(other,point):
            if other.label == "__replace_label__": # if label is this, then it's result of
                                       # earlier multiplication and should be made invisible
                other.visible = False  # this is to suppress visualization of intermediate frames
                                       # in e.g. F0 * R01 * R12, etc. 
            frame_new = frame(label="__replace_label__")
            frame_new.hom = np.dot(other.hom,self.hom)
            return frame_new



class axes(object):
    def __init__(self,frame_obj,visible=True,visible_label=True,scale=1.0):
        x_red   = visual.color.darkerred #(1,0.2,0.2)
        y_green = visual.color.darkergreen #(0.2,1,0.2)
        z_blue  = visual.color.darkerblue #(0.2,0.2,1)
        label_color = visual.color.fainttext #(0.7,0.7,0.7)

        self.__scale = scale
        al = self.__scale      # arrow length
        sw = self.__scale*0.01 # shaftwidth
        hw = self.__scale*0.03 # headwidth
        hl = self.__scale*0.05 # headlength

        self.__frame_obj = frame_obj
        self.__frame_axis_obj = visual.frame(frame=self.__frame_obj,pos=(0,0,0),visible=visible)        
        self.__frame_axis_label_obj = visual.frame(frame=self.__frame_axis_obj,pos=(0,0,0),visible=visible_label)
        self.__x_axis_obj = visual.arrow(frame=self.__frame_axis_obj,pos=(0,0,0),axis=(al,0,0),shaftwidth=sw,headwidth=hw,headlength=hl,color=x_red)
        self.__x_axis_label_obj = visual.label(frame=self.__frame_axis_label_obj,pos=(al,0,0),xoffset=1,font='sans',text="x",box=False,opacity=0,border=0,line=0,height=10*scale,color=label_color)
        self.__y_axis_obj = visual.arrow(frame=self.__frame_axis_obj,pos=(0,0,0), axis=(0,al,0),shaftwidth=sw,headwidth=hw,headlength=hl,color=y_green)
        self.__y_axis_label_obj = visual.label(frame=self.__frame_axis_label_obj,pos=(0,al,0),xoffset=1,font='sans',text="y",box=False,opacity=0,border=0,line=0,height=10*scale,color=label_color)
        self.__z_axis_obj = visual.arrow(frame=self.__frame_axis_obj,pos=(0,0,0), axis=(0,0,al),
                shaftwidth=sw,headwidth=hw,headlength=hl,color=z_blue)
        self.__z_axis_label_obj = visual.label(frame=self.__frame_axis_label_obj,pos=(0,0,al),xoffset=1,font='sans',text="z",box=False,opacity=0,border=0,line=0,height=10*scale,color=label_color)

    @property
    def scale(self):
        return self.__scale
    @scale.setter
    def scale(self,val):
        self.__scale = val
        al = self.__scale      # arrow length
        sw = self.__scale*0.01 # shaftwidth
        hw = self.__scale*0.03 # headwidth
        hl = self.__scale*0.05 # headlength
        # update them all
        self.__x_axis_obj.axis       = (al,0,0)
        self.__x_axis_label_obj.pos  = (al,0,0)
        self.__y_axis_obj.axis       = (0,al,0)
        self.__y_axis_label_obj.pos  = (0,al,0)
        self.__z_axis_obj.axis       = (0,0,al)
        self.__z_axis_label_obj.pos  = (0,0,al)
        self.__x_axis_obj.shaftwidth = sw
        self.__x_axis_obj.headwidth  = hw
        self.__x_axis_obj.headlength = hl
        self.__y_axis_obj.shaftwidth = sw
        self.__y_axis_obj.headwidth  = hw
        self.__y_axis_obj.headlength = hl
        self.__z_axis_obj.shaftwidth = sw
        self.__z_axis_obj.headwidth  = hw
        self.__z_axis_obj.headlength = hl

    @property
    def visible(self):
        return self.__frame_axis_obj.visible

    @visible.setter
    def visible(self,val):
        self.__frame_axis_obj.visible = val

    @property
    def visible_label(self):
        return self.__frame_axis_label_obj.visible

    @visible_label.setter
    def visible_label(self,val):
        self.__frame_axis_label_obj.visible = val


class frame(object):
    def __init__(self,dis=np.zeros((3,1)),rot=np.eye(3),label="",frame_rel=None,color=visual.color.text,
                 visible=True,visible_frame=True,visible_label=True,visible_frame_label=True,scale=1.0):

       self.__dis = np.array(dis).reshape(3,1)
       self.__rot = np.array(rot).reshape(3,3)
       self.__hom = np.vstack((np.hstack((self.__rot,self.__dis)),np.array([0,0,0,1])))
       self.__hom_inv = np.vstack((np.hstack((self.__rot.T,-np.dot(self.__rot.T,self.__dis))),np.array([0,0,0,1]))) 
       self.__label = label
       self.__color = color

       if frame_rel == None:
           self.__frame_rel = None
           self.__frame_obj = visual.frame(pos=self.__dis,visible=visible)
       else:
           self.__frame_rel = frame_rel
           self.__frame_obj = visual.frame(frame=self.__frame_rel.__frame_obj,pos=self.__dis,visible=visible)

       self.__frame_obj.axis = self.__rot[:,0]
       self.__frame_obj.up = self.__rot[:,1]
       self.__point_obj = visual.points(frame=self.__frame_obj,pos=(0,0,0),color=color,size=4,size_units="pixels",shape="round")
       self.__label_obj = visual.label(frame=self.__frame_obj,text=self.__label,visible=visible_label,
               pos=(0,0,0),xoffset=5*scale,yoffset=1*scale,space=5*scale,line=0,height=16*scale,border=0,font='sans',color=color,box=False,opacity=0)
       self.axis = axes(frame_obj=self.__frame_obj,visible=visible_frame,visible_label=visible_frame_label,scale=scale)

    def __repr__(self):
        string =  "{0.__class__.__name__}: label = {0.label}, ".format(self)
        if self.__frame_rel == None:
            string += "defined in world coordinates\n\n"
        else:
            string += "defined relative to frame: {0}\n\n".format(self.__frame_rel.label)
        string += "dis: \n" + self.__dis.__repr__() +"\n\n"
        string += "rot: \n" + self.__rot.__repr__() +"\n\n"
        string += "hom: \n" + self.__hom.__repr__() +"\n\n"
        string += "visible      : {0.visible},\t visible_label      : {0.visible_label}\n".format(self)
        string += "axis.visible : {0.axis.visible},\t axis.visible_label : {0.axis.visible_label}".format(self)
        return string

    def copy(self,label="_copy"):
        """copy(self,label="_copy"): copies the frame self"""
        if label[0] == "_": label = self.label + label
        return frame(dis=self.dis,rot=self.rot,label=label,frame_rel=self.frame_rel,color=self.color,
                 visible=self.visible,visible_frame=self.axis.visible,visible_label=self.visible_label,
                 visible_frame_label=self.axis.visible_label,scale=self.axis.scale)

    @property
    def frame_obj(self):
        return self.__frame_obj

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self,label):
        self.__label = label
        self.__label_obj.text = self.__label

    @property
    def frame_rel(self):
        return self.__frame_rel
    @frame_rel.setter
    def frame_rel(self,frame_rel,*args):
        if len(args)==1:
            scale = args[0]
        else:
            if frame_rel == None:
                scale = 1
            else:
                scale = frame_rel.axis.scale

        visible = self.visible
        visible_label = self.visible_label
        visible_frame = self.axis.visible
        visible_frame_label = self.axis.visible_label
        color = self.color
        self.visible = False
        del self.__frame_rel
        del self.__frame_obj
        if frame_rel == None:
            self.__frame_rel = None
            self.__frame_obj = visual.frame(dis=self.__dis,visible=visible)
        else:
            self.__frame_rel = frame_rel
            self.__frame_obj = visual.frame(frame=self.__frame_rel.__frame_obj,pos=self.__dis,visible=visible)


        self.__frame_obj.axis = self.__rot[:,0]
        self.__frame_obj.up = self.__rot[:,1]
        self.__point_obj = visual.points(frame=self.__frame_obj,pos=(0,0,0),color=color,size=4,size_units="pixels",shape="round")
        self.__label_obj = visual.label(frame=self.__frame_obj,text=self.__label,visible=visible_label,
                pos=(0,0,0),xoffset=5*scale,yoffset=1*scale,space=5*scale,line=0,height=16*scale,border=0,font='sans',color=color,box=False,opacity=0)
        self.axis = axes(frame_obj=self.__frame_obj,visible=visible_frame,visible_label=visible_frame_label,scale=scale)


    @property
    def dis(self):
        """The disition of the point"""
        return self.__dis

    @dis.setter
    def dis(self,dis):
        self.__dis = np.array(dis).reshape((3,1))
        self.__hom[0:3,3] = self.__dis.reshape(3)
        self.__hom_inv[0:3,3] = -np.dot(self.__rot.T,self.__dis).reshape(3) # only this part changes
        self.__frame_obj.pos = self.__dis

    @property
    def rot(self):
        return self.__rot

    @rot.setter
    def rot(self,rot):
        self.__rot = np.array(rot).reshape((3,3))
        self.__hom[0:3,0:3] = self.__rot
        self.__hom_inv[0:3,:] = np.hstack((self.__rot.T,-np.dot(self.__rot.T,self.__dis)))
        self.__frame_obj.axis = self.__rot[:,0]
        self.__frame_obj.up   = self.__rot[:,1]

    @property
    def hom(self):
        return self.__hom
    @hom.setter
    def hom(self,hom):
        self.__hom = np.array(hom).reshape((4,4))
        self.dis = self.__hom[0:3,3]
        self.rot = self.__hom[0:3,0:3]
        # note, that it is easier to set hom_inv after rot and dis has been set
        self.__hom_inv[0:3,:] = np.hstack((self.__rot.T,-np.dot(self.__rot.T,self.__dis)))

    @property
    def hom_inv(self):
        return self.__hom_inv

    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self,val):
        self.__color = val
        self.__point_obj.color = val
        self.__label_obj.color = val

    @property
    def visible(self):
        return self.__frame_obj.visible

    @visible.setter
    def visible(self,val):
        self.__frame_obj.visible = val

    @property
    def visible_label(self):
        return self.__label_obj.visible

    @visible_label.setter
    def visible_label(self,val):
        self.__label_obj.visible = val

    def dis_world(self,dis=[0,0,0]):
        dis = np.array(dis).reshape((3,1))
        if self.__frame_rel == None:
            return self.dis + np.dot(self.rot,dis)
        else:
            return self.__frame_rel.dis_world(self.dis+np.dot(self.rot,dis))

    def rot_world(self,rot=np.eye(3)):
        rot = np.array(rot).reshape((3,3))
        if self.__frame_rel == None:
            return np.dot(self.rot,rot)
        else:
            return self.__frame_rel.rot_world(np.dot(self.rot,rot))

    def hom_world(self,hom=np.eye(4)):
        hom = np.array(hom).reshape((4,4))
        if self.__frame_rel == None:
            return np.dot(self.hom,hom) 
        else:
            return self.__frame_rel.hom_world(np.dot(self.hom,hom))

    def dis_local(self,dis=[0,0,0]):
        dis = np.array(dis).reshape((3,1))
        if self.__frame_rel == None:
            return np.dot(self.rot.T,dis - self.dis)
        else:
            return np.dot(self.rot.T,self.__frame_rel.dis_local(dis)-self.dis)

    def rot_local(self,rot=np.eye(3)):
        rot = np.array(rot).reshape((3,3))
        if self.__frame_rel == None:
            return np.dot(self.rot.T,rot)
        else:
            return np.dot(self.rot.T,self.__frame_rel.rot_local(rot))

    def hom_local(self,hom=np.eye(4)):
        hom = np.array(hom).reshape((4,4))
        if self.__frame_rel == None:
            return np.dot(self.hom_inv,hom)
        else:
            return np.dot(self.hom_inv,self.__frame_rel.hom_local(hom))

    def mul(self,obj):
        """left multiplication of self.rot or self.hom with obj,
           can be so3 (rotation) or se3 (homogeneous transf.) object or
           an numpy.array of dimension 3x3 (rotation) or 4x4 (homogenous
           transf.)
        """
        error = True 
        if isinstance(obj,so3):
            self.rot = np.dot(obj.rot,self.rot)
            error = False
        elif isinstance(obj,se3):
            self.hom = np.dot(obj.hom,self.hom)
            error = False
        elif isinstance(obj,np.ndarray):
            if (obj.shape == (3,3)):
                if is_so3(obj):
                    self.rot = np.dot(obj,self.rot)
                    error = False
            elif (obj.shape == (4,4)):
                if is_se3(obj):
                    self.hom = np.dot(obj,self.hom)
                    error = False 
            else:
                error = True
        else:
            error = True
        if error: raise TypeError("({0.__class__.__name__}, mul), obj is of wrong type.".format(self))

class point(frame):
    def __init__(self,frame=None,dis=[0,0,0],label=''):
        super(point,self).__init__(dis=dis,rot=np.eye(3),label=label,frame_rel=frame,color=visual.color.text,
                 visible=True,visible_frame=False,visible_label=True,visible_frame_label=True)

    def __repr__(self):
        string =  "{0.__class__.__name__}: label = {0.label}, ".format(self)
        if self.frame_rel == None:
            string += "defined in world coordinates\n\n"
        else:
            string += "defined relative to frame: {0}\n\n".format(self.frame_rel.label)
        string += "dis: \n" + self.dis.__repr__() +"\n\n"
        string += "visible      : {0.visible},\t visible_label      : {0.visible_label}\n".format(self)
        string += "axis.visible : {0.axis.visible},\t axis.visible_label : {0.axis.visible_label}".format(self)
        return string
 
class display(visual.display):
    def camera(self,frame=None,center=[0,0,0],forward=[0,0,-1],up=[0,1,0]):
        if frame==None:
            self.center  = center
            self.forward = forward
            self.up      = up
#        else:
#            self.center  = frame.pos_world(center)
#            self.forward = frame.pos_world(forward)-frame.pos_world([0,0,0]) #np.array(self.center).reshape((3,1))
#            self.up      = frame.pos_world(up)-frame.pos_world([0,0,0]) #np.array(self.center).reshape((3,1))



