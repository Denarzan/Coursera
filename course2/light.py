class Light:
    """
    Given class.
    """
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    """
    Given class.
    """
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class MappingAdapter:
    """
    Implementing an adapter for the class.
    """
    def __init__(self, adaptee):
        self.adaptee = adaptee  # Save the adaptable object
        self.lights = []
        self.obstacles = []
        self.dim = [0, 0]

    def lighten(self, grid):  # Determine the method for calculating the illumination
        self.dim = [len(grid[0]), len(grid)]  # Determining the size of the map

        for i in range(self.dim[0]):  # Calculate positions of objects from the source map
            for j in range(self.dim[1]):
                if grid[j][i] > 0:
                    self.lights.append((i, j))  # adding lights
                elif grid[j][i] < 0:
                    self.obstacles.append((i, j))  # adding obstacles

        self.adaptee.set_dim(self.dim)  # Setting the size of the map in the adapted object
        self.adaptee.set_lights(self.lights)  # Setting lights
        self.adaptee.set_obstacles(self.obstacles)  # Setting obstacles

        return self.adaptee.generate_lights()
