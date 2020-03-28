![alt text](https://docs.google.com/drawings/d/e/2PACX-1vRoP2HqMsB_c6zIruq1oqvYZ2b1jlXSe9mKGeDNs38SOBh-v853UQC3NQctYHhdvSRnFrP1ls7vr0uy/pub?w=198&h=287)

# Mola
Lightweight Computational Design Library

## Modules
- core_vertex
  - class definition for `Vertex`
- core_face
  - class definition for `Face`
- core_edge
  - class definition for `Edge`
- core_mesh
  - class definition for `Mesh`
- core_box
  - class definition for `Box`
- core_grid
  - class definitions for `GridManager` and `Grid`, orthogonal grid in 2d or 3d, and `Hexgrid`
- mesh_factory
  - Factory to create different mesh primitives like single face, cone, box, platonic solids
- mesh_subdivision
  - CatmullClark and simple Quad-split subdivision of an entire mesh, also method to collect vertices.
- mesh_marching_cubes
  - Create an isosurface mesh in a 3D grid of voxels
- utils_vertex
  - Vector math, input and output of type `Vertex` in most cases
- utils_face
  - Utilities to calculate different properties of a `Face`, e.g. normal, center, perimeter, etc.
- utils_poly
  - Utilities for 2D Polygons, e.g. construction of circle and 2D subdivision
- utils_color
  - Utilities to color lists of objects of class `Face` by different properties, e.g area, perimeter, curvature, etc.
- slicer
  - Slicing tools for mesh geometry
- graph
  - Classes `Graph` and `GraphAnalyser` (for shortest path or centrality calculation)
- io
  - Import / export of [OBJ Wavefront Files](https://en.wikipedia.org/wiki/Wavefront_.obj_file)
- colab2D
  - Display in [P5.js](http://p5js.org) for 2D graphics in [Google Colab](https://colab.research.google.com/notebooks/welcome.ipynb#recent=true)
- colab3D
  - Display in [Babylon.js](https://www.babylonjs.com) for 3D graphics in Google Colab
- module_processing
  - Display in [Processing Python Mode](https://py.processing.org)
- module_rhino
  - Construct and load mesh geometry in [Rhino](https://www.rhino3d.com)
- module_blender 
  - Construct mesh geometry in [Blender](https://www.blender.org)
* module_compas
  - Convert mesh objects between Mola and [COMPAS](https://compas-dev.github.io/).

## Use Cases
- The Mola library has been used in the elective course _Advanced Computational Design Course_, spring semester 2019 at ETH Zurich.
- The Mola library has been used in the MAS dfab T2 project _Concrete Choreography_
