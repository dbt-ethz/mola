#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

__code=""

'''display variables'''
__showAxis=False
__showEdges=False
__edgesWidth=1.0
__showWireframe=False
__backgroundColor = (0,0,0)

def displayMesh(mesh,showAxis=True,showEdges=False,edgesWidth=1.0,showWireframe=False,backgroundColor=(0,0,0)):
  """
  Displays Mesh.
  Arguments:
  ----------
  mesh : mola.core.Mesh
         The mesh to be displayed
  ----------
  Optional Arguments:
  ----------
  showAxis : Boolean
  showEdges : Boolean
  showWireframe : Boolean
  edgesWidth : float
  backgroundColor : tuple (r,g,b)
                    r,g,b values, 0.0 to 1.0
  """
  global __showAxis,__showEdges,__edgesWidth,__showWireframe,__backgroundColor
  __showAxis=showAxis
  __showEdges=showEdges
  __edgesWidth=edgesWidth
  __showWireframe=showWireframe
  __backgroundColor=backgroundColor
  return display(mesh.faces)

def display(faces):
    __begin3D()
    positions=[]
    indices=[]
    colors=[]
    cIndex=0
    for face in faces:
        for v in face.vertices:
            positions.extend((v.x,v.y,v.z))
            colors.extend(face.color)
        indices.extend([cIndex,cIndex+1,cIndex+2])
        if len(face.vertices)==4:
            indices.extend([cIndex+2,cIndex+3,cIndex])
        cIndex+=len(face.vertices)
    __drawMeshWithColors(positions,indices,colors)
    __end3D()
    return __code

def __begin3D():
    global __code
    __code+='''<canvas id="renderCanvas" touch-action="none" width="1280px" height="720px"></canvas>
        <script src="https://cdn.babylonjs.com/babylon.js"></script>

        <style>
            html, body {
                overflow: hidden;
                width: 100%;
                height: 100%;
                margin: 0;
                padding: 0;
            }

            #renderCanvas {
                width: 100%;
                height: 100%;
                touch-action: none;
            }
        </style>
        <script>
      var canvas = document.getElementById("renderCanvas");'''
    __code+='''var createScene = function () {var scene = new BABYLON.Scene(engine);'''
    __code+='''scene.clearColor = new BABYLON.Color3'''+str(__backgroundColor)+ ";"
    __code+='''var light = new BABYLON.DirectionalLight("direct", new BABYLON.Vector3(1, 1, 1), scene);var light2 = new BABYLON.DirectionalLight("direct", new BABYLON.Vector3(-1, -1, -1), scene);'''
    __code+='''var camera = new BABYLON.ArcRotateCamera("camera1",  0, 0, 0, new BABYLON.Vector3(0, 0, 0), scene);
            camera.setPosition(new BABYLON.Vector3(0, 5, -30));
             camera.attachControl(canvas, true);'''
    __code+=''' var light = new BABYLON.HemisphericLight("light1", new BABYLON.Vector3(0, 1, 0), scene); // Default intensity is 1. Let's dim the light a small amount
    light.intensity = 0.5;'''


def __drawMeshWithColors(vertices,faces,vertexColors):
    global __code
    __code+="var positions = "+str(vertices)+";"
    __code+="var indices = "+str(faces)+";"
    __code+="var colors = "+str(vertexColors)+";"
    return __code

def __drawTestMesh():
    global __code
    __code+='''    var positions = [-5, 2, -3, -7, -2, -3, -3, -2, -3, 5, 2, 3, 7, -2, 3, 3, -2, 3];
            var indices = [0, 1, 2, 3, 4, 5];    '''

def __end3D():
  global __code
  __code+= '''
        //Create a custom mesh
          var customMesh = new BABYLON.Mesh("custom", scene);
        //Empty array to contain calculated values
          var normals = [];

          var vertexData = new BABYLON.VertexData();
          BABYLON.VertexData.ComputeNormals(positions, indices, normals);

          //Assign positions, indices and normals to vertexData
          vertexData.positions = positions;
          vertexData.indices = indices;
          vertexData.normals = normals;
          vertexData.colors = colors;

          //Apply vertexData to custom mesh
          vertexData.applyToMesh(customMesh);


          /******Display custom mesh in wireframe view to show its creation****************/
          var mat = new BABYLON.StandardMaterial("mat", scene);
          mat.backFaceCulling = false;'''
  if __showWireframe:
    __code+='''mat.wireframe=true;'''
  __code+='''customMesh.material = mat;'''
  if __showEdges:
    __code+= '''customMesh.enableEdgesRendering();'''
    __code+= '''customMesh.edgesWidth = ''' + str(__edgesWidth)+';'
  __code+='''
        /*******************************************************************************/

        var makeTextPlane = function(text, color, size) {
            var dynamicTexture = new BABYLON.DynamicTexture("DynamicTexture", 50, scene, true);
            dynamicTexture.hasAlpha = true;
            dynamicTexture.drawText(text, 5, 40, "bold 36px Arial", color , "transparent", true);
            var plane = new BABYLON.Mesh.CreatePlane("TextPlane", size, scene, true);
            plane.material = new BABYLON.StandardMaterial("TextPlaneMaterial", scene);
            plane.material.backFaceCulling = false;
            plane.material.specularColor = new BABYLON.Color3(0, 0, 0);
            plane.material.diffuseTexture = dynamicTexture;
            return plane;
        };'''
  if __showAxis:
    __code+='''// show axis
            var showAxis = function(size) {
              var axisX = BABYLON.Mesh.CreateLines("axisX", [
                    new BABYLON.Vector3.Zero(), new BABYLON.Vector3(size, 0, 0), new BABYLON.Vector3(size * 0.95, 0.05 * size, 0),
                    new BABYLON.Vector3(size, 0, 0), new BABYLON.Vector3(size * 0.95, -0.05 * size, 0)
                ], scene);
              axisX.color = new BABYLON.Color3(1, 0, 0);
              var xChar = makeTextPlane("X", "red", size / 10);
              xChar.position = new BABYLON.Vector3(0.9 * size, -0.05 * size, 0);
              var axisY = BABYLON.Mesh.CreateLines("axisY", [
                  new BABYLON.Vector3.Zero(), new BABYLON.Vector3(0, size, 0), new BABYLON.Vector3( -0.05 * size, size * 0.95, 0),
                  new BABYLON.Vector3(0, size, 0), new BABYLON.Vector3( 0.05 * size, size * 0.95, 0)
              ], scene);
              axisY.color = new BABYLON.Color3(0, 1, 0);
              var yChar = makeTextPlane("Y", "green", size / 10);
              yChar.position = new BABYLON.Vector3(0, 0.9 * size, -0.05 * size);
              var axisZ = BABYLON.Mesh.CreateLines("axisZ", [
                  new BABYLON.Vector3.Zero(), new BABYLON.Vector3(0, 0, size), new BABYLON.Vector3( 0 , -0.05 * size, size * 0.95),
                  new BABYLON.Vector3(0, 0, size), new BABYLON.Vector3( 0, 0.05 * size, size * 0.95)
              ], scene);
              axisZ.color = new BABYLON.Color3(0, 0, 1);
              var zChar = makeTextPlane("Z", "blue", size / 10);
              zChar.position = new BABYLON.Vector3(0, 0.05 * size, 0.9 * size);
          };
          showAxis(10);'''
  __code+='''return scene;
    };

      var engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true });
      var scene = createScene();

      engine.runRenderLoop(function () {
          if (scene) {scene.render();}
          });

      // Resize
      window.addEventListener("resize", function () {
          engine.resize();
      });
  </script>'''
