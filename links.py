# todo: documentation
from __future__ import division, print_function  # to improve compatibility with python 3

from frames import *
from time import sleep

class link(object):
    def __init__(self,frame_rel,a=1,alpha=0,d=0,theta=0,q=0,joint='r',label='',scale=1,unit='deg'):
        self.__joint = joint
        self.__q = q
        if self.__joint == 'p': # prismatic joint
            self.__Hq = se3(dis=[0,0,q])
        else:
            self.__Hq = se3(dis=[0,0,0],angle=q,axis=[0,0,1],unit=unit)

        self.__unit    = unit 
        self.__alpha   = alpha
        self.__a       = a
        self.__d       = d
        self.__theta   = theta 

        self.__H_alpha = se3(dis=[0,0,0],angle=alpha,axis=[1,0,0],unit=unit)
        self.__H_a     = se3(dis=[a,0,0])
        self.__H_d     = se3(dis=[0,0,d])
        self.__H_theta = se3(dis=[0,0,0],angle=theta,axis=[0,0,1],unit=unit)
        
        self.__hom = self.__Hq*self.__H_theta*self.__H_d*self.__H_a*self.__H_alpha

        self.__frame_rel = frame_rel

        self.__frame = frame(dis=self.__hom.hom[0:3,3],rot=self.__hom.hom[0:3,0:3],label=label,frame_rel=frame_rel);
        self.__frame.axis.scale = scale
    
        #rotating link:
        # todo: if a and d both are 0
        if (a==0) & (d==0):
            x = z = np.zeros((1,1))
        elif np.abs(a)>=np.abs(d):
            x = np.sign(a)*np.linspace(0.1*scale,np.abs(a)-.1*scale,int(2+50*np.abs(d/a)))
            #x = np.sign(a)*np.linspace(0,np.abs(a),int(2+40*np.abs(d/a)))
            x = x.reshape((len(x),1))
            beta = 500/len(x) #8
            z = d/(1+np.exp(-beta*(x/a-0.5)))
            #z = d/(1+np.exp(-beta*((x-np.sign(a)*0.1*scale)/a-0.5)))
            #z = self.__d/(1+np.exp(-beta*((x-np.sign(self.__a)*0.1*self.__scale)/self.__a-0.5)))
        else:
            z = np.sign(d)*np.linspace(0,np.abs(d),int(2+50*np.abs(a/d)))
            z = z.reshape((len(z),1))
            beta = 500/len(z)
            x = a/(1+np.exp(-beta*(z/d-0.5)))

        self.__x = x
        self.__z = z
        self.__scale = scale

        if self.__joint == 'r': # joint is revolute
            if self.__unit == 'deg':
                angle = (self.__q + self.__theta) / 180. * np.pi
            else:
                angle = self.__q + self.__theta
            z_vals = self.__z
        else: # joint is prismatic
            if self.__unit == 'deg':
                angle = (self.__theta) / 180. * np.pi
            else:
                angle = self.__theta
            z_vals = self.__z + self.__q
        pos_xyz = np.hstack((np.hstack((np.cos(angle)*self.__x,np.sin(angle)*self.__x)),z_vals))

        if self.__unit == 'deg':
            twist=-self.__alpha/180. * np.pi / len(self.__x)#-np.linspace(0,(self.__alpha/180.) * np.pi,len(x))
        else:
            twist=-self.__alpha/len(self.__x)#-np.linspace(0,self.__alpha,len(x))

        square = visual.shapes.rectangle(pos=(0,0),width=0.1*self.__scale,height=0.05*self.__scale,roundness = 0.2)

        self.__link = visual.extrusion(frame=self.__frame_rel.frame_obj,
                pos=pos_xyz,up=(0,0,1),twist=twist,shape=square,smooth=.9,color=visual.color.lighterblue,
                material=visual.materials.diffuse) #(0.8,0.8,1))
        #self.__hinge1  = visual.cylinder(frame=self.__frame_rel.frame_obj,pos=[0,0,z_vals[0]],axis=[0,0,.05*scale],radius=.1*scale,
        if self.__joint == 'p':
            self.__hinge1  = visual.cylinder(frame=self.__frame_rel.frame_obj,pos=[0,0,self.__q],axis=[0,0,.05*scale],radius=.1*scale,color=visual.color.darkyellow,material=visual.materials.plastic)
        else:
            self.__hinge1  = visual.cylinder(frame=self.__frame_rel.frame_obj,pos=[0,0,0],axis=[0,0,.05*scale],radius=.1*scale,color=visual.color.darkyellow,material=visual.materials.plastic)


        self.__hinge2 = visual.cylinder(frame=self.__frame.frame_obj,pos=[0,0,-0.05*scale],axis=[0,0,.05*scale],radius=.1*scale,
        color=visual.color.lighteryellow,material=visual.materials.plastic)#(.7,.7,0))
        

        # if joint is prismatic, also ad a cylinder in z-direction along which the link is
        # displaced w.r.t. it's mounting point:
        if self.__joint == 'p':
            #self.__prismatic = visual.cylinder(frame=self.__frame_rel.frame_obj,pos=[0,0,0],axis=[0,0,self.__q+np.sign(self.__q)*0.06*scale],
            self.__prismatic = visual.cylinder(frame=self.__frame_rel.frame_obj,pos=[0,0,0],axis=[0,0,self.__q],
                    radius=0.04*scale,color=visual.color.darkeryellow,material=visual.materials.plastic) #color=(1,.8,0))



    @property
    def z(self):
        return self.__z
    @property
    def x(self):
        return self.__x
    @property
    def hom(self):
        return self.__hom
    @property
    def frame_rel(self):
        return self.__frame_rel
    @property
    def frame(self):
        return self.__frame
    @property
    def joint(self):
        return self.__joint
    @property
    def unit(self):
        return self.__unit
    @property
    def alpha(self):
        return self.__alpha

    @alpha.setter
    def alpha(self,alpha):
        self.__alpha = alpha

        self.__H_alpha = se3(dis=[0,0,0],angle=self.__alpha,axis=[1,0,0],unit=self.__unit)
        self.__H_a     = se3(dis=[self.__a,0,0])
        self.__H_d     = se3(dis=[0,0,self.__d])
        self.__H_theta = se3(dis=[0,0,0],angle=self.__theta,axis=[0,0,1],unit=self.__unit)
        
        self.__hom = self.__Hq*self.__H_theta*self.__H_d*self.__H_a*self.__H_alpha


        self.__frame.hom = self.__hom.hom

        self.update_view()


    @property
    def H_alpha(self):
        return self.__H_alpha
    @alpha.setter
    def alpha(self,alpha):
        self.__alpha = alpha
        self.__H_alpha = se3(dis=[0,0,0],angle=self.__alpha,axis=[1,0,0],unit=self.__unit)
        self.__hom = self.__Hq*self.__H_theta*self.__H_d*self.__H_a*self.__H_alpha
        self.__frame.hom = self.__hom.hom
        self.update_view()

    @property
    def a(self):
        return self.__a
    @a.setter
    def a(self,a):
        self.__a = a
        self.__H_a     = se3(dis=[self.__a,0,0])
        self.__hom = self.__Hq*self.__H_theta*self.__H_d*self.__H_a*self.__H_alpha
        self.__frame.hom = self.__hom.hom
        self.update_view()
    @property
    def H_a(self):
        return self.__H_a
    @property
    def d(self):
        return self.__d
    @d.setter
    def d(self,d):
        self.__d = d
        self.__H_d     = se3(dis=[0,0,self.__d])
        self.__hom = self.__Hq*self.__H_theta*self.__H_d*self.__H_a*self.__H_alpha
        self.__frame.hom = self.__hom.hom
        self.update_view()

    @property
    def H_d(self):
        return self.__H_d
    @property
    def theta(self):
        return self.__theta
    @theta.setter
    def theta(self,theta):
        self.__theta = theta 
        self.__H_theta = se3(dis=[0,0,0],angle=self.__theta,axis=[0,0,1],unit=self.__unit)
        self.__hom = self.__Hq*self.__H_theta*self.__H_d*self.__H_a*self.__H_alpha
        self.__frame.hom = self.__hom.hom
        self.update_view()

    @property
    def H_theta(self):
        return self.__H_theta

    @property
    def Hq(self):
        return self.__Hq
    @property
    def q(self):
        return self.__q
    @q.setter
    def q(self,q):
        self.__q = q
        Hq_old_inv = self.__Hq.hom_inv
        if self.__joint == 'p': # prismatic joint
            self.__Hq = se3(dis=[0,0,self.__q])
        else:
            self.__Hq = se3(dis=[0,0,0],angle=self.__q,axis=[0,0,1],unit=self.__unit)
        self.__hom = self.__Hq*self.__H_theta*self.__H_d*self.__H_a*self.__H_alpha
        self.__frame.hom = self.__hom.hom 
        self.update_view()

    def set_delayed(self,prop='q',incr=1,delay=1,niter=20):
        delay_step = 1.0*delay/niter
        incr_step = 1.0*incr/niter
        for i in range(niter):
            if prop=='q':
                self.q += incr_step
            elif prop=='a':
                self.a += incr_step
            elif prop=='alpha':
                self.alpha += incr_step
            elif prop=='d':
                self.d += incr_step
            elif prop=='theta':
                self.theta += incr_step
            else:
                print('Warning: invalid property.')
            sleep(delay_step)
        return 0


    def update_view(self):
        if (self.__a==0) & (self.__d==0):
            x = z = np.zeros((1,1))
        elif np.abs(self.__a)>=np.abs(self.__d):
            x = np.sign(self.__a)*np.linspace(0.1*self.__scale,np.abs(self.__a)-.1*self.__scale,int(2+50*np.abs(self.__d/self.__a)))
            x = x.reshape((len(x),1))
            beta = 500/len(x) #8
            z = self.__d/(1+np.exp(-beta*(x/self.__a-0.5)))
        else:
            z = np.sign(self.__d)*np.linspace(0,np.abs(self.__d),int(2+50*np.abs(self.__a/self.__d)))
            z = z.reshape((len(z),1))
            beta = 500/len(z)
            x = self.__a/(1+np.exp(-beta*(z/self.__d-0.5)))

        self.__x = x
        self.__z = z

        if self.__joint == 'r': # joint is revolute
            if self.__unit == 'deg':
                angle = (self.__q + self.__theta) / 180. * np.pi
            else:
                angle = self.__q + self.__theta
            z_vals = self.__z
        else: # joint is prismatic
            if self.__unit == 'deg':
                angle = (self.__theta) / 180. * np.pi
            else:
                angle = self.__theta
            z_vals = self.__z + self.__q

        pos_xyz = np.hstack((np.hstack((np.cos(angle)*self.__x,np.sin(angle)*self.__x)),z_vals))

        if self.__unit == 'deg':
            twist=-self.__alpha/180. * np.pi / len(self.__x)#-np.linspace(0,(self.__alpha/180.) * np.pi,len(x))
        else:
            twist=-self.__alpha/len(self.__x)#-np.linspace(0,self.__alpha,len(x))

        square = visual.shapes.rectangle(pos=(0,0),width=0.1*self.__scale,height=0.05*self.__scale,roundness = 0.2)


        self.__link.pos = pos_xyz
        self.__link.twist = twist


        if self.__joint == 'p':
            self.__prismatic.axis = [0,0,self.__q] #+np.sign(self.__q)*0.06*scale]
            self.__hinge1.pos = [0,0,self.__q] #[0,0,z_vals[0]]
        else:
            self.__hinge1.pos = [0,0,0] #[0,0,z_vals[0]]
        

#scene = display(title='Test visualization',center=(0,0,0),forward=(0,0,-1),up=(0,1,0),background=visual.color.background,range=5)
#scene.fov = 0.01 # mimic orthographic projection

#scene.camera(center=[0,0,0],forward = [-1,-1,-1],up=[0,0,1])
#
#scale = 1;
#F0 = frame([0,0,0],label='O',scale=scale)
#
