# Websocket Decoding Constants
#######
# Update realtime API packet header size, in bytes.
UPDATE_PACKET_HEADER_SIZE = 8

# Update realtime API packet types.
UPDATE_PACKET_TYPE_ACTION = 1
UPDATE_PACKET_TYPE_PAYLOAD = 2

# Update realtime API payload types.
UPDATE_PAYLOAD_TYPE_JSON = 1
UPDATE_PAYLOAD_TYPE_STRING = 2
UPDATE_PAYLOAD_TYPE_BUFFER = 3

UPDATE_PACKET_HEADER_TYPE = 0
UPDATE_PACKET_HEADER_PAYLOAD_FORMAT = 1
UPDATE_PACKET_HEADER_COMPRESSED = 2
# Byte 3 is unknown, always zero
UPDATE_PACKET_HEADER_PAYLOAD_SIZE = 4 # big endian, 32 bits