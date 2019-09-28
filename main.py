import sys
import rendering, objects, networking, input


running = True


def run():
    rendering.init_rendering()
    # TODO: create objects that exist at start here
    test_object = objects.Object(rendering.render_context.CreateSquare(position=(200, 200), size=(60, 60)))
    #square2 = render_context.CreateSquare(position=(200, 200), size=(60, 60))
    global running
    running = True
    while running:
        result = input.handle_input()
        if result == 'QUIT':
            running = False
        rendering.render_context.world.process()
    return 0


if __name__ == "__main__":
    sys.exit(run())
