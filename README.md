# Mola
Lightweight Computational Design Library

## Modules
- core
  - class definitions for `Vertex`, `Face`, `Edge`, `Box`, `Mesh`
- vec
  - vector math, input and output of type `Vertex` in most cases
- rules
  - rules for mesh subdivision, input `Face`, output list of `Face`s
- faceUtils
  - utilities to calculate different properties of a `Face`, e.g. normal, center, perimeter, etc.
- subdivision
  - CatmullClark subdivision of an entire mesh, also method to collect vertices.
- factory
  - Factory to create different mesh primitives like single face, cone, box, platonic solids
- meshSlicer
- marchingCubes
- grid
- graph
- io
- renderP5
- renderRhino
- renderP5JS
- renderBabylonJS
