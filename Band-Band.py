
"""this scrpit generates three types of rectangular modules and a gird of points and it allows the user to pick on one of the module types. Then they can place it on the grid.
The process begins with selecting an start point then the second point to specify the shorter side of the module and finally the third point specify the longer side of the module
or the module direction.
there is a toggle button at one side of grid which changes between level-mode and delete-mode. it allows the user to change the level of modules between ground or first level
or when set on delete them, to delete one drawn module by clicking on it."""
#steps of generating module type-1: vertical rectangle(curve)from 3 points-->offset rectangle toward its center(curve)-->transform space between two rectangles into a surface-->extrude the surface in horizontal direction
#steps of generating module type-2:get 4 points-->draw a polyline using points(U-shape)-->make a surface by extudeing the polyline horizontally-->get surface normals and analyse them-->offset the surface vetically  
#steps of generating module type-3:same as type-2 
import rhinoscriptsyntax as rs

#Enabling Osnap and Ortho
if not rs.Ortho(): rs.Ortho(True)
if not rs.Osnap(): rs.Osnap(True)
#setting ducument unit tolerance to 0.01
rs.UnitAbsoluteTolerance( 0.01 )
#setting perspective view to "shaded" mode
rs.ViewDisplayMode('Perspective', 'Shaded')
#three variables to specify the  modules dimentions
Width=1.19
Length=5.95
Height=3.09
#this variable contains a code that changes the osnap mode 
mode=134217728
#this function allows the user to create a module type-1
def add_module1():
    rs.TextDotText(STATUS, text="Tap ouside the board to cancel selection")    
    #point1 is one of the lowest corner points of the module.
    Point1 = rs.GetPoint("Pick the first corner of rectangle")
    #changes osnap mode to zero-->snap doesn't detect anything so user is just allowed to pick a direction in otrho mode.
    rs.OsnapMode(0)
    #if the selected point is one of grid points user is allowed to select the second point of rectangle.
    #to check the point postion on the grid program calculates the remainder of point z-parameter divided by the grid unit which is 1.19.
    #this happens in other functions as well.
    if (Point1[0]*100)%119==0 or int((Point1[0]*100)%119)==118:
        rs.TextDotText(STATUS, text="Draw")
        #the user picks point two in a specific distance from first point
        Point2 = rs.GetPoint("Pick the second corner of rectangle", Point1,Length )
        #adds point3 using point1 coordinates. point3 is a upper corner of rectangle 
        Point3=(Point1[0],Point1[1],Height)
        #drawing a plane from 3 added points. 
        base_plane=rs.PlaneFromPoints(Point3,Point1,Point2) 
        #drawing a rectangle using the plane with specific width and height
        rect=rs.AddRectangle(base_plane, Height, Length)
        #calculates center of the rectangle
        offset_point=((Point2[0]+Point3[0])/2,(Point2[1]+Point3[1])/2,(Point2[2]+Point3[2])/2)
        if rs.IsCurve(rect):
            #adds a new renctangle by offseting rectangle toward its center
            rect2=rs.OffsetCurve( rect,offset_point, 0.23 )
        #adding a surface using 2 generated rectangles.    
        if rect and rect2:surf=rs.AddPlanarSrf([rect,rect2])
        #getting a point connected to rectanle corner.the line between two points shows extrude direction
        Point4 = rs.GetPoint("pick extrude direction", Point2,Width )
        #this boolean changes to true when user picks a proper point
        ex_condition=False
        #while point4 is not in a correct distance from point1 the code keeps asking the user to pick a correct point4
        while ex_condition==False:
            if rs.Distance(Point1,Point4)>=6.06 and rs.Distance(Point1,Point4)<=6.08:
                ex_condition=True
                #if the distance is correnct it draws a line using point2 and point4
                curve = rs.AddLine(Point2,Point4)
                #extrude surface using added line as direction. the result is the final object.
                result=rs.ExtrudeSurface(surf, curve)
                
            else:
                Point4 = rs.GetPoint("pick extrude direction", Point2,Width )
        #delete generated objects except result        
        rs.DeleteObject(curve)
        rs.DeleteObject(rect)
        rs.DeleteObject(rect2)
        rs.DeleteObject(surf)
        #return result which is final module
        return result
    else:
        #if the first point is not on grid function returns 0
        return 0
#this function creates a module type-1  to help user pick a module type 

