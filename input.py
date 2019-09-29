import sdl2


debug = False

is_mouse_down = False
x = 0.0
y = 0.0
x_hold = 0.
y_hold = 0.


def handle_events():
    global is_mouse_down

    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT or (event.type == sdl2.SDL_KEYUP and event.key.keysym.sym == sdl2.SDLK_q):
            return 'QUIT'
        elif event.type == sdl2.SDL_KEYUP:
            if event.key.keysym.sym == sdl2.SDLK_s:
                return 'SQUARE'
            elif event.key.keysym.sym == sdl2.SDLK_c:
                return 'CIRCLE'
            elif event.key.keysym.sym == sdl2.SDLK_p:
                return 'POINT'
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            is_mouse_down = True
        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            is_mouse_down = False


def handle_mouse():
    global x
    global y
    global x_hold
    global y_hold
    x, y = sdl2.c_int(), sdl2.c_int()
    sdl2.SDL_GetMouseState(x, y)
    x, y = float(x.value), float(y.value)
    if debug:
        print("Mouse position: ", x, y, "Mouse down: ", is_mouse_down)


def handle_input():
    result = handle_events()
    handle_mouse()
    return result

def get_x():
    return x

def get_y():
    return y

def store_position():
    x_hold = x
    y_hold = y
