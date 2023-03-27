

import socket
import struct


TCP_IP = '192.168.252.143'
TCP_PORT = 42069
TYPESSTRINGS = {0b0:"Null", 0b1:"Camera", 0b10:"ReferenceAbsolute", 0b100:"ReferenceRelative", 0b1000:"Robot", 0b10000:"Puck", 0b100000:"Tag"}
HEADERSTRUCT = "<QQII"
POSSTRUCT = "<BBHfff"
HEADERSIZE = struct.calcsize(HEADERSTRUCT)
POSSIZE = struct.calcsize(POSSTRUCT)

print(f"{HEADERSIZE=} {POSSIZE=}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while True:
    header = s.recv(HEADERSIZE)
    SentTick, Latency, TickRate, NumDatas = struct.unpack(HEADERSTRUCT, header)
    positions = s.recv(NumDatas * POSSIZE)
    print(f"received data: {SentTick=} {Latency=} {TickRate=} {NumDatas=}")
    for i in  range(NumDatas):
        indexstart = POSSIZE*i
        PacketType, PacketNumeral, PacketMetadata, PosX, PosY, Rot = struct.unpack_from(POSSTRUCT, positions, indexstart)
        
        print(f"\t{i}: {TYPESSTRINGS[PacketType]}%{PacketNumeral}({PacketMetadata}) @ ({PosX}, {PosY})/{Rot}")

