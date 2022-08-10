import logging
from copy import deepcopy
from math import tan, cos, sin
from pprint import pformat
from typing import List

import pygame

logger = logging.getLogger(__name__)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class vec3d:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


class triangle:
    def __init__(self, p1: vec3d, p2: vec3d, p3: vec3d) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    @classmethod
    def from_points(cls, *points):
        return cls(
            vec3d(
                points[0],
                points[1],
                points[2],
            ),
            vec3d(
                points[3],
                points[4],
                points[5],
            ),
            vec3d(
                points[6],
                points[7],
                points[8],
            ),
        )

    def __repr__(self):
        return f"{self.p1}, {self.p2}, {self.p3}"


class mesh:
    def __init__(self, triangles) -> None:
        self.tris = triangles


class mat4x4:
    m: List[List]

    def __init__(self) -> None:
        self.m = [
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ]

        self.m = [[0.0] * 4] * 4

    def __repr__(self) -> str:
        return pformat(self.m)


class Window:
    _screenheight: float = 1000.0
    _screenwidth: float = 1000.0

    def __init__(self) -> None:
        self.fTheta = 0.0
        fNear: float = 0.1
        fFar: float = 1000.0
        fFov: float = 90.0
        fAspectRatio = self.screenheight / self.screenwidth
        fFovRad: float = 1.0 / tan(fFov * 0.5 / 180.0 * 3.14159)

        mat_proj = mat4x4()
        mat_proj.m[0] = [fAspectRatio * fFovRad, 0.0, 0.0, 0.0]
        mat_proj.m[1] = [0.0, fFovRad, 0.0, 0.0]
        mat_proj.m[2] = [0.0, 0.0, fFar / (fFar - fNear), 1.0]
        mat_proj.m[3] = [0.0, 0.0, (-fFar * fNear) / (fFar - fNear), 0.0]
        self.mat_proj = mat_proj

        logger.debug("Calculated projection matrix\n%s", mat_proj)

        pygame.init()
        self.screen = pygame.display.set_mode([self.screenheight, self.screenwidth])
        self.clock = pygame.time.Clock()

    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(BLACK)
            self.draw()
            pygame.display.flip()
        print(self.mat_proj)
        pygame.quit()

    @property
    def screenheight(self):
        if not self._screenheight:
            self._screenheight = float(input("Screen Height"))
        return self._screenheight

    @property
    def screenwidth(self):
        if not self._screenwidth:
            self._screenwidth = float(input("Screen Width"))
        return self._screenwidth

    def update(self):
        pass

    cube = mesh(
        [
            # SOUTH
            triangle.from_points(0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0),
            triangle.from_points(0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0),
            # EAST
            triangle.from_points(1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0),
            triangle.from_points(1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0),
            # NORTH
            triangle.from_points(1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0),
            triangle.from_points(1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0),
            # WEST
            triangle.from_points(0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0),
            triangle.from_points(0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
            # TOP
            triangle.from_points(0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0),
            triangle.from_points(0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0),
            # BOTTOM
            triangle.from_points(1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0),
            triangle.from_points(1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0),
        ]
    )

    def draw(self):
        self.clock.tick(60)
        self.fTheta += 1.0 * (self.clock.get_time() / 1000.0)

        matRotZ = mat4x4()
        matRotZ.m[0] = [cos(self.fTheta), sin(self.fTheta), 0.0, 0.0]
        matRotZ.m[1] = [sin(self.fTheta) * -1.0, cos(self.fTheta), 0.0, 0.0]
        matRotZ.m[2] = [0.0, 0.0, 1.0, 0.0]
        matRotZ.m[3] = [0.0, 0.0, 0.0, 1.0]

        matRotX = mat4x4()
        matRotX.m[0] = [1.0, 0.0, 0.0, 0.0]
        matRotX.m[1] = [0.0, cos(self.fTheta * 0.5), sin(self.fTheta * 0.5), 0.0]
        matRotX.m[2] = [0.0, sin(self.fTheta * 0.5) * -1.0, cos(self.fTheta * 0.5), 0.0]
        matRotX.m[3] = [0.0, 0.0, 0.0, 1.0]

        for tri in self.cube.tris:
            logger.debug("Current triangle pre-processed %s", tri)

            # Rotate on Z axis
            tri_rotated_z = triangle(
                multiply_vec3d_mat4x4(tri.p1, matRotZ),
                multiply_vec3d_mat4x4(tri.p2, matRotZ),
                multiply_vec3d_mat4x4(tri.p3, matRotZ),
            )
            # Rotate on X axis
            tri_rotated_zx = triangle(
                multiply_vec3d_mat4x4(tri_rotated_z.p1, matRotX),
                multiply_vec3d_mat4x4(tri_rotated_z.p2, matRotX),
                multiply_vec3d_mat4x4(tri_rotated_z.p3, matRotX),
            )
            # Translate away from camera
            tri_translated = deepcopy(tri_rotated_zx)
            tri_translated.p1.z = tri_rotated_zx.p1.z + 3.0
            tri_translated.p2.z = tri_rotated_zx.p2.z + 3.0
            tri_translated.p3.z = tri_rotated_zx.p3.z + 3.0
            logger.debug(
                "Current triangle translated in front of the camera %s", tri_translated
            )
            # Project onto screen
            tri_projected = triangle(
                multiply_vec3d_mat4x4(tri_translated.p1, self.mat_proj),
                multiply_vec3d_mat4x4(tri_translated.p2, self.mat_proj),
                multiply_vec3d_mat4x4(tri_translated.p3, self.mat_proj),
            )

            logger.debug("Current triangle projected to 2d space %s", tri_projected)

            # Center
            tri_projected.p1.x += 1.0
            tri_projected.p1.y += 1.0
            tri_projected.p2.x += 1.0
            tri_projected.p2.y += 1.0
            tri_projected.p3.x += 1.0
            tri_projected.p3.y += 1.0

            # Scale into view
            tri_projected.p1.x *= 0.5 * self.screenwidth
            tri_projected.p1.y *= 0.5 * self.screenheight
            tri_projected.p2.x *= 0.5 * self.screenwidth
            tri_projected.p2.y *= 0.5 * self.screenheight
            tri_projected.p3.x *= 0.5 * self.screenwidth
            tri_projected.p3.y *= 0.5 * self.screenheight

            logger.debug("Current triangle 2d scaled into view %s", tri_projected)
            # Draw

            pygame.draw.polygon(
                self.screen,
                WHITE,
                (
                    (tri_projected.p1.x, tri_projected.p1.y),
                    (tri_projected.p2.x, tri_projected.p2.y),
                    (tri_projected.p3.x, tri_projected.p3.y),
                ),
                width=2,
            )


def multiply_vec3d_mat4x4(i: vec3d, m: mat4x4):
    x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + m.m[3][0]
    y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + m.m[3][1]
    z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + m.m[3][2]
    o = vec3d(x, y, z)
    w: float = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + m.m[3][3]

    if w != 0.0:
        o.x /= w
        o.y /= w
        o.z /= w

    return o


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    w = Window()
    w.start()
