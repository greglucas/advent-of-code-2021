
print("--- DAY 16 ---")
print("--- PART 1 ---")

with open("input.txt") as f:
    transmission = f.readline().strip()

# Test cases
# transmission = "D2FE28"
# transmission = "38006F45291200"
# transmission = "EE00D40C823060"
# transmission = "8A004A801A8002F478"
# transmission = "620080001611562C8802118E34"
# transmission = "C0015000016115A2E0802F182340"
# transmission = "A0016C880162017C3686B18A3D4780"


# Hexadecimal, base 16
# [2:] strips off the leading 0b
# zfill left-pads zeros
bits = ""
for x in transmission:
    bits += bin(int(x, 16))[2:].zfill(4)


# To get back to decimal number: int(bits[x:y], 2)
def binary_to_decimal(bits):
    return int(bits, 2)


def read_packets(bits, packets=list(), loc=0):
    """Reads a packet from the input bits"""
    # First three bits are the version
    version = binary_to_decimal(bits[loc:loc+3])
    loc += 3
    # Next 3 numbers are the type ID
    type_id = binary_to_decimal(bits[loc:loc+3])
    loc += 3
    if type_id == 4:
        # This is a literal value
        # pad to a multiple of 4?
        # bits = bits.zfill(len(bits) + 4 - len(bits) % 4)
        # Now we group into sets of 5
        value_bits = ""
        while True:
            value_bits += bits[loc+1:loc+5]
            loc += 5
            if bits[loc-5] == "0":
                # This was the last value
                break

        packet = {"version": version, "type_id": type_id,
                  "value": int(binary_to_decimal(value_bits))}
        packets.append(packet)
        return packets, loc

    # We have an operator packet
    packet = {"version": version, "type_id": type_id}
    packets.append(packet)
    length_type_id = bits[loc]
    loc += 1
    if length_type_id == "0":
        # Next 15 bits are a number representing total length in bits
        # of the sub-packets contained by this packet.
        length_subpacket = int(binary_to_decimal(bits[loc:loc+15]))
        loc += 15
        end_loc = loc + length_subpacket

        while loc < end_loc:
            packets, loc = read_packets(bits, packets, loc)
    else:
        # Next 11 bits are a number of sub-packets immediately
        # contained within this packet
        n_sub_packets = int(binary_to_decimal(bits[loc:loc+11]))
        loc += 11
        for _ in range(n_sub_packets):
            packets, loc = read_packets(bits, packets, loc)

    return packets, loc


packets, _ = read_packets(bits)
version_sum = 0
for packet in packets:
    version_sum += packet['version']

print(f"The version sum of the packets is: {version_sum}")

print("--- DAY 16 ---")
print("--- PART 2 ---")

# Repeat the function and just add in the new operations

def read_packets(bits, packets=list(), loc=0):
    """Reads a packet from the input bits"""
    # First three bits are the version
    version = binary_to_decimal(bits[loc:loc+3])
    loc += 3
    # Next 3 numbers are the type ID
    type_id = binary_to_decimal(bits[loc:loc+3])
    loc += 3
    if type_id == 4:
        # This is a literal value
        # pad to a multiple of 4
        # bits = bits.zfill(len(bits) + 4 - len(bits) % 4)
        # Now we group into sets of 5
        value_bits = ""
        while True:
            value_bits += bits[loc+1:loc+5]
            loc += 5
            if bits[loc-5] == "0":
                # This was the last value
                break

        packet = {"version": version, "type_id": type_id,
                  "value": int(binary_to_decimal(value_bits))}
        packets.append(packet)
        return packets, loc

    # We have an operator packet
    original_packets = packets
    packets = list()
    length_type_id = bits[loc]
    loc += 1
    if length_type_id == "0":
        # Next 15 bits are a number representing total length in bits
        # of the sub-packets contained by this packet.
        length_subpacket = int(binary_to_decimal(bits[loc:loc+15]))
        loc += 15
        end_loc = loc + length_subpacket

        while loc < end_loc:
            packets, loc = read_packets(bits, packets, loc)
    else:
        # Next 11 bits are a number of sub-packets immediately
        # contained within this packet
        n_sub_packets = int(binary_to_decimal(bits[loc:loc+11]))
        loc += 11
        for _ in range(n_sub_packets):
            packets, loc = read_packets(bits, packets, loc)

    if type_id == 0:
        # Sum
        value = sum(packet["value"] for packet in packets)
    elif type_id == 1:
        # product
        value = 1
        for packet in packets:
            value *= packet["value"]
    elif type_id == 2:
        # min
        value = min(packet["value"] for packet in packets)
    elif type_id == 3:
        # max
        value = max(packet["value"] for packet in packets)
    elif type_id == 5:
        # greater than
        value = 1 if packets[0]["value"] > packets[1]["value"] else 0
    elif type_id == 6:
        # less than
        value = 1 if packets[0]["value"] < packets[1]["value"] else 0
    elif type_id == 7:
        # equal to
        value = 1 if packets[0]["value"] == packets[1]["value"] else 0

    packet = {"version": version, "type_id": type_id, "value": value}
    packets = original_packets
    packets.append(packet)
    return packets, loc

packets, _ = read_packets(bits)
# Packets is reduced to one outermost packet now
print(f"The value of the outermost packet is: {packets[0]['value']}")
