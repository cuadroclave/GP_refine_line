import bpy
import mathutils
from bpy.props import IntProperty, FloatProperty
"""Sepan disculpar lo sucio de este codigo"""
print ("")

def gpr_refine():
    gpr_working_distance = 0.05    
    gpr_vertexIn = 0
    gpr_vertexOut = 3
    gpr_actual_distance = gpr_working_distance
    gpr_strk1_in=0
    gpr_strk1_out=0
    gpr_strk2_in=0
    gpr_strk2_out=0

    """Detectar si tenemos seleccionado un GP OK"""
    """Detectar si estamos en Modo dibujo OK"""
    if bpy.context.mode == 'PAINT_GPENCIL':       
        """Mejorar el punto de recuperación para Ctrl Z"""
        """Guardar el stroke placement actual"""
        lyr = bpy.context.object.data.layers.active
        if lyr.active_frame.strokes:
            bpy.ops.ed.flush_edits(-1)
            if len(lyr.active_frame.strokes)>1 :
                stroke1 = lyr.active_frame.strokes[-2]
                stroke2 = lyr.active_frame.strokes[-1]                 
                #1-------------------------------------------------------------         
                #BUSCAMOS EL PRIMER PUNTO DE CORTE                
                gpr_actual_distance = gpr_working_distance
                print ("INICIAMOS")
                if gpr_vertexIn == 0:
                    print ("IN") 
                    n1 = 0                      
                    n2 = 0         
                    for point2 in stroke2.points:                            
                        nn = 0
                        In = 0
                        for point1 in stroke1.points:  
                            if nn < len(stroke1.points)-2 :                                                                                   
                                gpr_working_distance = (point1.co - stroke1.points[nn+1].co).length
                                #print ("IN  gpr_working_distance: ", gpr_working_distance)                         
                                                   
                            #print ("parabola", nn, ": ", p)                                           
                            distance = (point2.co - point1.co).length
                            if distance < gpr_working_distance:
                                print(nn)
                                if distance < gpr_actual_distance:
                                    n1=nn
                                    gpr_vertexIn = 1
                                    gpr_actual_distance=distance
                                    In = 1
                                elif In == 1:                               
                                    break
                            nn += 1 
                        #print (gpr_vertexIn,"n1:", n1, " n2: ", n2)
                        if gpr_vertexIn == 1:                     
                            """guardamos el vertice inicial del stroke 1 y stroke 2"""
                            print(n1," ", n2)                          
                            gpr_strk1_in=n1
                            gpr_strk2_in=n2
                            gpr_vertexOut = 0
                            gpr_vertexIn = 2 
                        elif gpr_vertexIn == 2:
                            break 
                        n2 += 1    
                            
                #BUSCAMOS EL SEGUNDO PUNTO DE CORTE-reseteamos gpr_actual_distance
                gpr_actual_distance = gpr_working_distance  
                
                if gpr_vertexOut == 0:
                    print ("OUT")
                    n1 = 0
                    n2 = 0         
                    for point2 in reversed(stroke2.points):
                        nn = 0
                        In = 0
                        for point1 in reversed(stroke1.points):
                            if nn < len(stroke1.points):                                                                                         
                                gpr_working_distance = (point1.co - stroke1.points[len(stroke1.points)-nn-2].co).length
                            distance = (point2.co - point1.co).length
                            if distance < gpr_working_distance:
                                if distance < gpr_actual_distance:
                                    n1=nn
                                    gpr_vertexOut = 1
                                    gpr_actual_distance=distance
                                    In = 1
                                elif In == 1:                                        
                                    break
                            nn+=1 
                        #print (gpr_vertexOut,"n1:", n1, " n2: ", n2)
                        if gpr_vertexOut == 1:
                            """guardamos el vertice inicial del stroke 1 y stroke 2"""
                            gpr_strk1_out=len(stroke1.points)-n1
                            gpr_strk2_out=len(stroke2.points)-n2
                            gpr_vertexOut = 2 
                            
                        elif gpr_vertexOut == 2:
                            break                                             
                        n2 += 1
                
            # REFINA O REEMPLAZA . todo eso no va acá
            e = gpr_strk2_in-gpr_strk2_out 
            print ("gpr_vertexOut: ", gpr_vertexOut)
            if e > -2 and e < 2 : #REEMPLAZA AL INICIO O AL FINAL
                if gpr_vertexOut!=3:               
                    if gpr_strk1_in <  len(stroke1.points)/2:          
                        gpr_vertexIn = 1
                        print("AGREGA LINEA AL INICIO", gpr_vertexOut )
                    else:                    
                        print("AGREGA LINEA AL FINAL")
                gpr_vertexOut = 0 
            else:#REFINA
                print("REFINA LINEA")
               
                
                                    
            if gpr_vertexIn == 2 and gpr_vertexOut == 2 :
                bpy.ops.ed.flush_edits()
                             
                print(".......1")
                print("linea1: ", gpr_strk1_in, " ", gpr_strk1_out, " >", len(stroke1.points))
                print("linea2: ", gpr_strk2_in, " ", gpr_strk2_out ," >", len(stroke2.points))
                print(".......")
                
                if gpr_strk1_in > gpr_strk1_out:
                    print("linea 1 invertida")
                    print ("in: ", gpr_strk1_in, "   out: ",gpr_strk1_out ," len: ", len(stroke1.points) )                  
                    gpr_strk1_in = len(stroke1.points)-gpr_strk1_in
                    gpr_strk1_out = len(stroke1.points)-gpr_strk1_out
                    
                    #bpy.context.mode = 'EDIT'
                    bpy.ops.gpencil.editmode_toggle()
                    bpy.ops.gpencil.select_all(action='DESELECT')
                    bpy.context.object.data.layers.active.active_frame.strokes[-2].select = True
                    bpy.ops.gpencil.stroke_flip()
                    bpy.ops.gpencil.paintmode_toggle()
                    print (">in: ", gpr_strk1_in, "   out: ",gpr_strk1_out , " len: ", len(stroke1.points)) 
                if gpr_strk2_in > gpr_strk2_out:
                    print("linea 2 invertida")
                    print ("in: ", gpr_strk2_in, "   out: ",gpr_strk2_out ," len: ", len(stroke2.points) )                  
                    
                    gpr_strk2_in = len(stroke2.points)-gpr_strk2_in
                    gpr_strk2_out = len(stroke2.points)-gpr_strk2_out
                    
                    #bpy.context.mode = 'EDIT'
                    bpy.ops.gpencil.editmode_toggle()
                    bpy.ops.gpencil.select_all(action='DESELECT')
                    bpy.context.object.data.layers.active.active_frame.strokes[-1].select = True
                    bpy.ops.gpencil.stroke_flip()
                    bpy.ops.gpencil.paintmode_toggle()
                    print (">in: ", gpr_strk2_in, "   out: ",gpr_strk2_out , " len: ", len(stroke2.points)) 
                    
                lyr = bpy.context.object.data.layers.active
                stroke3= lyr.active_frame.strokes.new()
                stroke3.display_mode = '3DSPACE'
                stroke3.line_width = stroke1.line_width#Todo: Detectar el size del brush actual para asignar este valor
                stroke3.material_index = stroke1.material_index#Todo: Detectar Usar el material que usa el anteultima stroke
                #creamos el largo final de la linea
                c = gpr_strk1_in+(gpr_strk2_out-gpr_strk2_in)+(len(stroke1.points)-gpr_strk1_out)
                stroke3.points.add(count= c)
                print ("1MODIFICANDO LINEA de 1 a 2")
                for n in range(gpr_strk1_in):
                    stroke3.points[n].co=stroke1.points[n].co
                    stroke3.points[n].strength=1
                    stroke3.points[n].pressure=stroke1.points[n].pressure
                for n in range (gpr_strk2_out-gpr_strk2_in):
                    nn=n+gpr_strk1_in
                    nn2= n +gpr_strk2_in
                    #print(stroke2.points[nn2].co)
                    stroke3.points[nn].co=stroke2.points[nn2].co
                    stroke3.points[nn].strength=1
                    stroke3.points[nn].pressure=stroke2.points[nn2].pressure
                for n in range(len(stroke1.points)-gpr_strk1_out):
                    nn = n+gpr_strk1_in+(gpr_strk2_out-gpr_strk2_in)
                    nn2 = n+gpr_strk1_out
                    stroke3.points[nn].co=stroke1.points[nn2].co
                    stroke3.points[nn].strength=1
                    stroke3.points[nn].pressure=stroke1.points[nn2].pressure   
                """  
                ELIMINAR LOS DOS STROKES ANTERIORES
                """
                
                bpy.context.object.data.layers.active.active_frame.strokes.remove(stroke1)
                bpy.context.object.data.layers.active.active_frame.strokes.remove(stroke2)
                bpy.ops.ed.undo_push()
                
                 
                #stroke2.remove()
        
            elif gpr_vertexIn == 2:
                print(".......2")
                print("linea1: ", gpr_strk1_in, " ", gpr_strk1_out, " >", len(stroke1.points))
                print("linea2: ", gpr_strk2_in, " ", gpr_strk2_out ," >", len(stroke2.points))
                print(".......")
                """if gpr_strk1_in > gpr_strk1_out:
                    print("linea 1 invertida")
                    print ("in: ", gpr_strk1_in, "   out: ",gpr_strk1_out ," len: ", len(stroke1.points) )                  
                    gpr_strk1_in = len(stroke1.points)-gpr_strk1_in
                    gpr_strk1_out = len(stroke1.points)-gpr_strk1_out
                    
                    #bpy.context.mode = 'EDIT'
                    bpy.ops.gpencil.editmode_toggle()
                    bpy.ops.gpencil.select_all(action='DESELECT')
                    bpy.context.object.data.layers.active.active_frame.strokes[-2].select = True
                    bpy.ops.gpencil.stroke_flip()
                    bpy.ops.gpencil.paintmode_toggle()
                    print (">in: ", gpr_strk1_in, "   out: ",gpr_strk1_out , " len: ", len(stroke1.points)) 
                if gpr_strk2_in > gpr_strk2_out:
                    print("linea 2 invertida")
                    print ("in: ", gpr_strk2_in, "   out: ",gpr_strk2_out ," len: ", len(stroke2.points) )                  
                    
                    gpr_strk2_in = len(stroke2.points)-gpr_strk2_in
                    gpr_strk2_out = len(stroke2.points)-gpr_strk2_out
                    
                    #bpy.context.mode = 'EDIT'
                    bpy.ops.gpencil.editmode_toggle()
                    bpy.ops.gpencil.select_all(action='DESELECT')
                    bpy.context.object.data.layers.active.active_frame.strokes[-1].select = True
                    bpy.ops.gpencil.stroke_flip()
                    bpy.ops.gpencil.paintmode_toggle()
                    print (">in: ", gpr_strk2_in, "   out: ",gpr_strk2_out , " len: ", len(stroke2.points))""" 
                
                lyr = bpy.context.object.data.layers.active
                stroke3= lyr.active_frame.strokes.new()
                stroke3.display_mode = '3DSPACE'
                stroke3.line_width = stroke1.line_width#Todo: Detectar el size del brush actual para asignar este valor
                stroke3.material_index = stroke1.material_index#Todo: Detectar Usar el material que usa el anteultima stroke
                #creamos el largo final de la linea
                c = gpr_strk1_in+(len(stroke2.points)-gpr_strk2_in)
                stroke3.points.add(count= c)
                print ("2CORTANDO LINEA Y REDIRECCIONANDO")
                for n in range(gpr_strk1_in):
                    stroke3.points[n].co=stroke1.points[n].co
                    stroke3.points[n].strength=1
                    stroke3.points[n].pressure=stroke1.points[n].pressure
                for n in range (len(stroke2.points)-gpr_strk2_in):
                    nn=n+gpr_strk1_in
                    nn2= n +gpr_strk2_in
                    #print(stroke2.points[nn2].co)
                    stroke3.points[nn].co=stroke2.points[nn2].co
                    stroke3.points[nn].strength=1
                    stroke3.points[nn].pressure=stroke2.points[nn2].pressure                   
                """  
                ELIMINAR LOS DOS STROKES ANTERIORES
                """ 
                         
                bpy.context.object.data.layers.active.active_frame.strokes.remove(stroke1)
                bpy.context.object.data.layers.active.active_frame.strokes.remove(stroke2)
                bpy.ops.ed.undo_push() 
                #stroke2.remove()
            elif gpr_vertexIn == 1:
                print(".......3")
                print("linea1: ", gpr_strk1_in, " ", gpr_strk1_out, " >", len(stroke1.points))
                print("linea2: ", gpr_strk2_in, " ", gpr_strk2_out ," >", len(stroke2.points))
                print(".......")
                """if gpr_strk1_in > gpr_strk1_out:
                    print("linea 1 invertida")
                    print ("in: ", gpr_strk1_in, "   out: ",gpr_strk1_out ," len: ", len(stroke1.points) )                  
                    gpr_strk1_in = len(stroke1.points)-gpr_strk1_in
                    gpr_strk1_out = len(stroke1.points)-gpr_strk1_out
                    
                    #bpy.context.mode = 'EDIT'
                    bpy.ops.gpencil.editmode_toggle()
                    bpy.ops.gpencil.select_all(action='DESELECT')
                    bpy.context.object.data.layers.active.active_frame.strokes[-2].select = True
                    bpy.ops.gpencil.stroke_flip()
                    bpy.ops.gpencil.paintmode_toggle()
                    print (">in: ", gpr_strk1_in, "   out: ",gpr_strk1_out , " len: ", len(stroke1.points)) """
                if gpr_strk2_in > gpr_strk2_out:
                    print("linea 2 invertida")
                    print ("in: ", gpr_strk2_in, "   out: ",gpr_strk2_out ," len: ", len(stroke2.points) )                  
                    
                    gpr_strk2_in = len(stroke2.points)-gpr_strk2_in
                    gpr_strk2_out = len(stroke2.points)-gpr_strk2_out
                    
                    #bpy.context.mode = 'EDIT'
                    bpy.ops.gpencil.editmode_toggle()
                    bpy.ops.gpencil.select_all(action='DESELECT')
                    bpy.context.object.data.layers.active.active_frame.strokes[-1].select = True
                    bpy.ops.gpencil.stroke_flip()
                    bpy.ops.gpencil.paintmode_toggle()
                    print (">in: ", gpr_strk2_in, "   out: ",gpr_strk2_out , " len: ", len(stroke2.points)) 
                
                lyr = bpy.context.object.data.layers.active
                stroke3= lyr.active_frame.strokes.new()
                stroke3.display_mode = '3DSPACE'
                stroke3.line_width = stroke1.line_width#Todo: Detectar el size del brush actual para asignar este valor
                stroke3.material_index = stroke1.material_index#Todo: Detectar Usar el material que usa el anteultima stroke
                #creamos el largo final de la linea
                c = (len(stroke2.points)-gpr_strk2_in)+(len(stroke1.points)-gpr_strk1_in)
                stroke3.points.add(count= c)
                print ("3CORTANDO LINEA Y REDIRECCIONANDO de 2 a 1") 
                print("len(stroke2.points): ",len(stroke2.points), "(gpr_strk2_in):", (gpr_strk2_in))              
                for n in range(len(stroke2.points)-(gpr_strk2_in)):
                                 
                    nn2= len(stroke2.points) - n -1           
                    stroke3.points[n].co=stroke2.points[nn2].co
                    stroke3.points[n].strength=1
                    stroke3.points[n].pressure=stroke2.points[nn2].pressure
                for n in range (len(stroke1.points)-(gpr_strk1_in)):
                    nn=n+len(stroke2.points)-(gpr_strk2_in)
                    nn2= n +gpr_strk1_in
                    #print(stroke2.points[nn2].co)
                    stroke3.points[nn].co=stroke1.points[nn2].co
                    stroke3.points[nn].strength=1
                    stroke3.points[nn].pressure=stroke1.points[nn2].pressure                   
                """  
                ELIMINAR LOS DOS STROKES ANTERIORES
                """ 
                         
                bpy.context.object.data.layers.active.active_frame.strokes.remove(stroke1)
                bpy.context.object.data.layers.active.active_frame.strokes.remove(stroke2)
                bpy.ops.ed.undo_push() 
                #stroke2.remove()
            else:
                print("no se creara ninguna linea")




class ModalOperator(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "gpencil.modal_operator"
    bl_label = "Refine Line"

    first_value = FloatProperty()

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' :
            
            self.lmb = event.value == 'RELEASE'
            #print (self.lmb)
            
            """
            if event.type == 'LEFTMOUSE' :
                # we could handle PRESS and RELEASE individually if necessary
                self.lmb = event.value == 'RELEASE'
                print ("dibujando")
            if event.type == 'LEFTMOUSE' and value == 'RELEASE':
                print ("dejo de dibujar")
            """
        elif self.lmb == False:
            gpr_refine() 
            print ("listo!")
            print ("")
            self.lmb = True
        if event.type in {'MIDDLEMOUSE','SPACEBAR', 'ESC'}:
            print ("DESACTIVADO")  
            print ("")   
            print ("")        
            return {'CANCELLED'}
            #return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        # variable to remember left mouse button state    
        self.lmb = True

        if context.object:


            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalOperator)


def unregister():
    bpy.utils.unregister_class(ModalOperator)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.modal_operator('INVOKE_DEFAULT')  
