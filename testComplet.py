import bpy, os
import random
import functools
from math import *

""" TEXTURING """

def run(theObj, texture):
    # Load image file. Change here if the snippet folder is 
    # not located in you home directory.
    try:
        img = bpy.data.images.load(texture)
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
 
    # Assign UVs to object
    bpy.context.scene.objects.active = theObj
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
 
    # Add material to current object
    ob = bpy.context.object
    me = ob.data
    me.materials.append(mat)
 
    return
	
""" ///////////////////// PLAN 2D \\\\\\\\\\\\\\\\\\\\ """

def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat
 
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

class Vector:

    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z

    def fromPoint(p1,p2,norm=False):
        x=p2.x-p1.x
        y=p2.y-p1.y
        z=p2.z-p1.z
        if norm:
            n=p1.norme(p2)
            x/=n
            y/=n
            z/=n
        return Vector(x,y,z)

    def myprint(self):
        print("x=",self.x," y=",self.y," z=",self.z)

    def __add__(self, vB):
        return Vector(self.x+vB.x,self.y+vB.y,self.z+vB.z) 
    
    def __sub__(self, vB):
        return Vector(self.x-vB.x,self.y-vB.y,self.z-vB.z) 
    
    def __mul__(self, c): 
        if isinstance(c,Vector):
            return  self.x*c.x+self.y*c.y+self.z*c.z  
        else:
            return Vector(c*self.x,c*self.y,c*self.z) 
        
    def __div__(self, c):
        return Vector(self.x/c, self.y/c,self.z/c)
    
    def angle2D(self):
        nb = self.y/self.x
        if nb<0: return (atan(nb))+3.14159
        else: return (atan(nb))
        
    def angle2DVector(self,v):
        return abs(self.angle2D()-v.angle2D())

class Point:
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z
        
    def print(self):
        print("x=",self.x," y=",self.y," z=",self.z)
        
    def cp(self,inv=False):
        if inv:
            return (Point(self.y,self.x,self.z))
        else:
            return (Point(self.x,self.y,self.z))
        
    def norme(self,p):
        return sqrt((p.x-self.x)**2+(p.y-self.y)**2+(p.z-self.z)**2)
    
    def tuple(self):
        return (self.x,self.y,self.z)
    
class Cercle:
    
    def __init__(self,p,r):
        self.point=p
        self.rayon=r
        
    def intersectionDroite(self,dr):
        
        a=dr.a**2+1
        b=2*self.point.x+2*-dr.a*(dr.d-self.point.y)
        c=(self.point.x)**2+(dr.d-self.point.y)**2-self.rayon**2
        
        delta=b**2-4*a*c
        if delta<=0:
            return False
        rac=sqrt(delta)
        
        p1=Point((b-rac)/(2*a),0,0)
        p2=Point((b+rac)/(2*a),0,0)
        
        if p2.x>p1.x:
            p1=p2
            
        p1.y=dr.getY(p1.x)
        
        return p1
        
