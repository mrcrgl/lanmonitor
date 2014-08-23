

def format_hw_address(hw_address):
    res = []

    for part in hw_address.split(':'):
        res.append(part.rjust(2, '0'))

    return ':'.join(res).upper()