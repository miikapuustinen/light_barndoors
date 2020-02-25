# # # ADDON INFO# # #
bl_info = {
        "name": "Barndoor Light",
    	"description": "Menu",
        "category": "Object",
    	"version": (0, 2, 1),
    	"blender": (2, 80, 0),
        "author": "Miika Puustinen"
        }


import bpy


class OBJECT_OT_barndoor_light(bpy.types.Operator):
    bl_idname = "object.barndoor_light" # name used to refer to this operator
    bl_label = "Barndoor Light" # operator's label
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add Spotlight with Barndoors" # tooltip

    def execute(self, context):
        scene = bpy.context.scene

        # add light data
        light_data = bpy.data.lights.new(name="spot_light_data", type='SPOT')

        # add light ojbect
        light_object = bpy.data.objects.new(name="Spot light", object_data=light_data)

        # add light to scene
        spot = scene.collection.objects.link(light_object)

        light_data.use_nodes = True


        # ADD NODES
        output_node = light_data.node_tree.nodes['Light Output']
        output_node.location = (900,300)

        emission1 = light_data.node_tree.nodes['Emission']
        emission1.location = (300,300)

        mix_rgb = light_data.node_tree.nodes.new('ShaderNodeMixRGB')
        mix_rgb.blend_type = 'MULTIPLY'
        mix_rgb.inputs[0].default_value = 1.0
        mix_rgb.location = (emission1.location[0] -250, emission1.location[1])

        # multiply1
        multiply1 = light_data.node_tree.nodes.new('ShaderNodeMath')
        multiply1.operation = 'MULTIPLY'
        multiply1.location = (-300,300)

        # multiply2
        multiply2 = light_data.node_tree.nodes.new('ShaderNodeMath')
        multiply2.operation = 'MULTIPLY'
        multiply2.location = (-600,450)

        # multiply3
        multiply3 = light_data.node_tree.nodes.new('ShaderNodeMath')
        multiply3.operation = 'MULTIPLY'
        multiply3.location = (-600,150)

        # ramp1
        ramp1 = light_data.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp1.color_ramp.interpolation = 'CONSTANT'
        ramp1.color_ramp.elements[0].color = (1,1,1,1)
        ramp1.color_ramp.elements[1].color = (0,0,0,1)
        ramp1.location = (-1000,900)

        # ramp1
        ramp2 = light_data.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp2.color_ramp.interpolation = 'CONSTANT'
        ramp2.color_ramp.elements[0].color = (1,1,1,1)
        ramp2.color_ramp.elements[1].color = (0,0,0,1)
        ramp2.location = (ramp1.location[0],ramp1.location[1] - 300)

        # ramp1
        ramp3 = light_data.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp3.color_ramp.interpolation = 'CONSTANT'
        ramp3.color_ramp.elements[0].color = (1,1,1,1)
        ramp3.color_ramp.elements[1].color = (0,0,0,1)
        ramp3.location = (ramp2.location[0],ramp2.location[1] - 300)

        # ramp1
        ramp4 = light_data.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp4.color_ramp.interpolation = 'CONSTANT'
        ramp4.color_ramp.elements[0].color = (1,1,1,1)
        ramp4.color_ramp.elements[1].color = (0,0,0,1)
        ramp4.location = (ramp3.location[0],ramp3.location[1] - 300)


        # gradient1
        gradient1 = light_data.node_tree.nodes.new('ShaderNodeTexGradient')
        gradient1.location = (ramp1.location[0] -300, ramp1.location[1])

        # gradient2
        gradient2 = light_data.node_tree.nodes.new('ShaderNodeTexGradient')
        gradient2.location = (gradient1.location[0], gradient1.location[1]-300)

        # gradient2
        gradient3 = light_data.node_tree.nodes.new('ShaderNodeTexGradient')
        gradient3.location = (gradient2.location[0], gradient2.location[1]-300)

        # gradient2
        gradient4 = light_data.node_tree.nodes.new('ShaderNodeTexGradient')
        gradient4.location = (gradient3.location[0], gradient3.location[1]-300)


        # mapping1
        mapping1 = light_data.node_tree.nodes.new('ShaderNodeMapping')
        mapping1.location = (gradient1.location[0] -500, gradient1.location[1])
        mapping1.inputs[2].default_value[1] = 3.141593


        # mapping2
        mapping2 = light_data.node_tree.nodes.new('ShaderNodeMapping')
        mapping2.location = (gradient3.location[0] -500, gradient3.location[1]+100)
        mapping2.inputs[2].default_value[2] = 1.570796

        # mapping3
        mapping3 = light_data.node_tree.nodes.new('ShaderNodeMapping')
        mapping3.location = (gradient4.location[0] -500, gradient4.location[1])
        mapping3.inputs[2].default_value[2] = -1.570796

        # reroute
        reroute1 = light_data.node_tree.nodes.new('NodeReroute')
        reroute1.location = (gradient2.location[0]-1000, gradient2.location[1]-100)

        # combine_XYZ
        combine_xyz1 = light_data.node_tree.nodes.new('ShaderNodeCombineXYZ')
        combine_xyz1.location = (reroute1.location[0] -300, reroute1.location[1]+50)

        # divide1
        divide1 = light_data.node_tree.nodes.new('ShaderNodeMath')
        divide1.operation = 'DIVIDE'
        divide1.location = (combine_xyz1.location[0]-300 ,combine_xyz1.location[1]+100)

        # divide2
        divide2 = light_data.node_tree.nodes.new('ShaderNodeMath')
        divide2.operation = 'DIVIDE'
        divide2.location = (combine_xyz1.location[0]-300 ,combine_xyz1.location[1]-100)

        # combine_XYZ
        separate_xyz1 = light_data.node_tree.nodes.new('ShaderNodeSeparateXYZ')
        separate_xyz1.location = (combine_xyz1.location[0]-600 ,combine_xyz1.location[1])


        # mapping4
        # mapping4 = light_data.node_tree.nodes.new('ShaderNodeMapping')
        # mapping4.location = (separate_xyz1.location[0] -600, separate_xyz1.location[1])
        # mapping4.use_min = True
        # mapping4.use_max = True
        # mapping4.min[0] = -1.0
        # mapping4.min[1] = -1.0
        # mapping4.min[2] = -1.0


        # mapping5
        # mapping5 = light_data.node_tree.nodes.new('ShaderNodeMapping')
        # mapping5.location = (mapping4.location[0] -400, mapping4.location [1])
        #
        # # mapping6
        # mapping6 = light_data.node_tree.nodes.new('ShaderNodeMapping')
        # mapping6.location = (mapping5.location[0] -400, mapping5.location [1])


        # geometry node
        #geometry1 = light_data.node_tree.nodes.new('ShaderNodeNewGeometry')
        #geometry1.location = (mapping6.location[0] -400, mapping6.location [1])

        tex_coord1 = light_data.node_tree.nodes.new('ShaderNodeTexCoord')
        tex_coord1.location = (separate_xyz1.location[0] -400, separate_xyz1.location [1])

        # create a group
        test_group = bpy.data.node_groups.new('BarndoorSettings', 'ShaderNodeTree')

        # create group inputs
        group_inputs = test_group.nodes.new('NodeGroupInput')
        group_inputs.location = (-350,0)
        test_group.inputs.new('NodeSocketShader','Shader In')
        light_color = test_group.inputs.new('NodeSocketColor','Light Color')
        light_color.default_value = (1,1,1,1)
        strength = test_group.inputs.new('NodeSocketFloat','Light Strength')
        strength.min_value = 0
        strength.default_value = 100.0
        left = test_group.inputs.new('NodeSocketFloat','Left')
        left.min_value = 0
        left.max_value = 1.0
        right = test_group.inputs.new('NodeSocketFloat','Right')
        right.min_value = 0
        right.max_value = 1.0
        top = test_group.inputs.new('NodeSocketFloat','Top')
        top.min_value = 0
        top.max_value = 1.0
        bottom = test_group.inputs.new('NodeSocketFloat','Bottom')
        bottom.min_value = 0
        bottom.max_value = 1.0


        # create group outputs
        group_outputs = test_group.nodes.new('NodeGroupOutput')
        group_outputs.location = (300,0)
        test_group.outputs.new('NodeSocketShader','Shader Out')

        # link group in - group out
        test_group.links.new(group_inputs.outputs['Shader In'], group_outputs.inputs['Shader Out'])

        # add group to the scene
        barndoor_settings = light_data.node_tree.nodes.new('ShaderNodeGroup')
        barndoor_settings.location = (550,300)
        barndoor_settings.node_tree = test_group


        # CREATE NODE LINKS
        links = light_data.node_tree.links
        link = links.new(barndoor_settings.outputs[0], output_node.inputs[0])
        link = links.new(emission1.outputs[0], barndoor_settings.inputs[0])
        link = links.new(mix_rgb.outputs[0], emission1.inputs[0])
        link = links.new(multiply1.outputs[0], mix_rgb.inputs[1])
        link = links.new(multiply2.outputs[0], multiply1.inputs[0])
        link = links.new(multiply3.outputs[0], multiply1.inputs[1])
        link = links.new(ramp1.outputs[0], multiply2.inputs[0])
        link = links.new(ramp2.outputs[0], multiply2.inputs[1])
        link = links.new(ramp3.outputs[0], multiply3.inputs[0])
        link = links.new(ramp4.outputs[0], multiply3.inputs[1])
        link = links.new(gradient1.outputs[0], ramp1.inputs[0])
        link = links.new(gradient2.outputs[0], ramp2.inputs[0])
        link = links.new(gradient3.outputs[0], ramp3.inputs[0])
        link = links.new(gradient4.outputs[0], ramp4.inputs[0])
        link = links.new(mapping1.outputs[0], gradient1.inputs[0])
        link = links.new(reroute1.outputs[0], gradient2.inputs[0])
        link = links.new(mapping2.outputs[0], gradient3.inputs[0])
        link = links.new(mapping3.outputs[0], gradient4.inputs[0])
        link = links.new(reroute1.outputs[0], mapping1.inputs[0])
        link = links.new(reroute1.outputs[0], mapping2.inputs[0])
        link = links.new(reroute1.outputs[0], mapping3.inputs[0])
        link = links.new(combine_xyz1.outputs[0], reroute1.inputs[0])
        link = links.new(divide1.outputs[0], combine_xyz1.inputs[0])
        link = links.new(divide2.outputs[0], combine_xyz1.inputs[1])
        link = links.new(separate_xyz1.outputs[0], divide1.inputs[0])
        link = links.new(separate_xyz1.outputs[1], divide2.inputs[0])
        link = links.new(separate_xyz1.outputs[2], divide1.inputs[1])
        link = links.new(separate_xyz1.outputs[2], divide2.inputs[1])
        link = links.new(separate_xyz1.outputs[2], combine_xyz1.inputs[2])
        #link = links.new(mapping4.outputs[0], separate_xyz1.inputs[0])
        #link = links.new(mapping5.outputs[0], mapping4.inputs[0])
        #link = links.new(mapping6.outputs[0], mapping5.inputs[0])
        link = links.new(tex_coord1.outputs[1], separate_xyz1.inputs[0])


        # CREATE DRIVERS
        def add_driver_variable(driven, ob_name, property):
            # Create variable
            newVar = driven.driver.variables.new()
            newVar.name = "var"

            # If driver is the sky settings
            if ob_name == 'light':
                newVar.targets[0].id_type = 'LIGHT'
                newVar.targets[0].id = light_data
                newVar.targets[0].data_path = property
                driven.driver.expression = "var"

            # if driver is an object
            else:
                newVar.targets[0].id_type = 'OBJECT'
                newVar.targets[0].id = ob_name
                newVar.type = 'TRANSFORMS'
                newVar.targets[0].transform_type = property
                driven.driver.expression = "-var"

            return None

        nodes = light_data.node_tree.nodes

        # Add driver
        driver1 = nodes[ramp1.name].color_ramp.elements[1].driver_add('position')

        # Define property for driver (string)
        property1 = 'node_tree.nodes["Group"].inputs[3].default_value'

        # Add driver variables and links
        add_driver_variable(driver1, 'light', property1)

        # Change driver expression
        driver1.driver.expression = '1-var'


        # ramp2
        driver2 = nodes[ramp2.name].color_ramp.elements[1].driver_add('position')
        property2 = 'node_tree.nodes["Group"].inputs[4].default_value'
        add_driver_variable(driver2, 'light', property2)
        driver2.driver.expression = '1-var'

        # ramp3
        driver3 = nodes[ramp3.name].color_ramp.elements[1].driver_add('position')
        property3 = 'node_tree.nodes["Group"].inputs[5].default_value'
        add_driver_variable(driver3, 'light', property3)
        driver3.driver.expression = '1-var'

        # ramp4
        driver4 = nodes[ramp4.name].color_ramp.elements[1].driver_add('position')
        property4 = 'node_tree.nodes["Group"].inputs[6].default_value'
        add_driver_variable(driver4, 'light', property4)
        driver4.driver.expression = '1-var'

        # emission1
        driver5 = nodes[emission1.name].inputs[1].driver_add('default_value')
        property5 = 'node_tree.nodes["Group"].inputs[2].default_value'
        add_driver_variable(driver5, 'light', property5)

        # Light color RED
        driver6 = nodes[mix_rgb.name].inputs['Color2'].driver_add('default_value', 0)
        property6 = 'node_tree.nodes["Group"].inputs[1].default_value[0]'
        add_driver_variable(driver6, 'light', property6)

        # Light color GREEN
        driver7 = nodes[mix_rgb.name].inputs['Color2'].driver_add('default_value', 1)
        property7 = 'node_tree.nodes["Group"].inputs[1].default_value[1]'
        add_driver_variable(driver7, 'light', property7)

        # Light color BLUE
        driver8 = nodes[mix_rgb.name].inputs['Color2'].driver_add('default_value', 2)
        property8 = 'node_tree.nodes["Group"].inputs[1].default_value[2]'
        add_driver_variable(driver8, 'light', property8)

        # Close barn doors for visibility

        # light = light_object
        light_data.node_tree.nodes["Group"].inputs[3].default_value = 0.75
        light_data.node_tree.nodes["Group"].inputs[4].default_value = 0.75
        light_data.node_tree.nodes["Group"].inputs[5].default_value = 0.75
        light_data.node_tree.nodes["Group"].inputs[6].default_value = 0.75

        # driver9 = nodes[mapping4.name].inputs[2].driver_add('default_value', 0)
        # property9 = 'ROT_X'
        # add_driver_variable(driver9, light_object, property9)
        #
        #
        # driver10 = nodes[mapping5.name].inputs[2].driver_add('.default_value', 1)
        # property10 = 'ROT_Y'
        # add_driver_variable(driver10, light_object, property10)
        #
        # driver11 = nodes[mapping6.name].inputs[2].driver_add('default_value', 2)
        # property11 = 'ROT_Z'
        # add_driver_variable(driver11, light_object, property11)

        return{'FINISHED'}


def menu_item(self, context):
       self.layout.operator(OBJECT_OT_barndoor_light.bl_idname, text="Barndoors", icon="LIGHT_HEMI")

# Register
classes = (
    OBJECT_OT_barndoor_light,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.VIEW3D_MT_light_add.append(menu_item)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        bpy.types.VIEW3D_MT_light_add.remove(menu_item)

if __name__ == "__main__":
    register()
