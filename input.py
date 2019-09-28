import sdl2


debug = True

is_mouse_down = False


def handle_events():
    global is_mouse_down

    events = sdl2.ext.get_events()

    for event in events:
        if event.type == sdl2.SDL_QUIT:
            return 'QUIT'
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            is_mouse_down = True
        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            is_mouse_down = False


def handle_mouse():

    x, y = sdl2.c_int(), sdl2.c_int()
    sdl2.SDL_GetMouseState(x, y)
    if debug:
        print("Mouse position: ", x, y, "Mouse down: ", is_mouse_down)


def handle_input():
    result = handle_events()
    handle_mouse()
    return result
