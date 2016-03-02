import bpy, os
import random
import functools
from math import *

""" TEXTURING """

def run(obj, texture):
    # Load image file. Change here if the snippet folder is 
    # not located in you home directory.
    realpath = os.path.expanduser(texture)
    try:
        img = bpy.data.images.load(realpath)
    except:
        raise NameError("Cannot load image %s" % realpath)
 
    # Create image texture from image
    cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
    cTex.image = img
 
    # Create procedural texture 
    sTex = bpy.data.textures.new('BumpTex', type = 'STUCCI')
    sTex.noise_basis = 'BLENDER_ORIGINAL' 
    sTex.noise_scale = 0.25 
    sTex.noise_type = 'SOFT_NOISE' 
    sTex.saturation = 1 
    sTex.stucci_type = 'PLASTIC' 
    sTex.turbulence = 5 
 
    # Create blend texture with color ramp
    # Don't know how to add elements to ramp, so only two for now
    bTex = bpy.data.textures.new('BlendTex', type = 'BLEND')
    bTex.progression = 'SPHERICAL'
    bTex.use_color_ramp = True
    ramp = bTex.color_ramp
    values = [(0.6, (1,1,1,1)), (0.8, (0,0,0,1))]
    for n,value in enumerate(values):
        elt = ramp.elements[n]
        (pos, color) = value
        elt.position = pos
        elt.color = color
 
    # Create material
    mat = bpy.data.materials.new('TexMat')
 
    # Add texture slot for color texture
    mtex = mat.texture_slots.add()
    mtex.texture = cTex
    mtex.texture_coords = 'UV'
    mtex.use_map_color_diffuse = True 
    mtex.use_map_color_emission = True 
    mtex.emission_color_factor = 0.5
    mtex.use_map_density = True 
    mtex.mapping = 'FLAT' 
 
    # Add texture slot for bump texture
    mtex = mat.texture_slots.add()
    mtex.texture = sTex
    mtex.texture_coords = 'ORCO'
    mtex.use_map_color_diffuse = False
    mtex.use_map_normal = True 
    #mtex.rgb_to_intensity = True
 
    # Add texture slot 
    mtex = mat.texture_slots.add()
    mtex.texture = bTex
    mtex.texture_coords = 'UV'
    mtex.use_map_color_diffuse = True 
    mtex.diffuse_color_factor = 1.0
    mtex.blend_type = 'MULTIPLY'
 
    # Create new cube and give it UVs
    obj.mode_set(mode='EDIT')
    obj.uv.smart_project()
    obj.object.mode_set(mode='OBJECT')
 
    # Add material to current object
    ob = bpy.context.object
    me = ob.data
    me.materials.append(mat)
 
    return
	
""" ///////////////////// PLAN 2D \\\\\\\\\\\\\\\\\\\\"""

class Point:
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z
    def print(self):
        print("x=",self.x," y=",self.y," z=",self.z)
        
    def cp(self):
        return (Point(self.x,self.y,self.z))

