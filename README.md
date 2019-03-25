![alt text](https://docs.google.com/drawings/d/e/2PACX-1vRoP2HqMsB_c6zIruq1oqvYZ2b1jlXSe9mKGeDNs38SOBh-v853UQC3NQctYHhdvSRnFrP1ls7vr0uy/pub?w=198&h=287)

# Mola
Lightweight Computational Design Library

## Modules
- core
  - class definitions for `Vertex`, `Face`, `Edge`, `Box`, `Mesh`
- vec
  - vector math, input and output of type `Vertex` in most cases
- faceUtils
  - Utilities to calculate different properties of a `Face`, e.g. normal, center, perimeter, etc.
- subdivision
  - CatmullClark and simple Quad-split subdivision of an entire mesh, also method to collect vertices.
  - rules for mesh subdivision, input `Face`, output list of `Face`s
- factory
  - Factory to create different mesh primitives like single face, cone, box, platonic solids
- polyUtils
  - Utilities for `2D Polygons`, e.g. construction of circle and 2D subdivision
- slicer
  - Slicing tools for mesh geometry
- marchingCubes
  - Create an isosurface mesh in a 3D grid of voxels
- grid
  - Classes `GridManager` and `Grid`, orthogonal grid in 2d or 3d, and `Hexgrid`
- graph
  - Classes `Graph` and `GraphAnalyser` (for shortest path or centrality calculation)
- io
  - Import / export of [OBJ Wavefront Files](https://en.wikipedia.org/wiki/Wavefront_.obj_file)
- renderP5
  - Display in [Processing Python Mode](https://py.processing.org)
- renderP5JS
  - Display in [P5.js](http://p5js.org) for 2D graphics in [Google Colab](https://colab.research.google.com/notebooks/welcome.ipynb#recent=true)
- renderBabylonJS
  - Display in [Babylon.js](https://www.babylonjs.com) for 3D graphics in Google Colab
- renderRhino
  - Construct and load mesh geometry in [Rhino](https://www.rhino3d.com)
