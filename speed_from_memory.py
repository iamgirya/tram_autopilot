from pymem import *
from pymem.process import *
from pymem.ptypes import RemotePointer

mem = Pymem("TramSimVienna-Win64-Shipping.exe")
offsets = [0x28, 0x508, 0x10, 0x260, 0x12C]
base_offset = 0x04B6F410


def getPtrAddr(base, offsets):
    remote_pointer = RemotePointer(mem.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(
                mem.process_handle, remote_pointer.value + offset
            )
        else:
            return remote_pointer.value + offset


def get_speed_from_memory():
    return mem.read_int(getPtrAddr(mem.base_address + base_offset, offsets))


# Значение скорости, которое может влиять на трамвай
# getPtrAddr(mem.base_address + 0x047DE9E0, [0xD8, 0x1A0, 0x470, 0xA0, 0x380])
# formatted_speed = speed // 1000000
# formatted_speed = 250 / (1155 - formatted_speed)
# formatted_speed = 0 if formatted_speed <= 0 else formatted_speed
