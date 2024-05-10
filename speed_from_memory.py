from pymem import *
from pymem.process import *
from pymem.ptypes import RemotePointer

mem = Pymem("TramSimVienna-Win64-Shipping.exe")
# offsets = [0x28, 0x508, 0x10, 0x260, 0x12C] переменная со значением спидометра
# base_offset = 0x04B6F410
speed_offsets = [0xD8, 0x1A0, 0x470, 0xA0, 0x380]  # переменная со значением скорости
speed_base_offset = 0x047DE9E0
acceleration_offsets = [0x28, 0x508, 0x10, 0x3B0, 0x90]
acceleration_base_offset = 0x04B6F410


def getPtrAddr(base, offsets):
    remote_pointer = RemotePointer(mem.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(
                mem.process_handle, remote_pointer.value + offset
            )
        else:
            return remote_pointer.value + offset


def get_speed():
    return (
        mem.read_float(getPtrAddr(mem.base_address + speed_base_offset, speed_offsets))
        * 0.0357
    )


def get_acceleration():
    return (
        mem.read_float(
            getPtrAddr(
                mem.base_address + acceleration_base_offset, acceleration_offsets
            )
        )
        / 4.16
    )
