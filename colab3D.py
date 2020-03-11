#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

__code=""

'''display variables'''
__showAxis=True
__showEdges=False
__edgesWidth=1.0
__showWireframe=False
__showPointsCloud=False
__showPointsNumbers=False
__backgroundColor = (0,0,0)
__edgesColor = (1,1,1,1)
__pointColor = (1,1,1)
__pointSize = 10
__numberColor = (1,1,1)
__numberSize = 1
__canvasWidth = "100%"
__canvasHeight = "56.25vw"

__positionsWelded = []

def display_mesh(mesh,canvasWidth=None,canvasHeight=None,showAxis=True,showEdges=False,edgesWidth=1.0,showWireframe=False,showPointsCloud=False,showPointsNumbers=False,backgroundColor=(0,0,0),edgesColor=(1,1,1,1),pointColor=(1,1,1),pointSize=10,numberColor=(1,1,1),numberSize=1):
  """
  Displays Mesh.
  Arguments:
  ----------
  mesh : mola.core.Mesh
         The mesh to be displayed

  Optional Arguments:
  ----------
  canvasWidth : float
  canvasHeight : float
  showAxis : Boolean
  showEdges : Boolean
  showWireframe : Boolean
  showPointsCloud : Boolean
  showPointsNumbers : Boolean
  edgesWidth : float
  backgroundColor : tuple (r,g,b)
                    r,g,b values, 0.0 to 1.0
  edgesColor : tuple (r,g,b,a)
              r,g,b,a values, 0.0 to 1.0
  pointColor : tuple (r,g,b)
                r,g,b values, 0.0 to 1.0
  pointSize : float
  numberColor : tuple (r,g,b)
                r,g,b values, 0.0 to 1.0
  numberSize : float
  """
  global __canvasWidth, __canvasHeight, __showAxis,__showEdges,__edgesWidth,__showWireframe,__showPointsCloud,__showPointsNumbers,__backgroundColor,__edgesColor,__pointColor,__pointSize,__numberColor,__numberSize
  if(canvasWidth):
    __canvasWidth = str(canvasWidth) + "px"
  if(canvasHeight):
    __canvasHeight = str(canvasHeight) + "px"
  __showAxis=showAxis
  __showEdges=showEdges
  __edgesWidth=edgesWidth
  __showWireframe=showWireframe
  __showPointsCloud = showPointsCloud
  __showPointsNumbers = showPointsNumbers
  __backgroundColor = backgroundColor
  __edgesColor = edgesColor
  __pointColor = pointColor
  __pointSize = pointSize
  __numberColor = numberColor
  __numberSize = numberSize

  if(showPointsNumbers):
    global __positionsWelded
    __positionsWelded = []
    for v in mesh.vertices:
      __positionsWelded.extend((v.x,v.y,v.z))

  return display_faces(mesh.faces)



def display_faces_welded(faces):
    __begin3D()
    verticesDict={}
    positions=[]
    indices=[]
    colors=[]
    cIndex=0
    for face in faces:
        col=face.color
        # triangle
        for i in range(3):
            p=face.vertices[i]
            ptuple = (p.x,p.y,p.z)
            if ptuple in verticesDict:
                indices.append(verticesDict[ptuple])
            else:
                verticesDict[ptuple]=cIndex
                positions.extend(ptuple)
                colors.extend(face.color)
                indices.append(cIndex)
                cIndex+=1
        # quad
        if len(face.vertices)>3:
            p=face.vertices[3]
            ptuple = (p.x,p.y,p.z)
            i0=indices[-3]
            i1=indices[-1]
            indices.append(i0)
            indices.append(i1)
            if ptuple in verticesDict:
                indices.append(verticesDict[ptuple])
            else:
                verticesDict[ptuple]=cIndex
                positions.extend(ptuple)
                colors.extend(face.color)
                indices.append(cIndex)
                cIndex+=1
    __draw_mesh_with_colors(positions, indices, colors)
    __end3D()
    return __code




def display_faces(faces):
    __begin3D()
    positions=[]
    indices=[]
    colors=[]

    cIndex=0
    for face in faces:
        for v in face.vertices:
            positions.extend((v.x,v.y,v.z))
            colors.extend(face.color)
        indices.extend([cIndex, cIndex+1, cIndex+2])
        if len(face.vertices)>3:
            # indices.extend([cIndex+2, cIndex+3, cIndex])
            for i in range(2,len(face.vertices)-1):
                indices.extend([cIndex+i, cIndex+i+1, cIndex])
        cIndex+=len(face.vertices)
    __draw_mesh_with_colors(positions, indices, colors)
    __end3D()
    return __code

