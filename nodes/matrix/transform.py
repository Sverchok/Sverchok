
@node_func
def transform(vertices: Vertices = Required,
              matrix: Matrix = Matrix.id
              ) -> Vertices:
    return vertices @ matrix
