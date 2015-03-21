# ----------------------------------------
# NoCVision
# Copyright 2014 The Regents of the University of Michigan
# Vaibhav Gogte, Ritesh Parikh, Valeria Bertacco
# 
# NocVision is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---------------------------------------------

from nocvision_config import *

def restart():
   canvas.grid_remove()
   hbar.grid_remove()
   vbar.grid_remove()
   for child in frame1.winfo_children():
      child.grid_remove()
   exit_gui()
