slow = 1
fast = 3
class Plant():
    def __init__(self, height, grow_speed):
        self.height = height
        self.grow_speed = grow_speed

    def grow(self):
        '''Makes plant grow'''


class Rose(Plant):
  def __init__(self, grow_speed):
    super().__init__(grow_speed)

class Tulip(Plant):
    def __init__(self, grow_speed):
        super().__init__(grow_speed)

class Daisy(Plant):
    def __init__(self, grow_speed):
        super().__init__(grow_speed)


Plants = [Rose(), Tulip(), Daisy()]
for plant in Plants:
    plant.grow()