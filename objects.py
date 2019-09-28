import uuid
import rendering


class Object:
    def __init__(self, graphic, serialized_data=None):
        self.id = hex(uuid.getnode())
        self.serialized_data = serialized_data
        if serialized_data is None:
            self.graphic = graphic
        else:
            pass

    def serialize(self):
        # TODO Export data to transfer to peers
        pass

    def deserialize(self, input_data):
        # TODO take data and decode value
        pass

    def move(self, x, y):
        rendering.Renderable.Move(self.graphic, x, y)

    def move_additive(self, x, y, x_init=0, y_init=0):
        rendering.Renderable.MoveAdditive(self.graphic, (x_init - x) // 10, (y_init - y)//10)

    def transfer_to_peer(self, peer):
        # TODO Transfer object to peer
        pass