class Droite:
    
    def __init__(self,p1,p2):
        
        self.p1=p1
        self.p2=p2
        if self.p1.x>self.p2.x:
            self.p1,self.p2=self.p2,self.p1
        self.vector = Vector.fromPoint(self.p1,self.p2)
        self.a=(self.p1.y-self.p2.y)/(self.p1.x-self.p2.x)
        self.d=self.p1.y-self.a*self.p1.x
        
        
    def getY(self,x):
        return self.a*x+self.d
    
    def normePoint(self,p):
        X=-(self.p2.x-self.p1.x)
        Y=-(self.p2.y-self.p1.y)
        Z=p.x*-X+p.y*-Y
        
        proj=Point()
        proj.x=-(self.d*Y+Z)/(X+Y*self.a)
        proj.y=self.a*proj.x+self.d
        
        return p.norme(proj)
   
    def projPoint(self,p):
        X=-(self.p2.x-self.p1.x)
        Y=-(self.p2.y-self.p1.y)
        Z=p.x*-X+p.y*-Y
        
        proj=Point()
        proj.x=-(self.d*Y+Z)/(X+Y*self.a)
        proj.y=self.a*proj.x+self.d
        
        return proj
    
    def norme(self):
        return self.p1.norme(self.p2)
    

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
        dr = []
        rp=[]
        if self.aire()<4:
            print("test aire")
            return [self]
        if self.sens:
            dr.append(Droite(self.points[0].cp(),self.points[1].cp()))
            dr.append(Droite(self.points[2].cp(),self.points[3].cp()))
        else:
            dr.append(Droite(self.points[0].cp(True),self.points[2].cp(True)))
            dr.append(Droite(self.points[1].cp(True),self.points[3].cp(True)))
        
        for i in range(0,2):
            r = Point(random.uniform(dr[i].p1.x+espace,dr[i].p2.x-(espace*2)),0,0)
            r.y=dr[i].getY(r.x)
            rp.append(r)
                
        coupe=Droite(rp[0],rp[1])
        
        for i in range(0,2):
            j=1
            if i==1: j=0
            
            #norme = dr[j].normePoint(rp[i])
            if dr[i].norme()<espace*2 or dr[j].norme()<espace*2 :
                print("to small")
                return [self]
            
            angle=sin(coupe.vector.angle2DVector(dr[i].vector))
            ecart = espace/angle
            c = Cercle(rp[i],ecart)
            intersect = c.intersectionDroite(dr[i])
            p.append(rp[i].cp(not self.sens))
            p.append(intersect.cp(not self.sens))
            
        if self.sens:
            
            self.points[1]=p[0]
            self.points[3]=p[2]
            newPlate.points[0]=p[1]
            newPlate.points[2]=p[3]
            
        else:
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
            
    def aire(self):
        d=Droite(self.points[0],self.points[3])
        p1 = d.projPoint(self.points[1])
        p2= d.projPoint(self.points[2])
        a1 = p1.norme(self.points[1])*p1.norme(self.points[0])/2
        a2= p1.norme(self.points[1])*p1.norme(self.points[3])/2
        a3 = p2.norme(self.points[2])*p2.norme(self.points[0])/2
        a4= p2.norme(self.points[2])*p2.norme(self.points[3])/2
        
        if p1.x<self.points[0].x:
            a1=-a1
        if p1.x>self.points[3].x:
            a2=-a2
        if p2.x<self.points[0].x:
            a3=-a3
        if p2.x>self.points[3].x:
            a4=-a4

        return a1+a2+a3+a4

class Map2D:
    
    def __init__(self):
        self.plates = []
        
    def perform(self, n=1):
        self.plates = [Plate(Point(0,0,0),Point(20,0,0),Point(0,20,0),Point(20,20,0))]
        print(self.plates[0].aire())
        for i in range(0,n):
            newPlates = []
            for j in range(0,len(self.plates)):
                newPlates+=self.plates[j].divide(.5)
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
        m = Map2D()
        m.perform(20)
        print("Hello WOrld")
        
        
        return{'FINISHED'}

class View3dPanel():    
    bl_space_type="VIEW_3D"
    bl_region_type="TOOLS"
    bl_category="City Generator"


class CityGeneratorPanel(View3dPanel,bpy.types.Panel):
    bl_label="City Generator"   
    
    
    def draw(self,context):
        layout=self.layout
        layout.operator(operator = "dh.simple_opt",text = "Create City",icon = "RADIO")
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

bpy.types.Scene.myEnumitem=bpy.props.EnumProperty(name ="Obj Type",items=item_type_lst)
bpy.types.Scene.myEnumitem_obj=bpy.props.EnumProperty(name ="Object",items=item_type_obj)
   
if __name__=='__main__':
    bpy.utils.register_module(__name__)
 
if __name__ == "__main__":
    
    pathTexture = 'C:/Users/User/Documents/GitHub/CityGenerator/Texture/gratteciel.jpg'
    bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
    myObj = bpy.context.object
    run(myObj, pathTexture)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	