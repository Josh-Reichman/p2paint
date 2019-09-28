import uuid
import json
import rendering


class Object:
    def __init__(self, graphic, serialized_data=None):
        # TODO Attributes needed: graphic assigned, current machine id, visible
        # TODO If serialized data was passed in (from being transferred from a peer) make the object
        #  factoring in velocity and correct position
        self.id = hex(uuid.getnode())
        self.serialized_data = serialized_data
        if serialized_data == None:
            self.graphic = graphic
        else:
            pass
        self.move(20,20)
        print("It works!")

    def serialize(self):
        # TODO Export data to transfer to peers
        pass

    def deserialize(self, input_data):
        # TODO take data and decode value
        json.load(input_data)

    def move(self, velocity_x, velocity_y):
        # TODO Change position based on velocity of drag
        rendering.Renderable.Move(self.graphic, velocity_x, velocity_y)

    def transfer_to_peer(self, peer):
        # TODO Transfer object to peer
        pass


if __name__ == '__main__':
    test = Object()
