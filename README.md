python-robotics
===============

robot kinematics with python-visual visualization


These python modules has been written for use in the course Robot Modeling
at the Hague University of Applied Sciences, by Rufus Fraanje
(p.r.fraanje@hhs.nl)

In this course, we use the book Robot Modeling and Control by Mark W. Spong, Seth Hutchinson, M. Vidyasagar, Wiley, 2005, some pieces of the code may resemble the notation and derivations from this (excellent) book.

The code relies on:
 - the great transformations module by Christoph Gohlke
 - the python visual module (also called vpython) for 3D visualization

The code offers:
 - frames.py: construction and visualization of frames in 3D, and performing
              translations, rotations, homogeneous transformations
 - links.py:  construction of joints with attached links and a frame located at
              the end of the link, specified on the basis of Denavit Hartenberg
              parameters
 - examples:  frames_examples.py and links_examples.py give some examples for
              using frames.py and links.py
 
The current focus has been on 3D visualization of frames, joints, links on the
basis of Denavit Hartenberg parameters. Inverse kinematics and (multibody) dynamics haven't been implemented yet. Documentation needs to be completed.

The code has been written with care, but may be improved. Any suggestions are
welcome. Feel free to use the code, but its use is without any guarantee.