def add_preview1(): 
    #add 3points as 3 corners of rectangle   
    point1 =(0,0,0)
    point2 =(0,Length,0)
    point3=(point1[0],point1[1],Height)
    #adds a plane based on 3points
    base_plane=rs.PlaneFromPoints(point3,point1 ,point2) 
    #draw a rectangle using 3points and added plane
    rect=rs.AddRectangle(base_plane, Height, Length)
    #calculate center of rectangle
    offset_point=((point2[0]+point3[0])/2,(point2[1]+point3[1])/2,(point2[2]+point3[2])/2)
    #draw a new rectangle by offseting first rectngle toward its center
    if rs.IsCurve(rect):
        rect2=rs.OffsetCurve( rect,offset_point, 0.23 ) 
    #add a surface between 2 rectangles    
    if rect and rect2:surf=rs.AddPlanarSrf([rect,rect2])
    #add point4 
    point4 = (Width,Length,0)
    #draw a line using point2 and point4 named curve
    curve = rs.AddLine(point2,point4)
    #extrude surface using curve as a direction.result is a module type-1
    result=rs.ExtrudeSurface(surf, curve)  
    #delete all generated objects except result
    rs.DeleteObject(curve)
    rs.DeleteObject(rect)
    rs.DeleteObject(rect2)
    rs.DeleteObject(surf)
    #next three lines move the created module to a position next to other modules.
    translation =(-5,0,0)
    r=rs.MoveObject(result, translation)
    rs.AddTextDot("1",(-5,0,4))
    #returning created module
    return r

#this function allows user to create a module type-2    
def add_module2():
    #change status 
    rs.TextDotText(STATUS, text="Tap ouside the board to cancel selection")
    #the user picks the first point
    Point1 = rs.GetPoint("Pick the first corner of rectangle")
    #change osnap to 0 so it doesn't detect any type of object
    rs.OsnapMode(0)
    #if point1 is one of grid points user can pick second point
    if (Point1[0]*100)%119==0 or int((Point1[0]*100)%119)==118:
        #when first point is correct user sees 'draw' in status bar
        rs.TextDotText(STATUS, text="Draw")
        #the user picks the second point
        Point2 = rs.GetPoint("Pick the second corner of rectangle", Point1,Length )
        #adding point3 and point5 using point1 and point2 
        Point3=(Point1[0],Point1[1],Height)
        Point5=(Point2[0],Point2[1],Height)
        #drawing a polyline using four points
        rect=rs.AddPolyline([Point1,Point3,Point5,Point2], replace_id=None)
        #user pick point4 
        Point4 = rs.GetPoint("pick extrude direction", Point2,Width )
        #this boolean changes to true if the user picks point correctly
        ex_condition=False
        #asking the user to pick point4 until the picked point is in a correct distance from point1
        while ex_condition==False:
            #if the  point is correctly picked, the code draws a line between point1 and point2
            if rs.Distance(Point1,Point4)>=6.06 and rs.Distance(Point1,Point4)<=6.08:
                ex_condition=True
                curve = rs.AddLine(Point2,Point4)
                #extruding the rectangle using a direction made out of the two points
                psrf=rs.ExtrudeCurve(rect, curve)       
            else:
                Point4 = rs.GetPoint("pick extrude direction", Point2,Width )
        #calculating center point of the recntagle        
        center_point=((Point2[0]+Point3[0])/2,(Point2[1]+Point3[1])/2,(Point2[2]+Point3[2])/2)
        #exploding extruded surface to three surfaces and save them in a list
        srf_list=rs.ExplodePolysurfaces( psrf )
        #finding the horizontal surface and save its normal vector z parameter in normal_control variable
        for i in srf_list:
            points =rs.SurfacePoints(i, return_all=True)
            normal = rs.SurfaceNormal(i, points[0])
            if normal[2]==1 or normal[2]==-1:
                normal_control=normal[2]
                break
       #in the next two for loops: if normel vector z parameter is positive or negative, saved surfaces will extrude toward oposite direction
        psrf_list=[]
        if normal_control==1:
            for i in srf_list:
                psrf_list.append(rs.OffsetSurface( i,-0.23, tolerance=None, both_sides=False, create_solid=True))
        if normal_control==-1:
            for i in srf_list:
                psrf_list.append(rs.OffsetSurface( i,0.23, tolerance=None, both_sides=False, create_solid=True))        
        #join extruded surfaces together.result is final object    
        result=rs.BooleanUnion(psrf_list, delete_input=True)
        #deleting generated objects except the result
        rs.DeleteObject(psrf)
        rs.DeleteObject(curve)
        rs.DeleteObject(rect)
        rs.DeleteObjects(srf_list)
    #return final object
        return result
    else:
        #if the first picked point is not correct function returns 0
        return 0
