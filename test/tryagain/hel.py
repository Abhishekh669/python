import struct
import ipaddress

# Example raw IP header (for illustration; real data would be captured from a network)
buff = b'\x45\x00\x00\x54\x00\x00\x40\x00\x40\x06\xb1\xe6\xc0\xa8\x00\x68\xc0\xa8\x00\x01'

# Unpack the IP header
header = struct.unpack("<BBHHHBBH4s4s", buff)

# Assign variables from the unpacked data
ver_ihl = header[0]
ver = ver_ihl >> 4
ihl = ver_ihl & 0xF
tos = header[1]
total_length = header[2]
identification = header[3]
flags_offset = header[4]
ttl = header[5]
protocol_num = header[6]
checksum = header[7]
src_address = ipaddress.ip_address(header[8])
dst_address = ipaddress.ip_address(header[9])

# Print the extracted values
print(f"Version: {ver}")
print(f"IHL: {ihl}")
print(f"TOS: {tos}")
print(f"Total Length: {total_length}")
print(f"Identification: {identification}")
print(f"Flags and Fragment Offset: {flags_offset}")
print(f"TTL: {ttl}")
print(f"Protocol Number: {protocol_num}")
print(f"Checksum: {checksum}")
print(f"Source IP Address: {src_address}")
print(f"Destination IP Address: {dst_address}")
