"""
GREASE PENCIL: REFINE LINE
Version: 0.05
Author : Victor L. Caballero
"""
import bpy
import mathutils as mu
import numpy as np
from bpy.props import IntProperty, FloatProperty
"""
a = np.array([[1, 1, 1], [2, 2, 3]])
print (np.median(a, axis= 0))
"""

    
def gpr_set_point(stroke3, stroke):
    stroke3.co=stroke.co
    stroke3.strength=stroke.strength
    stroke3.pressure=stroke.pressure

def gpr_refine():
    print("--------------------iniciando")
    #DECLARANDO VARIABLES INICIALES
    gpr_workingDistance=0.1
    gpr_minDistance = gpr_workingDistance#Variara segun se vaya encontrando un nuevo vertice mas cercano
    gpr_in = 0 #Si se encuentra un punto de inicio este valor cambia
    gpr_out = 0 #Si se encuentra un punto de final este valor cambia
    gpr_cyclic = 4
    
    gpr_strk1_in = 0
    gpr_strk1_out = 0
    gpr_strk2_in = 0
    gpr_strk2_out = 0

    if bpy.context.mode == 'PAINT_GPENCIL':#PROVISORIO. Tal vez deberia ir al modal.
        
        strokes = bpy.context.object.data.layers.active.active_frame.strokes
        if strokes:
            
            if len(strokes) > 1:#Si tenemos mas de dos lineas
                
                stroke1 = strokes[-2]
                stroke1_len = len (stroke1.points)
                stroke2 = strokes[-1]
                stroke2_len = len (stroke2.points)             
                if stroke2_len > 1: #Si la nueva linea tiene el largo suficiente
                    point2=0
                    #BUSCANDO EL IN  -------------------------------------------            
                    for p2 in stroke2.points:#Comenzamos por la segunda linea
                        point1=0
                        if point2 < stroke2_len-2:
                            line2_in = stroke2.points[point2].co
                            line2_out = stroke2.points[point2+1].co             
                            for p1 in stroke1.points: #Seguimos por la primera linea                               
                                if point1 < stroke1_len-2:                                
                                    line1_in = stroke1.points[point1].co
                                    line1_out = stroke1.points[point1+1].co
                                    # HASTA NO ENCONTRAR UNA MEJOR MANERA DE MEDIR LA INTERSECCION DE DOS PORCIONES DE LINEA
                                    a = mu.geometry.intersect_line_line(line1_in, line1_out, line2_in, line2_out) #encuentra el punto mas cercano entre dos lineas
                                    if a:                                          
                                        dist1 = (line1_in-line1_out).length
                                        dist2 = (line2_out-line2_in).length
                                        d1 = (line1_in-a[0]).length
                                        d2 = (line1_out-a[0]).length
                                        d3 = (line2_in-a[0]).length
                                        d4 = (line2_out-a[0]).length                                        
                                        if all ([d1 < dist1, d2 < dist1,d3 < dist2, d4 < dist2]):
                                            #print("a: ", a)
                                            b = np.round(a, 5) #lo convertimos a un array numpy para poder redondear los decimales                                        
                                            if (b[0]==b[1]).all():#evualuamos si hay cruce de linea
                                                gpr_in = 1
                                                bpy.data.objects["X"].location = a[0]
                                                break
                                point1 += 1
                        if gpr_in == 1:
                            gpr_strk1_in=point1    
                            gpr_strk2_in=point2
                            gpr_vertexIn = a[0] #ESTE ES UN VECTOR QUE SE VA A GUARDAR PARA SERVIR DE UNION DE LINEAS
                            print ("gpr_strk1_in:",gpr_strk1_in)
                            print ("gpr_strk2_in:",gpr_strk2_in)
                            del a
                            break
                        
                        point2 += 1
                    
                    if gpr_in == 1:
                        print("BUSCANDO OUT")
                        point2=stroke2_len-1    
                        #BUSCANDO EL OUT  -------------------------------------------            
                        for p2 in reversed(stroke2.points):#Comenzamos por la segunda linea
                            point1=stroke1_len-1
                            if point2 > 0:
                                
                                line2_in = stroke2.points[point2].co
                                line2_out = stroke2.points[point2-1].co
                                           
                                for p1 in reversed(stroke1.points):
                                    if point1 > 0:
                                        line1_in = stroke1.points[point1].co
                                        line1_out = stroke1.points[point1-1].co
                                        # HASTA NO ENCONTRAR UNA MEJOR MANERA DE MEDIR LA INTERSECCION DE DOS PORCIONES DE LINEA
                                        a = mu.geometry.intersect_line_line(line1_in, line1_out, line2_in, line2_out) #encuentra el punto mas cercano entre dos lineas
                                        if a:
                                            dist1 = (line1_in-line1_out).length
                                            dist2 = (line2_in-line2_out).length
                                            d1 = (line1_in-a[0]).length
                                            d2 = (line1_out-a[0]).length
                                            d3 = (line2_in-a[0]).length
                                            d4 = (line2_out-a[0]).length 
                                            if all ([d1 < dist1, d2 < dist1,d3 < dist2, d4 < dist2]):
                                                b = np.round(a, 5) #lo convertimos a un array numpy para poder redondear los decimales
                                                if (b[0]==b[1]).all():#evualuamos si hay cruce de linea
                                                    gpr_out = 1                                                  
                                                    bpy.data.objects["X2"].location = a[0]
                                                    break
                                    point1 -= 1
                            if gpr_out == 1:
                                gpr_strk1_out=point1  
                                gpr_strk2_out=point2
                                gpr_vertexOut = a[0] #ESTE ES UN VECTOR QUE SE VA A GUARDAR PARA SERVIR DE UNION DE LINEAS
                                print ("gpr_strk1_out:",gpr_strk1_out)
                                print ("gpr_strk2_out:",gpr_strk2_out)
                                break
                            
                            point2 -= 1
                            
                    #   COMENZAMOS A PROCESAR LINEA   #------------------------------------------------
                    if gpr_strk1_in > gpr_strk1_out: #SI LA LINEA 2 ESTA INVERTIDA
                        print("invertiendo linea 1")
                        print ("in: ", gpr_strk1_in, "   out: ",gpr_strk1_out ," len: ", stroke1_len )                  
                        gpr_strk1_in = stroke1_len-gpr_strk1_in
                        gpr_strk1_out = stroke1_len-gpr_strk1_out
                        
                        bpy.ops.gpencil.editmode_toggle()
                        bpy.ops.gpencil.select_all(action='DESELECT')
                        bpy.context.object.data.layers.active.active_frame.strokes[-2].select = True
                        bpy.ops.gpencil.stroke_flip()
                        bpy.ops.gpencil.paintmode_toggle()
                        print (">in: ", gpr_strk1_in, "   out: ",gpr_strk1_out , " len: ", stroke1_len)
                    if gpr_strk2_in > gpr_strk2_out: #SI LA LINEA 2 ESTA INVERTIDA
                        print("invertiendo linea 1")
                        print ("in: ", gpr_strk2_in, "   out: ",gpr_strk2_out ," len: ", stroke1_len )                  
                        gpr_strk2_in = stroke2_len-gpr_strk2_in
                        gpr_strk2_out = stroke2_len-gpr_strk2_out
                        
                        bpy.ops.gpencil.editmode_toggle()
                        bpy.ops.gpencil.select_all(action='DESELECT')
                        bpy.context.object.data.layers.active.active_frame.strokes[-1].select = True
                        bpy.ops.gpencil.stroke_flip()
                        bpy.ops.gpencil.paintmode_toggle()
                        print (">in: ", gpr_strk2_in, "   out: ",gpr_strk2_out , " len: ", stroke2_len)
                    
                    if np.absolute(gpr_strk1_out-gpr_strk1_in) <= 2 :
                        print("PODRIA EXTENDERSE LA LINEA O NO")
                        gpr_out = 0
                
                    if gpr_in == 1 and gpr_out == 1:
                    
                        
                        
                        lyr = bpy.context.object.data.layers.active
                        stroke3= lyr.active_frame.strokes.new()
                        stroke3.display_mode = '3DSPACE'
                        stroke3.line_width = stroke1.line_width#Todo: Detectar el size del brush actual para asignar este valor
                        stroke3.material_index = stroke1.material_index   
                        
                        cyclic_in = stroke1_len/gpr_cyclic
                        cyclic_out = stroke1_len-stroke1_len/gpr_cyclic
                        print("cyclic_in", cyclic_in, "cyclic_out", cyclic_out)
                        print("stroke1_len",stroke1_len)
                        if gpr_strk1_in < cyclic_in and gpr_strk1_out > cyclic_out: # CIERRA LA LINEA         
                            print("CIERRA LA LINEA")
                            #creamos el largo final de la linea
                            #LINEA 1 DESDE IN A OUT, LINEA 2 DESDE IN A OUT
                            #Creamos una tercera linea para alojar el resultado
                            l1 = gpr_strk1_out-gpr_strk1_in-1
                            l2 = gpr_strk2_out-gpr_strk2_in-1                           
                            print ("l1:",l1 , "l2:",l2)
                            c =l1+1+l2+1                 
                            stroke3.points.add(count= c)
                            
                            #PRIMER SEGMENTO DE LINEA
                            n = 0
                            print (".")
                            for n in range(l1):
                                nn = n+gpr_strk1_in+1
                                gpr_set_point(stroke3.points[n], stroke1.points[nn]) 
                            #UNION DE LINEAS 
                            print ("..",n)                                      
                            stroke3.points[l1].co=gpr_vertexOut
                            stroke3.points[l1].strength=stroke1.points[nn].strength
                            stroke3.points[l1].pressure=stroke1.points[nn].pressure
                            #SEGUNDO SEGMENTO DE LINEA
                            print ("...",l1) 
                            for n in range (l2):
                                nn=n+l1+1
                                nn2= gpr_strk2_out-n-1
                                gpr_set_point(stroke3.points[nn], stroke2.points[nn2])
                            #UNION DE LINEAS
                            print ("....",nn)
                            print (".....",c)                                     
                            stroke3.points[c-1].co=gpr_vertexIn
                            stroke3.points[c-1].strength=stroke2.points[nn2].strength
                            stroke3.points[c-1].pressure=stroke2.points[nn2].pressure
                            stroke3.draw_cyclic = True
                                
                        else: #REEMPLAZA EL MEDIO DE LA LINEA
                            print("REEMPLAZA EL MEDIO DE LA LINEA")
                            #creamos el largo final de la linea
                            #LINEA 1 DESDE IN A OUT, LINEA 2 DESDE IN A OUT
                            #Creamos una tercera linea para alojar el resultado
                            l1 = gpr_strk1_in-1
                            l2 = gpr_strk2_out-gpr_strk2_in-1
                            l3 = stroke1_len-gpr_strk1_out                          
                            print ("l1:",l1 , "l2:",l2, "l3:",l3)
                            c =l1+1+l2+1+l3               
                            stroke3.points.add(count= c)
                            
                            #PRIMER SEGMENTO DE LINEA
                            n = 0
                            for n in range(l1):
                                gpr_set_point(stroke3.points[n], stroke1.points[n]) 
                            #UNION DE LINEAS 
                            
                            stroke3.points[l1].co=gpr_vertexIn
                            stroke3.points[l1].strength=stroke1.points[n].strength
                            stroke3.points[l1].pressure=stroke1.points[n].pressure
                            #SEGUNDO SEGMENTO DE LINEA
                            for n in range (l2):
                                nn=n+l1+1
                                nn2= gpr_strk2_in+n+1
                                gpr_set_point(stroke3.points[nn], stroke2.points[nn2])
                            #UNION DE LINEAS
                            
                            stroke3.points[l1+l2+1].co=gpr_vertexOut
                            stroke3.points[l1+l2+1].strength=stroke2.points[nn2].strength
                            stroke3.points[l1+l2+1].pressure=stroke2.points[nn2].pressure
                            #TERCER SEGMENTO DE LINEA
                            for n in range (l3):
                                nn=n+l1+l2+2
                                nn2= gpr_strk1_out+n
                                gpr_set_point(stroke3.points[nn], stroke1.points[nn2])
                            
                            if stroke1.draw_cyclic == True:
                                stroke3.draw_cyclic = True
                        #ELIMINAMOS LOS DOS STROKES ANTERIORES               
                        bpy.context.object.data.layers.active.active_frame.strokes.remove(stroke1)
                        bpy.context.object.data.layers.active.active_frame.strokes.remove(stroke2)
                        bpy.ops.ed.undo_push()
                                               
                        
                    elif gpr_in == 1:                        
                        
                        if gpr_strk1_in > stroke1_len/2: #REEMPLAZA EL INICIO DE LA LINEA         
                            print("AGREGA LINEA AL INICIO")
                            lyr = bpy.context.object.data.layers.active
                            stroke3= lyr.active_frame.strokes.new()
                            stroke3.display_mode = '3DSPACE'
                            stroke3.line_width = stroke1.line_width#Todo: Detectar el size del brush actual para asignar este valor
                            stroke3.material_index = stroke1.material_index                            
                            #creamos el largo final de la linea
                            #LINEA 1 DESDE IN A OUT, LINEA 2 DESDE IN A OUT
                            #Creamos una tercera linea para alojar el resultado
                            if stroke1.draw_cyclic == True:
                                l0 = stroke1_len                                
                                l1 = stroke2_len-gpr_strk2_out
                                c =l0+l1+1 
                                print ("l0:",l0 , "l1:",l1 ," total", c)              
                                stroke3.points.add(count= c)
                                for n in range(l0):
                                    nn = gpr_strk1_in - n
                                    print ("nn", nn)
                                    gpr_set_point(stroke3.points[n], stroke1.points[nn]) 
                                stroke3.points[l0].co=gpr_vertexOut
                                stroke3.points[l0].strength=stroke1.points[nn].strength
                                stroke3.points[l0].pressure=stroke1.points[nn].pressure
                                for n2 in range(l1):
                                    nn = l0+n2+1                               
                                    gpr_set_point(stroke3.points[nn], stroke2.points[gpr_strk2_out+n2]) 
                            else:
                                x = 0
                                l1 = gpr_strk1_in
                                l2 = stroke2_len-gpr_strk2_in-1                            
                                print ("l1:",l1 , "l2:",l2)                                
                                c =l1+1+l2               
                                stroke3.points.add(count= c)
                                #PRIMER SEGMENTO DE LINEA
                                print (".")
                                for n in range(l1):
                                    nn = n
                                    gpr_set_point(stroke3.points[nn], stroke1.points[n]) 
                                #UNION DE LINEAS 
                                print ("..",n)                                      
                                stroke3.points[l1+x].co=gpr_vertexOut
                                stroke3.points[l1+x].strength=stroke1.points[nn].strength
                                stroke3.points[l1+x].pressure=stroke1.points[nn].pressure
                                #SEGUNDO SEGMENTO DE LINEA
                                print ("...",l1) 
                                for n in range (l2):
                                    nn=n+l1+1
                                    nn2= gpr_strk2_in+n+1
                                    gpr_set_point(stroke3.points[nn], stroke2.points[nn2])
                            
                        else:#REEMPLAZA EL FINAL DE LA LINEA 
                            segment = 3                    
                            print("AGREGA LINEA AL FINAL")
                            lyr = bpy.context.object.data.layers.active
                            stroke3= lyr.active_frame.strokes.new()
                            stroke3.display_mode = '3DSPACE'
                            stroke3.line_width = stroke1.line_width#Todo: Detectar el size del brush actual para asignar este valor
                            stroke3.material_index = stroke1.material_index                            
                            #creamos el largo final de la linea
                            #LINEA 1 DESDE IN A OUT, LINEA 2 DESDE IN A OUT
                            #Creamos una tercera linea para alojar el resultado
                            if stroke1.draw_cyclic == True:
                                l0 = stroke1_len                                
                                l1 = stroke2_len-gpr_strk2_out
                                c =l0+l1+1 
                                print ("l0:",l0 , "l1:",l1 ," total", c)              
                                stroke3.points.add(count= c)
                                for n in range(l0):
                                    nn = gpr_strk1_in - n
                                    print ("nn", nn)
                                    gpr_set_point(stroke3.points[n], stroke1.points[nn]) 
                                stroke3.points[l0].co=gpr_vertexOut
                                stroke3.points[l0].strength=stroke1.points[nn].strength
                                stroke3.points[l0].pressure=stroke1.points[nn].pressure
                                for n2 in range(l1):
                                    nn = l0+n2+1                               
                                    gpr_set_point(stroke3.points[nn], stroke2.points[gpr_strk2_out+n2])  
                                
                            else:
                                x = 0
                                l1 = stroke1_len-gpr_strk1_in-1
                                l2 = stroke2_len-gpr_strk2_in-1                        
                                print ("l1:",l1 , "l2:",l2)                                
                                c =l1+1+l2               
                                stroke3.points.add(count= c)                            
                                #PRIMER SEGMENTO DE LINEA
                                print (".")
                                for n in range(l1):
                                    nn = n
                                    #nn2= gpr_strk2_in+n+1
                                    if stroke1.draw_cyclic == True:
                                        gpr_set_point(stroke3.points[nn], stroke1.points[nn-1]) 
                                    else:
                                        gpr_set_point(stroke3.points[nn], stroke1.points[stroke1_len-nn-1]) 
                                #UNION DE LINEAS 
                                print ("..",n)                                      
                                stroke3.points[l1].co=gpr_vertexOut
                                stroke3.points[l1].strength=stroke1.points[nn].strength
                                stroke3.points[l1].pressure=stroke1.points[nn].pressure
                                #SEGUNDO SEGMENTO DE LINEA
                                print ("...",l1) 
                                for n in range (l2):
                                    nn=n+l1+1
                                    nn2= gpr_strk2_in+n+1
                                    gpr_set_point(stroke3.points[nn], stroke2.points[nn2])
                        #ELIMINAMOS LOS DOS STROKES ANTERIORES               
                        bpy.context.object.data.layers.active.active_frame.strokes.remove(stroke1)
                        bpy.context.object.data.layers.active.active_frame.strokes.remove(stroke2)
                        bpy.ops.ed.undo_push()
                                 















class ModalGPR(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "gpencil.modal_operator"
    bl_label = "Refine Line"
    first_value = FloatProperty()

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' :
            
            self.lmb = event.value == 'RELEASE'
            #print (self.lmb)
            
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
    bpy.utils.register_class(ModalGPR)

def unregister():
    bpy.utils.unregister_class(ModalGPR)

if __name__ == "__main__":
    register()
