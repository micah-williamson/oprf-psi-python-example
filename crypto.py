import random

from ecdsa import NIST256p
from ecdsa.ellipticcurve import Point
from ecdsa.numbertheory import inverse_mod as ecdsa_inverse_mod


def gen_secret() -> int:
    return int.from_bytes(random.randbytes(32), 'big')


def bytes_to_ec_point(msg: bytes, curve=NIST256p) -> Point:
    x = int.from_bytes(msg, 'big')
    G = curve.generator
    n = curve.order
    return x % n * G


def ec_multiply(ec_point: Point, k: int) -> Point:
    return k * ec_point


def inverse_mod(i: int, curve=NIST256p) -> int:
    return ecdsa_inverse_mod(i, curve.order)


def pack_ec_point(ec_point: Point) -> str:
    return ec_point.to_bytes().hex()


def unpack_ec_point(pack: str, curve=NIST256p) -> Point:
    return Point.from_bytes(curve.curve, bytes.fromhex(pack))
