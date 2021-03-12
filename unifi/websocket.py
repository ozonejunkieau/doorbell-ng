import ssl
import struct
import zlib
import json

from websocket import create_connection

from .helpers import get_cookie_and_token
from .constants import *

def get_websocket(protect_ip, username, password, verify_ssl=False):
    # Perform an authentication against the Protect controller, grab the cookie and token

    update_ws_url = f"wss://{protect_ip}/proxy/protect/ws/updates"
    
    cookie, _ = get_cookie_and_token(protect_ip, username, password, verify_ssl)

    if not verify_ssl:
        sslopt = {"cert_reqs": ssl.CERT_NONE}
    else:
        sslopt = {}

    ws = create_connection(update_ws_url, cookie=cookie, sslopt=sslopt)

    return ws


def read_u32_in_bytes(_bytes, position):
    subarray = _bytes[position:position+4]
    return struct.unpack(b'>I', subarray)[0]


def read_u8_in_bytes(_bytes, position):
    return int(_bytes[position])


def decode_update_frame(in_bytes, packet_type):
    frame_type = read_u8_in_bytes(in_bytes, UPDATE_PACKET_HEADER_TYPE)    

    if frame_type != packet_type:
        # Throw an error
        assert False

    payload_format = read_u8_in_bytes(in_bytes, UPDATE_PACKET_HEADER_PAYLOAD_FORMAT)

    payload_compressed = read_u8_in_bytes(in_bytes, UPDATE_PACKET_HEADER_COMPRESSED)

    if payload_compressed:
        payload = zlib.decompress(in_bytes[UPDATE_PACKET_HEADER_SIZE:])
    else:
        payload = in_bytes[UPDATE_PACKET_HEADER_SIZE:]
        

    if payload_format == UPDATE_PAYLOAD_TYPE_JSON:
        return json.loads(payload.decode())
    elif payload_format == UPDATE_PAYLOAD_TYPE_STRING:
        return payload.decode()
    elif payload_format == UPDATE_PAYLOAD_TYPE_BUFFER:
        return payload
    else:
        # Raise an error
        assert False

def decode_update_packet(in_bytes):
        
    ## CHECK PACKET MAKES SENSE
    payload_size_bytes = in_bytes[UPDATE_PACKET_HEADER_PAYLOAD_SIZE:UPDATE_PACKET_HEADER_PAYLOAD_SIZE + 4]
    payload_size = read_u32_in_bytes(in_bytes, UPDATE_PACKET_HEADER_PAYLOAD_SIZE)

    data_offset = payload_size + UPDATE_PACKET_HEADER_SIZE

    total_size = data_offset + UPDATE_PACKET_HEADER_SIZE + read_u32_in_bytes(in_bytes, data_offset + UPDATE_PACKET_HEADER_PAYLOAD_SIZE)

    if total_size != len(in_bytes):
        # Throw an error!
        assert False

    action_frame_bytes = in_bytes[0:data_offset]
    payload_frame_bytes = in_bytes[data_offset:]

    action_frame = decode_update_frame(action_frame_bytes, UPDATE_PACKET_TYPE_ACTION)
    payload_frame = decode_update_frame(payload_frame_bytes, UPDATE_PACKET_TYPE_PAYLOAD)
    
    return action_frame, payload_frame