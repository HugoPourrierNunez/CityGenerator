

import bpy

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
        layout.operator(operator = "dh.simple_opt",text = "Create City",icon = "OUTLINER_DATA_LAMP")
        self.layout.split()
        self.layout.split()
        self.layout.split()
        
        
        col=layout.column(align = True)
        
        col.label(text = "Parameters")
        col.operator(operator = "mesh.primitive_cube_add",text = "Cube",icon = "MESH_CUBE")
        col.operator(operator = "mesh.primitive_cone_add",text = "Cone",icon = "MESH_CONE")
        row=col.row(align = True)
        row.operator(operator = "mesh.primitive_monkey_add",text = "Monkey",icon = "MESH_MONKEY")
        row.operator(operator = "mesh.primitive_torus_add",text = "Torus",icon = "MESH_TORUS")
        col.operator(operator = "mesh.primitive_cylinder_add",text = "Cylinder",icon = "MESH_CYLINDER")


"""
class PanelB(View3dPanel,bpy.types.Panel):
    bl_label="Panel B"
    
    def draw(self,context):
        layout=self.layout
        layout=layout.box()
        layout.label(text = "object list",icon = "SORTALPHA")
        col=layout.column(align = False)
        col.prop(data = context.scene,property = "myEnumitem")
        col.prop(data = context.scene,property = "myEnumitem_obj")
"""        
               


bpy.types.Scene.myEnumitem=bpy.props.EnumProperty(name ="Obj Type",items=item_type_lst)
bpy.types.Scene.myEnumitem_obj=bpy.props.EnumProperty(name ="Object",items=item_type_obj)


if __name__=='__main__':
    bpy.utils.register_module(__name__)

