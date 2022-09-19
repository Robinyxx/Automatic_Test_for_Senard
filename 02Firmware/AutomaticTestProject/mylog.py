

def print_2bytes_hex(data):
    lin = ['%02X' % i for i in data]
    print(" ".join(lin))


def print_4bytes_hex(data):
    lin = ['%04X' % i for i in data]
    print(" ".join(lin))
