import sys
import rendering, objects, networking


running = True


def run():
    rendering.init_rendering()
    # TODO: create objects that exist at start here
    #square2 = render_context.CreateSquare(position=(200, 200), size=(60, 60))
    global running
    running = True
    while running:
        rendering.handle_events()
        rendering.render_context.world.process()
    return 0


if __name__ == "__main__":
    sys.exit(run())
