import sys
import rendering, objects, networking, input


running = True

def run():
    rendering.init_rendering()

    # TODO: create objects that exist at start here
    object_list = [
        objects.Object(rendering.render_context.CreateSquare(position=(100, 100), size=(60, 60))),
        objects.Object(rendering.render_context.CreateSquare(position=(200, 200), size=(60, 60))),
        objects.Object(rendering.render_context.CreateSquare(position=(300, 300), size=(60, 60)))
    ]
    global running
    running = True
    clicked = False
    x_init = 200
    x_post = 200
    y_init = 200
    y_post = 200

    while running:
        result = input.handle_input()
        if result == 'QUIT':
            running = False
        rendering.clear()
        [o.graphic.render(rendering.render_context) for o in object_list]
        rendering.swap()
        object_list[0].move_additive(1, 1)
        if input.is_mouse_down:
            if not clicked:
                x_init = input.x.value
                y_init = input.y.value
            object_list[0].move(input.x.value, input.y.value)
            clicked = True
        else:
            if clicked:
                object_list[0].move_additive(input.x.value, input.y.value, x_init, y_init)
                clicked = False
                x_post = input.x.value
                y_post = input.y.value
            else:
                object_list[0].move_additive(x_init-x_post, y_init-y_post)
    return 0


if __name__ == "__main__":
    sys.exit(run())