class Plate:
    MIN=1
    
    def __init__(self, p1=Point(),p2=Point(),p3=Point(),p4=Point()):
        self.points = [p1,p2,p3,p4]
        self.sens=True
    
    def setPoint(self,index,p):
        if index>-1 and index<4:
            self.points[index] = p
            
    def divide(self,espace=0):
        #divide
        newPlate = Plate()
        newPlate.points = self.points[:]
        p = []
        if self.sens:
            """if abs(self.points[0].x-self.points[1].x)<Plate.MIN or abs(self.points[2].x-self.points[3].x)<Plate.MIN:
                self.sens = not self.sens
                return [self]"""
            #on prend au hasard un point sur chaque bord
            print("true")
            for i in range(0,3,2):
                p1=self.points[i].cp()
                p2=self.points[i+1].cp()
                if p1.x>p2.x:
                    p1,p2=p2,p1
                print("i=",i)
                a = (p1.y-p2.y)/(p1.x-p2.x)
                print("a=",a)
                d = p1.y-a*p1.x
                print("d=",d)
                
                rx = 10#random.uniform(p1.x+espace/2,p2.x-espace/2)
                
                ry=a*rx+d
                #bpy.ops.mesh.primitive_plane_add(location=(rx,ry,0))
                delta=(2*rx+2*-a*(d-ry))**2-4*(a**2+1)*(rx**2+(d-ry)**2-(espace/2)**2)
                print("delta=",delta)
                x1=((2*rx+2*-a*(d-ry))-sqrt(delta))/(2*(a**2+1))
                x2=((2*rx+2*-a*(d-ry))+sqrt(delta))/(2*(a**2+1))
                
                p.append(Point(x1, a*x1+d,0))
                p.append(Point(x2, a*x2+d,0))
            
            self.points[1]=p[0]
            self.points[3]=p[2]
            
            newPlate.points[0]=p[1]
            newPlate.points[2]=p[3]
        
        else:
            print("false")
            """if abs(self.points[0].y-self.points[2].y)<Plate.MIN or abs(self.points[1].y-self.points[3].y)<Plate.MIN:
                self.sens = not self.sens
                return [self]"""
            for i in range(0,2):
                print("p1=",self.points[i].print())
                print("p2=",self.points[i+2].print())
                a = (self.points[i].x-self.points[i+2].x)/(self.points[i].y-self.points[i+2].y)
                print("a=",a)
                d = self.points[i].x-a*self.points[i].y
                print("d=",d)
                if self.points[i].y>self.points[i+2].y:
                    rx = random.uniform(self.points[i+2].y+espace/2,self.points[i].y-espace/2)
                else :
                    rx = random.uniform(self.points[i].y+espace/2,self.points[i+2].y-espace/2)
                ry=a*rx+d
                delta=(2*rx+2*-a*(d-ry))**2-4*(a**2+1)*(rx**2+(d-ry)**2-(espace/2)**2)
                print("delta=",delta)
                x1=((2*rx+2*-a*(d-ry))-sqrt(delta))/(2*(a**2+1))
                x2=((2*rx+2*-a*(d-ry))+sqrt(delta))/(2*(a**2+1))
                p.append(Point(a*x1+d,x1,0))
                p.append(Point(a*x2+d,x2,0))
                
            self.points[2]=p[0]
            self.points[3]=p[2]
            
            newPlate.points[0]=p[1]
            newPlate.points[1]=p[3]
        
        self.sens=not self.sens
        newPlate.sens=self.sens
        
        return [self,newPlate]
    
    def draw(self):
        bpy.ops.mesh.primitive_plane_add(location=(0,0,0))
        obj=bpy.context.object
        for i in range(0,4):
            obj.data.vertices[i].co.x=self.points[i].x
            obj.data.vertices[i].co.y=self.points[i].y
            obj.data.vertices[i].co.z=self.points[i].z

class Map2D:
    
    def __init__(self):
        self.plates = []
        
    def perform(self, n=1):
        self.plates = [Plate(Point(0,-10,0),Point(20,0,0),Point(0,20,0),Point(20,20,0))]
        #self.plates[0].draw()
        for i in range(0,n):
            newPlates = []
            for j in range(0,len(self.plates)):
                newPlates+=self.plates[j].divide(.1)
            self.plates=newPlates
        for i in range(0,len(self.plates)):
            self.plates[i].draw()


""" ///////////////////// PANEL \\\\\\\\\\\\\\\\\\\\\ """

def item_type_lst(self,context):
    types={obj.type:obj.type for obj in context.scene.objects}
    return [(obj,obj,"")for obj in types]



def item_type_obj(self,context):
    return[(obj.name,obj.name,"") for obj in context.scene.objects if obj.type==context.scene.myEnumitem]

class SimpleOperator(bpy.types.Operator):
    bl_idname="dh.simple_opt"
    bl_label="Simple Operator"
    
    def execute(self,context):
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.mesh.primitive_cone_add()
        print("Hello WOrld")
        
        
        return{'FINISHED'}

class View3dPanel():    
    bl_space_type="VIEW_3D"
    bl_region_type="TOOLS"
    bl_category="City Generator"


