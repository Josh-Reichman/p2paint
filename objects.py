import uuid
import json


class Object:
    def __init__(self, serialized_data=None):
        # TODO Attributes needed: graphic assigned, current machine id, location on screen, visible
        # TODO If serialized data was passed in (from being transferred from a peer) make the object
        #  factoring in velocity and correct position
        self.serialized_data = serialized_data
        self.id = hex(uuid.getnode())

    def serialize(self):
        # TODO Export data to transfer to peers
        pass

    def deserialize(self):
        # TODO take data and decode value
        pass

    def move(self, velocity_x, velocity_y):
        # TODO Change position based on velocity of drag
        pass

    def transfer_to_peer(self, peer):
        # TODO Transfer object to peer
        pass

if __name__ == '__main__':
    test = Object()