#this function creates a module type-2  to help user pick a module type
############################## for now till here
def add_preview2():
    #add 2 point as 2 corners of rectangle
    Point1 =(0,0,0)
    Point2 =(0,Length,0)
    #add point3 and point 5 based on point1 and point2 positions
    Point3=(Point1[0],Point1[1],Height)
    Point5=(Point2[0],Point2[1],Height)
    #draw a polyline using four points
    rect=rs.AddPolyline([Point1,Point3,Point5,Point2], replace_id=None)
    #add point 4
    Point4 = (Width,Length,0)
    #draw a line using point2 and point4
    curve = rs.AddLine(Point2,Point4)
    #extrude polyline using added line as direction
    psrf=rs.ExtrudeCurve(rect, curve)       
    #expolde extruded surface to sub surfaces and save them in a list
    srf_list=rs.ExplodePolysurfaces( psrf )
    #find the horizontal surface and save its normal vector z parameter in normal_control variable
    for i in srf_list:
        points =rs.SurfacePoints(i, return_all=True)
        normal = rs.SurfaceNormal(i, points[0])
        if normal[2]==1 or normal[2]==-1:
            normal_control=normal[2]
            break
   #in next two for loops: if normel vector zparameter is positive or negative saved surfaces will extrude toward oposite direction
    psrf_list=[]
    if normal_control==1:
        for i in srf_list:
            psrf_list.append(rs.OffsetSurface( i,-0.23, tolerance=None, both_sides=False, create_solid=True))
    if normal_control==-1:
        for i in srf_list:
            psrf_list.append(rs.OffsetSurface( i,0.23, tolerance=None, both_sides=False, create_solid=True))        
   #join extruded surfaces together. result is the final object     
    result=rs.BooleanUnion(psrf_list, delete_input=True)
    #delete generated objects except the result
    rs.DeleteObject(psrf)
    rs.DeleteObject(curve)
    rs.DeleteObject(rect)
    rs.DeleteObjects(srf_list)
    #next three lines move the created module to a position next to other modules.
    translation =(-5,10,0)
    r=rs.MoveObject(result, translation)
    rs.AddTextDot("2",(-5,10,4))

    return r
#this function allows user to create a module type-3 
#similar to add_module2   
def add_module3():
    rs.TextDotText(STATUS, text="Tap ouside the board to cancel selection")
    Point1 = rs.GetPoint("Pick the first corner of rectangle")
    rs.OsnapMode(0)
    if (Point1[0]*100)%119==0 or int((Point1[0]*100)%119)==118:
        rs.TextDotText(STATUS, text="Draw")
        Point2 = rs.GetPoint("Pick the second corner of rectangle", Point1,Length )
    
        Point3=(Point1[0],Point1[1],Height)
        Point5=(Point2[0],Point2[1],Height)
        rect=rs.AddPolyline([Point3,Point1,Point2,Point5], replace_id=None)
        Point4 = rs.GetPoint("pick extrude direction", Point2,Width )
        ex_condition=False
        while ex_condition==False:
            if rs.Distance(Point1,Point4)>=6.06 and rs.Distance(Point1,Point4)<=6.08:
                ex_condition=True
                curve = rs.AddLine(Point2,Point4)
                psrf=rs.ExtrudeCurve(rect, curve)       
            else:
                Point4 = rs.GetPoint("pick extrude direction", Point2,Width )
                
        center_point=((Point2[0]+Point3[0])/2,(Point2[1]+Point3[1])/2,(Point2[2]+Point3[2])/2)
        srf_list=rs.ExplodePolysurfaces( psrf )
        for i in srf_list:
            points =rs.SurfacePoints(i, return_all=True)
            normal = rs.SurfaceNormal(i, points[0])
            if normal[2]==1 or normal[2]==-1:
                normal_control=normal[2]
                break
       
        psrf_list=[]
        if normal_control==1:
            for i in srf_list:
                psrf_list.append(rs.OffsetSurface( i,0.23, tolerance=None, both_sides=False, create_solid=True))
        if normal_control==-1:
            for i in srf_list:
                psrf_list.append(rs.OffsetSurface( i,-0.23, tolerance=None, both_sides=False, create_solid=True))        
            
        result=rs.BooleanUnion(psrf_list, delete_input=True)
       
        rs.DeleteObject(psrf)
        rs.DeleteObject(curve)
        rs.DeleteObject(rect)
        rs.DeleteObjects(srf_list)
    
        return result
    else:
        return 0        
