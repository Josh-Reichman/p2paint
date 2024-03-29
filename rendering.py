import sys
import os
import sdl2
import sdl2.ext
import ctypes
import numpy as np
from sdl2 import SDL_WINDOW_FULLSCREEN_DESKTOP

debug = True

window_x, window_y = 800, 800
WHITE = sdl2.ext.Color(255, 255, 255)
BLACK = sdl2.ext.Color(0, 0, 0)

window, render_context = None, None


class RenderContext:

    def __init__(self, window):
        self.window = window
        self.world = sdl2.ext.World()
        self.sdl_renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)
        sdl2.SDL_SetWindowFullscreen(window, SDL_WINDOW_FULLSCREEN_DESKTOP)
        sdl2.SDL_GL_SetSwapInterval(1)

    def CreateSquare(self, position=(0, 0), size=(20, 20), color=WHITE):
        return Square(self.world, position[0], position[1], size[0], size[1])

    def CreatePoint(self, position=(0, 0), size=(20, 20), color=WHITE):
        return Point(self.world, position[0], position[1], size[0], size[1])

    def CreateCircle(self, position=(0, 0), size=(20, 20), color=WHITE):
        return Circle(self.world, position[0], position[1], size[0], size[1])

    def CreateLine(self, position=(0, 0), size=(20, 20), color=WHITE):
        return Line(self.world, position[0], position[1], size[0], size[1])


class Renderable:
    def __init__(self, world, posx=0, posy=0, sizex=100, sizey=100):
        self.x = posx
        self.y = posy
        self.sx = sizex
        self.sy = sizey

    def move(self, x, y):
        self.x = x
        self.y = y

    def move_additive(self, x, y):
        self.x += x
        self.y += y

    def render(self, render_context):
        pass


class Square(Renderable):
    def render(self, render_context):
        sdl2.SDL_RenderDrawRect(render_context.sdl_renderer, sdl2.SDL_Rect(int(self.x-self.sx/2), int(self.y-self.sy/2), int(self.sx), int(self.sy)))

    def contains(self, point):
        return self.x-self.sx/2 < point[0] < self.x+self.sx/2 and self.y-self.sy/2 < point[1] < self.y+self.sy/2


class Point(Renderable):
    def render(self, render_context):
        sdl2.SDL_RenderDrawPoint(render_context.sdl_renderer, int(self.x), int(self.y))

    def contains(self, point):
        return False


class Line(Renderable):
    def render(self, render_context):
        sdl2.SDL_RenderDrawLine(
            render_context.sdl_renderer,
            int(self.x),
            int(self.y),
            int(self.x + self.sx),
            int(self.y + self.sy)
        )

    def contains(self, point):
        return False


class Circle(Renderable):
    def render(self, render_context):

        r = self.sx / 2

        theta = np.linspace(0, 2*np.pi, 400)
        points = np.stack((np.cos(theta)*r + self.x, np.sin(theta)*r + self.y), axis=-1).astype(int).tolist()
        points = [tuple(p) for p in points]

        num_points = len(points)

        points = (sdl2.SDL_Point * len(points))(*points)
        sdl2.SDL_RenderDrawPoints(render_context.sdl_renderer, points, num_points)

    def contains(self, point):
        r = self.sx / 2
        return (point[0] - self.x)**2 + (point[1] - self.y)**2 < r**2


def init_rendering():

    global window, render_context

    # initialize window
    sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
    window = sdl2.SDL_CreateWindow("Peer 2 Paint".encode('utf-8'), sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, window_x, window_y, 0)

    render_context = RenderContext(window)


def clear():
    sdl2.SDL_SetRenderDrawColor(render_context.sdl_renderer, 0, 0, 0, 255)
    sdl2.SDL_RenderClear(render_context.sdl_renderer)
    sdl2.SDL_SetRenderDrawColor(render_context.sdl_renderer, 255, 255, 255, 255)


def swap():
    sdl2.SDL_RenderPresent(render_context.sdl_renderer)
