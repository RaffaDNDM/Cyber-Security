def msg_to_byte(msg):
    encoded_msg = []

    for x in msg:
        encoded_msg.append(format(ord(x), '08b'))

    return encoded_msg

def byte_to_msg(msg):
    decoded_msg = ''
    for x in msg:
        decoded_msg+=chr(int(x, 2))

    return decoded_msg