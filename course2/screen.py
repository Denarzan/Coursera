import pygame
import random
import math


class Vec2d:

    """
    Computation over vectors.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, another_vector):
        """
        Subtraction of two vectors.
        :param self: vector1 -> (x[0], x[1])
        :param another_vector: vector2 -> (y[0], y[1])
        :return: vector3 -> (x[0] - y[0], x[1] - y[1])
        """
        return Vec2d(self.x - another_vector.x, self.y - another_vector.y)

    def __add__(self, another_vector):
        """
        Addition of two vectors.
        :param self: vector1 -> (x[0], x[1])
        :param another_vector: vector2 -> (y[0], y[1])
        :return: vector3 -> (x[0] + y[0], x[1] + y[1])
        """
        return Vec2d(self.x + another_vector.x, self.y + another_vector.y)

    def __mul__(self, k):
        """
        Multiplying a vector by a number.
        :param self: vector1 -> (x[0], x[1])
        :param k: constant
        :return: vector2 -> (x[0] * k, x[1] * k)
        """
        return Vec2d(self.x * k, self.y * k)

    def len(self):
        """
        Length of the vector.
        :param self: vector -> (x[0], x[1])
        :return: constant
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self):
        """
        Take current coordinates of the vector and return tuple with it's values.
        :return: (x, y)
        """
        return self.x, self.y


class Polyline:

    """
    Drawing of polyline
    """

    def __init__(self, points=None, speeds=None, screen_dim=(800, 600)):
        self.points = points or []
        self.speeds = speeds or []
        self.screen_dim = screen_dim

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        """
        Polyline drawing.
        :param style: check draw line or circle
        :param width: width of the line
        :param color: color of the polyline
        :return:
        """
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(self.points[p_n].x), int(self.points[p_n].y)),
                                 (int(self.points[p_n + 1].x), int(self.points[p_n + 1].y)), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.x), int(p.y)), width)

    def append(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        """
        Point coordinates recalculation.
        :param self.points: add new point
        :param self.speeds: speed of the point
        """
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > self.screen_dim[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > self.screen_dim[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)


class Knot(Polyline):

    """
    Adding and recalculating coordinates.
    """

    def __init__(self, points,  count):
        super().__init__()
        self.points = points or []
        self.count = count

    def __get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (self.__get_point(points, alpha, deg - 1) * (1 - alpha))

    def __get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.__get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        """
        Calculation of curve points by added "control" points.
        """
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.__get_points(ptn, self.count))
        return res


"""
Settings of the program
"""


def draw_help():
    """
    Show the commands available for use and run the program.
    """
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    screen_dim = (800, 600)
    pygame.init()
    gameDisplay = pygame.display.set_mode(screen_dim)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    polyline = Polyline(screen_dim=screen_dim)
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    polyline = Polyline(screen_dim=screen_dim)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                polyline.append(Vec2d(event.pos[0], event.pos[1]), Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points()
        knot = Knot(polyline.points, steps)
        curve = Polyline(knot.get_knot())
        curve.draw_points("line", 3, color)
        if not pause:
            polyline.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
