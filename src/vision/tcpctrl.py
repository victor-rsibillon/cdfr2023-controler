import socket
import struct

type_strings = {
    0b0: "Null",
    0b1: "Camera",
    0b10: "ReferenceAbsolute",
    0b100: "ReferenceRelative",
    0b1000: "Robot",
    0b10000: "Puck",
    0b100000: "Tag"
}

header_struct = "<QQII"
post_struct = "<BBHfff"
header_size = struct.calcsize(header_struct)
pos_size = struct.calcsize(post_struct)


class VisionElement:
    def __init__(self, tag_id: int, x: int, y: int, rot: int):
        self.tag_id = tag_id
        self.x = x
        self.y = y
        self.rotation = rot

    def __getitem__(self, item) -> int:
        match item:
            case "tag_id":
                return self.tag_id
            case "x":
                return self.x
            case "y":
                return self.y
            case "rotation":
                return self.rotation


class VisionListener:
    def __init__(self, ip: str, port=42069):
        self.ip = ip
        self.port = port
        self.socket = None
        self.run_socket = True
        self.debug_packet = False
        self.cache = {}  # Cache containing all tags id as key and their content as value

    def is_socket_setup(self) -> bool:
        return self.socket is not None

    def init_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        self.socket_listener()

    def close_connection(self):
        self.run_socket = False
        self.socket.close()

    def socket_listener(self):
        while self.run_socket:
            header = self.socket.recv(header_size)
            sent_tick, latency, tick_rate, num_datas = struct.unpack(header_struct, header)
            positions = self.socket.recv(num_datas * pos_size)
            if self.debug_packet:
                print(f"MVision-DEBUG> Received data: {sent_tick=} {latency=} {tick_rate=} {num_datas=}")
            for i in range(num_datas):
                index_start = pos_size * i
                PacketType, PacketNumeral, PacketMetadata, PosX, PosY, Rot = struct.unpack_from(post_struct, positions,
                                                                                                index_start)
                try:
                    # try converting to integer if failed warn message
                    vision_element = VisionElement(int(PacketNumeral), int(PosX), int(PosY), int(Rot))
                    self.cache[int(PacketNumeral)] = vision_element
                except ValueError:
                    print(
                        f"MVision-WARN> Attempt to cast some of those items (Numeral={PacketNumeral}, X={PosX}, Y={PosY}, R={Rot}) into int but python cast failed")

                if self.debug_packet:
                    print(f"MVision-DEBUG> \t{i}: {type_strings[PacketType]}%{PacketNumeral}({PacketMetadata}) "
                          f"@ ({PosX}, {PosY})/{Rot}")
