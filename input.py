import sdl2


debug = True


def handle_events():
    events = sdl2.ext.get_events()

    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
            break


def handle_mouse():

    x, y = sdl2.c_int(), sdl2.c_int()
    sdl2.SDL_GetMouseState(x, y)
    if debug:
        print("Mouse position: ", x, y)


def handle_input():
    handle_events()
    handle_mouse()