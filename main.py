import sys
import rendering, objects, networking, input


running = True


def run():
    rendering.init_rendering()

    # TODO: create objects that exist at start here
    object_list = [
        objects.Object(rendering.render_context.CreateSquare(position=(200, 200), size=(60, 60))),
        objects.Object(rendering.render_context.CreateSquare(position=(200, 200), size=(60, 60)))
    ]
    global running
    running = True
    while running:
        result = input.handle_input()
        if result == 'QUIT':
            running = False
        rendering.clear()
        [o.graphic.render(rendering.render_context) for o in object_list]
        #rendering.render_context.sdl_renderer.render([o.graphic.sprite for o in object_list])
        rendering.swap()
        object_list[0].moveAdditive(1, 1)
        if input.is_mouse_down:
            object_list[0].move(input.x.value, input.y.value)
    return 0


if __name__ == "__main__":
    sys.exit(run())
