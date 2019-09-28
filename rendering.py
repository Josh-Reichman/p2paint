import sys
import sdl2
import sdl2.ext

WHITE = sdl2.ext.Color(255, 255, 255)

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)


class Renderable(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy


def run():

    # initialize window
    sdl2.ext.init()
    window = sdl2.ext.Window("Peer to Paint", size=(800, 800))
    window.show()
    world = sdl2.ext.World()

    # initialize renderer and sprite factory
    sprite_renderer = SoftwareRenderer(window)
    world.add_system(sprite_renderer)
    sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    # create sprites
    square = sprite_factory.from_color(WHITE, size=(40, 40))

    player1 = Renderable(world, square, 0, 250)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        world.process()
    return 0


if __name__ == "__main__":
    sys.exit(run())