import sys
import rendering, objects, networking, input


running = True


def update_selection(object_list, click_point, sel_index):
    for o, obj in enumerate(object_list):
        if obj.graphic.contains(click_point):
            return o
    return -1


def run():
    rendering.init_rendering()

    # TODO: create objects that exist at start here
    object_list = [
        objects.Object(rendering.render_context.CreateSquare(position=(100, 100), size=(60, 60))),
        objects.Object(rendering.render_context.CreatePoint(position=(200, 200))),
        objects.Object(rendering.render_context.CreateCircle(position=(300, 300), size=(60, 60)))
    ]
    global running
    running = True
    clicked = False
    click_point = None
    x_init = 200
    x_post = 200
    y_init = 200
    y_post = 200
    sel_index = 0

    while running:
        result = input.handle_input()
        if result == 'QUIT':
            running = False
        rendering.clear()
        [o.graphic.render(rendering.render_context) for o in object_list]
        rendering.swap()
        if input.is_mouse_down:
            if not clicked:
                x_init = input.x.value
                y_init = input.y.value
                sel_index = update_selection(object_list, (x_init, y_init), sel_index)
            if sel_index is not -1:
                object_list[sel_index].move(input.x.value, input.y.value)
            clicked = True
            click_point = (input.x.value, input.y.value)
        else:
            if clicked:
                if sel_index is not -1:
                    object_list[sel_index].move_additive(input.x.value, input.y.value, x_init, y_init)
                clicked = False
                x_post = input.x.value
                y_post = input.y.value
            else:
                if sel_index is not -1:
                    object_list[sel_index].move_additive(x_init-x_post, y_init-y_post)
    return 0


if __name__ == "__main__":
    sys.exit(run())
