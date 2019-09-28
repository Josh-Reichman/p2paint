import sys
import os
import sdl2
import sdl2.ext

debug = True

WHITE = sdl2.ext.Color(255, 255, 255)
BLACK = sdl2.ext.Color(0, 0, 0)

window, render_context = None, None


class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, BLACK)
        super(SoftwareRenderer, self).render(components)


class RenderContext:

    def __init__(self, window):
        self.window = window
        self.world = sdl2.ext.World()

        # initialize renderer and sprite factory
        self.sprite_renderer = SoftwareRenderer(self.window)
        self.world.add_system(self.sprite_renderer)
        self.sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    def CreateSquare(self, position=(0, 0), size=(20, 20), color=WHITE):
        square_sprite = self.sprite_factory.from_color(color, size=size)
        square = Renderable(self.world, square_sprite, position[0], position[1])
        return square


class Renderable(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy

    def Move(self, x, y):
        self.sprite.position = self.sprite.position[0] + x, self.sprite.position[1] + y


def init_rendering():

    global window, render_context

    # initialize window
    sdl2.ext.init()
    window = sdl2.ext.Window("Peer 2 Paint", size=(800, 800))
    window.show()

    render_context = RenderContext(window)