#this function creates a module type-3s to help user pick a module type
#similar to add_preview2        
def add_preview3():
    Point1 =(0,0,0)
    Point2 =(0,Length,0)
    Point3=(Point1[0],Point1[1],Height)
    Point5=(Point2[0],Point2[1],Height)
    rect=rs.AddPolyline([Point3,Point1,Point2,Point5], replace_id=None)
    Point4 = (Width,Length,0)
    curve = rs.AddLine(Point2,Point4)
    psrf=rs.ExtrudeCurve(rect, curve)       

    srf_list=rs.ExplodePolysurfaces( psrf )
    for i in srf_list:
        points =rs.SurfacePoints(i, return_all=True)
        normal = rs.SurfaceNormal(i, points[0])
        if normal[2]==1 or normal[2]==-1:
            normal_control=normal[2]
            break
   
    psrf_list=[]
    if normal_control==1:
        for i in srf_list:
            psrf_list.append(rs.OffsetSurface( i,0.23, tolerance=None, both_sides=False, create_solid=True))
    if normal_control==-1:
        for i in srf_list:
            psrf_list.append(rs.OffsetSurface( i,-0.23, tolerance=None, both_sides=False, create_solid=True))        
        
    result=rs.BooleanUnion(psrf_list, delete_input=True)            
    rs.DeleteObject(psrf)
    rs.DeleteObject(curve)
    rs.DeleteObject(rect)
    rs.DeleteObjects(srf_list)
    
    translation =(-5,20,0)
    r=rs.MoveObject(result, translation)
    rs.AddTextDot("3",(-5,20,4))
    

    return r          
 
#change layer to default 
rs.CurrentLayer("Default")
#generates a grid of points  
for i in range(0,23):
    for j in range(0,23):
        grid=rs.AddPoint(j*Width,i*Width,0)

#adds a text dot to show status 
STATUS=rs.AddTextDot("Select a Module",(0,10,10))        


#add three modules for user to pick from  
sample1=add_preview1()
sample2=add_preview2()
sample3=add_preview3()
#add a cylinder as a button named mode_switch
mode_switch=rs.AddCylinder( (0,30,0), 1, 1 )
#this boolean changes between level-mode and delete-mode
B_mode=False
#change layer to change color of button
rs.ObjectLayer(mode_switch, "Layer 01")
#add a text dot to button that shows the current mode
text=rs.AddTextDot("Delete Mode",(0,30,3))



  
while True:
    #changes layer so user add modules in a different layer 
    rs.CurrentLayer("Layer 01")
    #changes snap to a mode that user can pick points and is not allowed to select other objects.
    rs.OsnapMode(mode)
    #this command asks user to select an object which should be on of three sample modules or one of user added modules.
    selection=rs.GetObjectEx(message=None, filter=16, preselect=False, select=True,objects=None)
    #if user selects one of three sample modules he can draw one of selected type.(next 6lines)
    if selection[0]==sample1:
        current_block=add_module1()
        rs.TextDotText(STATUS, text="Select a module")
    elif selection[0]==sample2:
        current_block=add_module2()
        rs.TextDotText(STATUS, text="Select a module")
    elif selection[0]==sample3:
        current_block=add_module3()
        rs.TextDotText(STATUS, text="Select a module")
        
    #with every click on mode_switch it changes between level-mode and delete-mode and button layar changes to change button color.    
    elif selection[0]==mode_switch:
        if B_mode==True:
            B_mode=False
            rs.ObjectLayer(mode_switch, "Layer 01")
            rs.CurrentLayer("Default")
            if text:
                rs.DeleteObject(text)    
            text=rs.AddTextDot("Delete Mode",(0,30,3))
        elif B_mode==False:
            B_mode=True
            rs.ObjectLayer(mode_switch, "Layer 04")
            rs.CurrentLayer("Default")
            if text:
                rs.DeleteObject(text)
            text=rs.AddTextDot("Level Mode",(0,30,3))
            

   #if user selects one of added modules it will be deleted or move up or down depends on mode-switch    
    else:
        if B_mode ==True:
            #gets selected module corner points and saves them in a list
            box_points=rs.BoundingBox(selection[0], view_or_plane=None, in_world_coords=False)
            #if botton first point of module has a height near 3 it will move a level down
            if box_points[0][2] <4 and box_points[0][2] >3:
                translation =(0,0,-1*Height)
                #move module on level upward.
                rs.MoveObject(selection[0], translation)
            #if the lowest point of module has a height near 0 it will move a level up
            if box_points[0][2] <0.5 and box_points[0][2] >-0.5:
                #move module on level up.
                translation =(0,0,Height)
                rs.MoveObject(selection[0], translation)
       #if mode-switch is false the selected module will be deleted         
        elif B_mode ==False:
            rs.DeleteObject(selection[0])
              
            
     
