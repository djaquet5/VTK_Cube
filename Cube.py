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


# TODO: Description
def connect_square():
    polys = vtk.vtkCellArray()

    # The vertices have to be in the clockwise
    faces = [
        (0, 4, 5, 1),   # Below face
        (0, 2, 6, 4),   # Behind face
        (0, 1, 3, 2),   # Left face
        (1, 3, 7, 5),   # Front face
        (4, 5, 7, 6),   # Right face
        (3, 2, 6, 7)    # Top face
    ]

    for face in faces:
        polys.InsertNextCell(4, face)

    return polys

# TODO: Description
def connect_triangles():
    polys = vtk.vtkCellArray()

    half_faces = [
        (0, 5, 1),  # Below
        (0, 4, 5),
        (0, 6, 4),  # Behind
        (0, 2, 6),
        (0, 1, 3),  # Left
        (0, 3, 2),
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
    # TODO: range of the loops [-0.5, 0.5]
    points = vtk.vtkPoints()
    noVertex = 0
    for i in range(2):
        for j in range(2):
            for k in range(2):
                points.InsertPoint(noVertex, (i-0.5, j-0.5, k-0.5))
                noVertex += 1

    # FIXME: to test the creation with different topology, uncomment the line to be tested
    polys = connect_square()
    # polys = connect_triangles()

    scalars = vtk.vtkFloatArray()
    for i in range(8):
        scalars.InsertTuple1(i, i)

    cube = vtk.vtkPolyData()
    cube.SetPoints(points)
    cube.SetPolys(polys)
    cube.GetPointData().SetScalars(scalars)

    # TODO: Generate the file
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

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)

    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(500, 500)

    style = vtk.vtkInteractorStyleTrackballCamera()
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.SetInteractorStyle(style)
    interactor.Initialize()
    interactor.Start()
