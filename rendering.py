import sys
import os
import sdl2
import sdl2.ext

debug = True

WHITE = sdl2.ext.Color(255, 255, 255)
RED = sdl2.ext.Color(255, 0, 0)
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
        self.sdl_renderer = sdl2.ext.TextureSpriteRenderSystem(self.window)
        # initialize renderer and sprite factory
        self.sprite_renderer = SoftwareRenderer(self.window)
        self.world.add_system(self.sprite_renderer)
        self.sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.sdl_renderer)

    def CreateSquare(self, position=(0, 0), size=(20, 20), color=WHITE):
        square_sprite = self.sprite_factory.from_color(color, size=size)
        square = Renderable(self.world, square_sprite, position[0], position[1])
        return square

    def CreatePoint(self, position=(0, 0), color=WHITE):
        #sdl2.SDL_RenderDrawPoint(self.sdl_renderer.sdlrenderer, position[0], position[1])
        point_sprite = self.sprite_factory.create_texture_sprite(self.sdl_renderer._renderer, (10, 10), access=sdl2.SDL_TEXTUREACCESS_TARGET)

        return Renderable(self.world, point_sprite, position[0], position[1])


class Renderable(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.x = posx
        self.sprite.y = posy

    def Move(self, x, y):
        self.sprite.x += x
        self.sprite.y += y

    def render(self, render_context):
        renderer = render_context.sdl_renderer._renderer
        sdl2.SDL_SetRenderTarget(renderer.sdlrenderer, self.sprite.texture)
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, 255, 0, 0, 255)
        sdl2.SDL_RenderDrawPoint(renderer.sdlrenderer, 5, 5)
        sdl2.SDL_SetRenderTarget(renderer.sdlrenderer, None)
        render_context.sdl_renderer.render(self.sprite)
        #sdl2.SDL_RenderCopy(renderer.sdlrenderer, self.sprite.texture)
        #self.sprite.texture.render()

        # SDL_SetRenderTarget(gRenderer, NULL);
        # gTargetTexture.render(0, 0, NULL, angle, & screenCenter );

def init_rendering():

    global window, render_context

    # initialize window
    sdl2.ext.init()
    window = sdl2.ext.Window("Peer 2 Paint", size=(800, 800))
    window.show()

    render_context = RenderContext(window)


def clear():
    sdl2.SDL_RenderClear(render_context.sdl_renderer.sdlrenderer)
