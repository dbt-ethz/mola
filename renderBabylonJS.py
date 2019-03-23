#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

__code=""

'''display variables'''
__backgroundColor = (0,0,0)

def displayMesh(mesh):
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
    __code+='''
          var createScene = function () {
             var scene = new BABYLON.Scene(engine);'''
    __code+='''scene.clearColor = new BABYLON.Color3'''
    __code+= "(" + str(__backgroundColor[0]) + ',' + str(__backgroundColor[1]) + ',' + str(__backgroundColor[2]) + ")"
    __code+='''
           var light = new BABYLON.DirectionalLight("direct", new BABYLON.Vector3(1, 1, 1), scene);
             var light2 = new BABYLON.DirectionalLight("direct", new BABYLON.Vector3(-1, -1, -1), scene);
             var camera = new BABYLON.ArcRotateCamera("camera1",  0, 0, 0, new BABYLON.Vector3(0, 0, 0), scene);
            camera.setPosition(new BABYLON.Vector3(0, 5, -30));
             camera.attachControl(canvas, true);
            '''

def __drawMeshWithColors(vertices,faces,vertexColors):
    global __code
    __code+="var positions = "
    __code+=str(vertices)
    __code+=";"
    __code+="var indices = "
    __code+=str(faces)
    __code+=";"
    __code+="var colors = "
    __code+=str(vertexColors);
    __code+=";"
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
            mat.backFaceCulling = false;
            customMesh.material = mat;
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
            };

            // show axis
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
            showAxis(10);
            return scene;
        };

        var engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true });
        var scene = createScene();

        engine.runRenderLoop(function () {
            if (scene) {
                scene.render();
            }
        });

        // Resize
        window.addEventListener("resize", function () {
            engine.resize();
        });
    </script>
  '''

def background(r,g,b):
    global __backgroundColor
    __backgroundColor = (r,g,b)