class CityGenerator(View3dPanel,bpy.types.Panel):
    bl_label="City Generator"   
    
    
    def draw(self,context):
        layout=self.layout
        layout.operator(operator = "dh.simple_opt",text = "Create City",icon = "RADIO")
        self.layout.split()
        self.layout.split()
        self.layout.split()
        
        

        col=layout.column(align = True)
        sub = col.column(align=True)
        scene = context.scene
        rd = scene.render
        sub.label(text = "// Parameters : \\")
        sub.label(text = "")
        sub.label(text = "Dimensions:")
        sub.prop(rd, "resolution_x", text="X")
        sub.prop(rd, "resolution_y", text="Y")
        sub.label(text="")
        sub.label(text="Streets :")
        sub.prop(scene, "frame_step")
        col.operator(operator = "mesh.primitive_cube_add",text = "Cube",icon = "MESH_CUBE")
        col.operator(operator = "mesh.primitive_cone_add",text = "Cone",icon = "MESH_CONE")
        row=col.row(align = True)
        row.operator(operator = "mesh.primitive_monkey_add",text = "Monkey",icon = "MESH_MONKEY")
        row.operator(operator = "mesh.primitive_torus_add",text = "Torus",icon = "MESH_TORUS")
        col.operator(operator = "mesh.primitive_cylinder_add",text = "Cylinder",icon = "MESH_CYLINDER")


bpy.types.Scene.myEnumitem=bpy.props.EnumProperty(name ="Obj Type",items=item_type_lst)
bpy.types.Scene.myEnumitem_obj=bpy.props.EnumProperty(name ="Object",items=item_type_obj)

	
""" ///////////////////// PANEL \\\\\\\\\\\\\\\\\\\\\ """

def item_type_lst(self,context):
    types={obj.type:obj.type for obj in context.scene.objects}
    return [(obj,obj,"")for obj in types]



def item_type_obj(self,context):
    return[(obj.name,obj.name,"") for obj in context.scene.objects if obj.type==context.scene.myEnumitem]

class SimpleOperator(bpy.types.Operator):
    bl_idname="dh.simple_opt"
    bl_label="Simple Operator"
    
    def execute(self,context):
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.mesh.primitive_cone_add()
        print("Hello WOrld")
        
        
        return{'FINISHED'}

class View3dPanel():    
    bl_space_type="VIEW_3D"
    bl_region_type="TOOLS"
    bl_category="City Generator"


class CityGenerator(View3dPanel,bpy.types.Panel):
    bl_label="City Generator"   
    
    
    def draw(self,context):
        layout=self.layout
        layout.operator(operator = "dh.simple_opt",text = "Create City",icon = "RADIO")
        self.layout.split()
        self.layout.split()
        self.layout.split()
        
        

        col=layout.column(align = True)
        sub = col.column(align=True)
        scene = context.scene
        rd = scene.render
        sub.label(text = "// Parameters : \\")
        sub.label(text = "")
        sub.label(text = "Dimensions:")
        sub.prop(rd, "resolution_x", text="X")
        sub.prop(rd, "resolution_y", text="Y")
        sub.label(text="")
        sub.label(text="Streets :")
        sub.prop(scene, "frame_step")
        col.operator(operator = "mesh.primitive_cube_add",text = "Cube",icon = "MESH_CUBE")
        col.operator(operator = "mesh.primitive_cone_add",text = "Cone",icon = "MESH_CONE")
        row=col.row(align = True)
        row.operator(operator = "mesh.primitive_monkey_add",text = "Monkey",icon = "MESH_MONKEY")
        row.operator(operator = "mesh.primitive_torus_add",text = "Torus",icon = "MESH_TORUS")
        col.operator(operator = "mesh.primitive_cylinder_add",text = "Cylinder",icon = "MESH_CYLINDER")


bpy.types.Scene.myEnumitem=bpy.props.EnumProperty(name ="Obj Type",items=item_type_lst)
bpy.types.Scene.myEnumitem_obj=bpy.props.EnumProperty(name ="Object",items=item_type_obj)
   
if __name__=='__main__':
    bpy.utils.register_module(__name__)
 
if __name__ == "__main__":
    m = Map2D()
    m.perform(5)
    myObj = bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
    run(myObj, 'C:/Users/User/Documents/GitHub/CityGenerator/Texture/gratteciel.jpg')
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	