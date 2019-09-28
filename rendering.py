import sys
import os
import sdl2
import sdl2.ext

debug = True

WHITE = sdl2.ext.Color(255, 255, 255)
BLACK = sdl2.ext.Color(0, 0, 0)

window, render_context = None, None


class RenderContext:

    def __init__(self, window):
        self.window = window
        self.world = sdl2.ext.World()
        self.sdl_renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)

    def CreateSquare(self, position=(0, 0), size=(20, 20), color=WHITE):
        square = Renderable(self.world, position[0], position[1])
        return square


class Renderable:
    def __init__(self, world, posx=0, posy=0):
        self.x = posx
        self.y = posy

    def Move(self, x, y):
        self.x = x
        self.y = y

    def MoveAdditive(self, x, y):
        self.x += x
        self.y += y

    def render(self, render_context):
        sdl2.SDL_RenderDrawRect(render_context.sdl_renderer, sdl2.SDL_Rect(0, 0, 100, 100))


def init_rendering():

    global window, render_context

    # initialize window
    sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
    #window = sdl2.ext.Window("Peer 2 Paint", size=(800, 800))
    window = sdl2.SDL_CreateWindow("Peer 2 Paint".encode('utf-8'), sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, 800, 800, 0)
    #window.show()

    render_context = RenderContext(window)


def clear():
    sdl2.SDL_SetRenderDrawColor(render_context.sdl_renderer, 0, 0, 0, 255)
    sdl2.SDL_RenderClear(render_context.sdl_renderer)
    sdl2.SDL_SetRenderDrawColor(render_context.sdl_renderer, 255, 255, 255, 255)

def swap():

    #square_sprite = sdl2.SDL_CreateTexture(render_context.sdl_renderer, sdl2.SDL_PIXELFORMAT_RGB888,
    #                                       sdl2.SDL_TEXTUREACCESS_STATIC, 100, 100)
    #sdl2.SDL_SetTextureBlendMode(square_sprite, sdl2.SDL_BLENDMODE_NONE)
    #sdl2.SDL_RenderCopy(render_context.sdl_renderer, square_sprite, sdl2.SDL_Rect(0, 0, 100, 100), sdl2.SDL_Rect(0, 0, 100, 100))
    #sdl2.SDL_RenderDrawRect(render_context.sdl_renderer, sdl2.SDL_Rect(0, 0, 100, 100))
    sdl2.SDL_RenderPresent(render_context.sdl_renderer)
