from __future__ import print_function
import pixy
from ctypes import *
from pixy import *
from networktables import NetworkTables

pixy.init()
pixy.change_prog("color_connected_components")

NetworkTables.initialize(server="10.48.28.2")
network_table = NetworkTables.getTable("pi")


class Blocks(Structure):
    _fields_ = [("m_signature", c_uint), ("m_x", c_uint), ("m_y", c_uint),
                ("m_width", c_uint), ("m_height", c_uint), ("m_angle", c_uint),
                ("m_index", c_uint), ("m_age", c_uint)]


frame_width = 315
blocks = BlockArray(100)

while 1:
    count = pixy.ccc_get_blocks(100, blocks)

    if count == 1:
        network_table.putNumber("value", 2 * blocks[0].m_x / frame_width - 1)
        print('[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' %
              (blocks[0].m_signature, blocks[0].m_x, blocks[0].m_y,
               blocks[0].m_width, blocks[0].m_height))
