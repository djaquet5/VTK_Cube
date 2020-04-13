"""
Lab: 2-Cube
Authors: David Jaquet
Description: Create a cube

Note: - Use the vtk example as inspiration
        https://vtk.org/Wiki/VTK/Examples/Python/DataManipulation/Cube.py

Python version: 3.7.4
"""
import vtk


# src: https://programtalk.com/python-examples/director.vtk.vtkPolyDataWriter/
def save_in_file(filename, data):
    """Create a file with the name "filename" and write "data" inside"""
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(data)
    writer.Write()


def connect_square():
    """Creates the faces of a cube by connecting its vertices with squares"""
    polys = vtk.vtkCellArray()

    # The vertices have to be in the clockwise
    faces = [
        (0, 1, 5, 4),   # Below face
        (0, 4, 6, 2),   # Behind face
        (2, 3, 1, 0),   # Left face
        (1, 3, 7, 5),   # Front face
        (4, 5, 7, 6),   # Right face
        (3, 2, 6, 7)    # Top face
    ]

    for face in faces:
        polys.InsertNextCell(4, face)

    return polys


def connect_triangles():
    """Creates the faces of a cube by connecting its vertices with triangles"""
    polys = vtk.vtkCellArray()

    half_faces = [
        (0, 1, 5),  # Below
        (0, 5, 4),
        (0, 4, 6),  # Behind
        (2, 0, 6),
        (0, 2, 3),  # Left
        (0, 3, 1),
        (1, 7, 5),  # Front
        (1, 3, 7),
        (4, 5, 7),  # Right
        (4, 7, 6),
        (3, 2, 7),  # Top
        (2, 6, 7)
    ]

    for face in half_faces:
        polys.InsertNextCell(3, face)

    return polys


def connect_triangles_strip():
    """Creates the faces of a cube by connecting its vertices with a triangles strip"""
    polys = vtk.vtkCellArray()

    # src: https://stackoverflow.com/questions/28375338/cube-using-single-gl-triangle-strip
    strip = [3, 7, 1, 5, 4, 7, 6, 3, 2, 1, 0, 4, 2, 6]

    polys.InsertNextCell(len(strip))

    for vertex in strip:
        polys.InsertCellPoint(vertex)

    return polys


if __name__ == '__main__':
    # Generate the vertices of the cube
    # [X,       Y,      Z]      = vertex number
    # [-0.5,    -0.5,   -0.5]   = 0
    # [-0.5,    -0.5,   0.5]    = 1
    # [-0.5,    0.5,    -0.5]   = 2
    # [-0.5,    0.5,    0.5]    = 3
    # [0.5,     -0.5,   -0.5]   = 4
    # [0.5,     -0.5,   0.5]    = 5
    # [0.5,     0.5,    -0.5]   = 6
    # [0.5,     0.5,    0.5]    = 7
    points = vtk.vtkPoints()
    noVertex = 0
    cube_range = [-0.5, 0.5]
    for i in cube_range:
        for j in cube_range:
            for k in cube_range:
                points.InsertPoint(noVertex, (i, j, k))
                noVertex += 1

    scalars = vtk.vtkFloatArray()
    for i in range(8):
        scalars.InsertTuple1(i, i)

    cube = vtk.vtkPolyData()
    cube.SetPoints(points)
    cube.GetPointData().SetScalars(scalars)

    # FIXME: To test the creation with different topology, uncomment the line to be tested
    # FIXME: Be aware to comment the SetPolys method and uncomment SetStrips if you use connect_triangles_strip
    polys = connect_square()
    # polys = connect_triangles()
    cube.SetPolys(polys)
    # polys = connect_triangles_strip()
    # cube.SetStrips(polys)

    # The file cube.vtk was generated with the squares in the cell array
    # The file cube_triangles.vtk was generated with the triangles in the cell array
    # The file cube_triangles_strip.vtk was generated with the triangles in the cell array
    save_in_file('cube.vtk', cube)

    reader = vtk.vtkPolyDataReader()
    reader.SetFileName('cube.vtk')

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    mapper.SetScalarRange(0, 5)

    # Create actor, render, interactor...
    # The code is from Cone5.py given for this lab
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # actor.GetProperty().FrontfaceCullingOn()
    # actor.GetProperty().BackfaceCullingOn()
    # actor.GetProperty().SetOpacity(0.5)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.2, 0.4)

    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(500, 500)

    style = vtk.vtkInteractorStyleTrackballCamera()
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.SetInteractorStyle(style)
    interactor.Initialize()
    interactor.Start()
