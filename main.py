import sys
import rendering, objects, networking, input
import numpy as np


running = True


def update_selection(object_list, click_point, sel_index):
    for o, obj in enumerate(object_list):
        if obj.graphic.contains(click_point):
            return o
    return -1


def run():
    rendering.init_rendering()

    line = rendering.render_context.CreateLine(position=(0., 0.), size=(40, 40))

    # TODO: create objects that exist at start here
    object_list = [
        objects.Object(rendering.render_context.CreateSquare(position=(100., 100.), size=(60, 60))),
        objects.Object(rendering.render_context.CreatePoint(position=(200., 200.))),
        objects.Object(rendering.render_context.CreateCircle(position=(300., 300.), size=(60, 60))),
    ]
    global running
    running = True
    clicked = False
    click_point = None
    x_init = 200.
    x_post = 200.
    y_init = 200.
    y_post = 200.
    sel_index = 0
    friction = 1.0

    while running:
        result = input.handle_input()
        if result == 'QUIT':
            running = False
        rendering.clear()
        # render all objects
        [o.graphic.render(rendering.render_context) for o in object_list]
        # update all objects' positions and velocities
        for o in object_list:
            o.move_additive(o.vx, o.vy)
            avx, avy = abs(o.vx), abs(o.vy)
            if avx + avy == 0:
                continue
            friction_x = friction * avx / (avx + avy)
            friction_y = friction * avy / (avx + avy)
            if o.vx > 0:
                o.vx = max(o.vx - friction_x, 0.0)
            else:
                o.vx = min(o.vx + friction_x, 0.0)
            if o.vy > 0:
                o.vy = max(o.vy - friction_y, 0.0)
            else:
                o.vy = min(o.vy + friction_y, 0.0)
        if input.is_mouse_down:
            if not clicked:
                x_init = input.x
                y_init = input.y
                sel_index = update_selection(object_list, (x_init, y_init), sel_index)
                line.move(input.x, input.y)
            if sel_index is not -1:
                object_list[sel_index].move(input.x, input.y)
            clicked = True
            click_point = (input.x, input.y)
            if object_list[sel_index].graphic.contains((input.x, input.y)):
                line.sx, line.sy = input.x - line.x, input.y - line.y
                line.render(rendering.render_context)
        else:
            if clicked:
                if sel_index is not -1:
                    object_list[sel_index].vx, object_list[sel_index].vy = input.x-x_init, input.y-y_init
                clicked = False
                x_post = input.x
                y_post = input.y
        rendering.swap()

    return 0


if __name__ == "__main__":
    sys.exit(run())
