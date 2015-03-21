from nocvision_config import *

def restart():
   canvas.grid_remove()
   hbar.grid_remove()
   vbar.grid_remove()
   for child in frame1.winfo_children():
      child.grid_remove()
   exit_gui()
