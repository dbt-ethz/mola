import sys
path = "C:\Users\Wenqian\Documents\GitHub"
if path not in sys.path:
    sys.path.append(path)

import rhinoscriptsyntax as rs

import mola
from mola import module_rhino

guid = rs.GetObject()

new_mesh = module_rhino.mesh_from_rhino_mesh(guid)

print(new_mesh)