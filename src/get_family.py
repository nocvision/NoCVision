import numpy as np

def get_family(nodes,num_vcs,l):
   if np.shape(l) == (nodes,4):
      return 'link'
   elif np.shape(l) == (nodes,):
      return 'router'
   elif np.shape(l) == (nodes,4, num_vcs):
      return 'vc'
   else:
      return -1
