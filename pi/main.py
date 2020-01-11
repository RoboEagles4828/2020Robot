from pixy import *
from ctypes import *

# Initialize pixy interpreter thread
pixy_init()


class Blocks(Structure):
    _fields_ = [("type", c_uint), ("signature", c_uint), ("x", c_uint),
                ("y", c_uint), ("width", c_uint), ("height", c_uint),
                ("angle", c_uint)]


blocks = BlockArray(100)
while True:
    count = pixy_get_blocks(100, blocks)
    if count > 0:  # Blocks found
        for index in range(count):
            print(
                '[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' %
                (blocks[index].type, blocks[index].signature, blocks[index].x,
                 blocks[index].y, blocks[index].width, blocks[index].height))