def __begin3D():
    global __code
    __code=""
    __code+='''<canvas id="renderCanvas" touch-action="none"></canvas>
        <script src="https://cdn.babylonjs.com/babylon.js"></script>
        <style>
            html, body {
                overflow: hidden;
                width:''' + __canvasWidth + ''';
                height: ''' + __canvasHeight + ''';
                margin: 0;
                padding: 0;
            }
            #renderCanvas {
                width:''' + __canvasWidth + ''';
                height: ''' + __canvasHeight + ''';
                touch-action: none;
            }
        </style>
        <script>
      var canvas = document.getElementById("renderCanvas");'''
    __code+='''var createScene = function () {var scene = new BABYLON.Scene(engine);'''
    __code+='''scene.useRightHandedSystem = true;'''
    __code+='''scene.clearColor = new BABYLON.Color3'''+str(__backgroundColor)+ ";"
    __code+='''var light = new BABYLON.DirectionalLight("direct", new BABYLON.Vector3(1, 1, 1), scene);var light2 = new BABYLON.DirectionalLight("direct", new BABYLON.Vector3(-1, -1, -1), scene);'''
    __code+='''var camera = new BABYLON.ArcRotateCamera("camera1",  0, 0, 0, new BABYLON.Vector3(0, 0, 0), scene);
            camera.setPosition(new BABYLON.Vector3(0, 5, 30));
             camera.attachControl(canvas, true);'''
    __code+=''' var light = new BABYLON.HemisphericLight("light1", new BABYLON.Vector3(0, 1, 0), scene);
    light.intensity = 0.5;'''


def __draw_mesh_with_colors(vertices,faces,vertexColors):
    global __code
    __code+="var positions = "+str(vertices)+";"
    __code+="var indices = "+str(faces)+";"
    __code+="var colors = "+str(vertexColors)+";"
    return __code

"""
def __draw_test_mesh():
    global __code
    __code+='''    var positions = [-5, 2, -3, -7, -2, -3, -3, -2, -3, 5, 2, 3, 7, -2, 3, 3, -2, 3];
            var indices = [0, 1, 2, 3, 4, 5];    '''
"""
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
          var mat = new BABYLON.StandardMaterial("mat", scene);
          mat.backFaceCulling = false;'''
  if __showWireframe:
    __code+='''mat.wireframe=true;'''
  if __showPointsCloud:
    __code+='''mat.pointsCloud=true;'''
    __code+='''mat.pointSize=''' + str(__pointSize) + ';'
    __code+='''mat.diffuseColor = new BABYLON.Color3'''+str(__pointColor)+ ';'
    __code+='''mat.emissiveColor = new BABYLON.Color3'''+str(__pointColor)+ ';'
    __code+='''mat.disableLighting = true; '''
  if __showEdges:
    __code+= '''customMesh.enableEdgesRendering();'''
    __code+= '''customMesh.edgesWidth = ''' + str(__edgesWidth * 10) +';'
    __code+= '''customMesh.edgesColor = new BABYLON.Color4'''+str(__edgesColor)+ ';'
  if __showPointsNumbers:
    __code+='''
    var drawNumber = function(scene, text, posVector){
      //data reporter
      var outputplane = BABYLON.Mesh.CreatePlane("outputplane", 1.5, scene, false);
      outputplane.billboardMode = BABYLON.AbstractMesh.BILLBOARDMODE_ALL;
      outputplane.material = new BABYLON.StandardMaterial("outputplane", scene);
      outputplane.position = posVector;
      outputplane.scaling.x = '''+str(__numberSize)+ ''';
      outputplane.scaling.y = '''+str(__numberSize)+ ''';
      var outputplaneTexture = new BABYLON.DynamicTexture("dynamic texture", 512, scene, true);
      outputplane.material.diffuseTexture = outputplaneTexture;
      outputplane.material.diffuseColor = new BABYLON.Color3'''+str(__numberColor)+ ''';
      outputplane.material.emissiveColor = new BABYLON.Color3'''+str(__numberColor)+ ''';
      outputplane.material.backFaceCulling = false;
      //outputplaneTexture.getContext().clearRect(0, 140, 512, 512);
      var textColor = new BABYLON.Color3''' + str(__numberColor) + '''.toHexString();
      outputplaneTexture.drawText(text, null, 300, "200px arial", textColor);
      outputplaneTexture.hasAlpha = true;
    };'''
    __code+='''
    //drawNumber(scene,"NT",new BABYLON.Vector3(0,0,0));
    //var vPositions = customMesh.getVerticesData(BABYLON.VertexBuffer.PositionKind);
    //console.log("vplength " + vPositions.length);
    var ind = 0;
    var pWelded = ''' +str(__positionsWelded)+ ''';
    for(var i=0;i<pWelded.length;i+=3){
      var posX = (pWelded[i]);
      var posY = (pWelded[i+1]);
      var posZ = (pWelded[i+2]);
      drawNumber(scene,ind.toString(),new BABYLON.Vector3(posX,posY+1,posZ));
      ind++;
    }
    '''
  if __showAxis:
    __code+='''
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
  __code+='''customMesh.material = mat;'''
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
