from hashlib import sha256

# Define secp256r1 curve parameters
P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
A = -3
B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B


def bytes_to_field(msg: bytes) -> int:
    """Hash message to a field element mod P using SHA-256"""
    digest = sha256(msg).digest()
    return int.from_bytes(digest, 'big') % P


def bytes_to_ec_point(msg: bytes) -> (int, int):
    """Hash a message to an elliptic curve point using a simplified SSWU method"""
    x = bytes_to_field(msg)
    while True:
        rhs = (x**3 + A*x + B) % P
        y = pow(rhs, (P + 1) // 4, P)
        if (y * y) % P == rhs:
            return x, y
        x = (x + 1) % P


def ec_multiply(ec_point: (int, int), k: int) -> (int, int):
    """Move the point around the curve"""
    return ec_point[0] * k % P, ec_point[1] * k % P


def mod_inverse(i: int) -> int:
    return pow(i, -1, P)


def pack_ec_point(ec_point: (int, int)) -> str:
    return (ec_point[0].to_bytes(32, 'big') + ec_point[1].to_bytes(32, 'big')).hex()


def unpack_ec_point(pack: str) -> (int, int):
    pack = bytes.fromhex(pack)
    return int.from_bytes(pack[:32], 'big'), int.from_bytes(pack[32:], 'big')
