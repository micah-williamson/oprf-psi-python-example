from __future__ import annotations
import random
from abc import ABC, abstractmethod

from ecdsa.ellipticcurve import Point

from crypto import bytes_to_ec_point, ec_multiply, inverse_mod, unpack_ec_point, \
    pack_ec_point, gen_secret

PRIVATE_SET_SIZE_MIN = 20
PRIVATE_SET_SIZE_MAX = 60


class AbstractAgent(ABC):

    def __init__(self, name: str):
        # Local secret salt for hashing
        self.name = name
        self.secret_key = gen_secret()

        # Create local private and public data sets
        data = [f'{i}'.encode() for i in range(100)]
        random.shuffle(data)
        self.priv_data = data[:random.randint(PRIVATE_SET_SIZE_MIN, PRIVATE_SET_SIZE_MAX)]
        self.pub_data = {self._hash(i) for i in self.priv_data}

    def _hash(self, val: bytes) -> str:
        ec_point = bytes_to_ec_point(val)
        new_point = ec_multiply(ec_point, self.secret_key)
        return pack_ec_point(new_point)

    @staticmethod
    def _blind(val: bytes) -> (Point, int):
        """
        Converts the value to a valid POINT on an EC curve.
        Then blinds the value by a blind factor.
        Returns the blinded value and the blind factor used as (BLINDED_VALUE, BLAND_FACTOR).
        The unblinded POINT can be found by passing the blinded value and blind factor to the
            unblind method.
        """
        blind_factor = gen_secret()
        ec_point = bytes_to_ec_point(val)
        blinded_point = ec_multiply(ec_point, blind_factor)
        return blinded_point, blind_factor

    @staticmethod
    def _unblind(blinded_point: Point, blind_factor: int) -> Point:
        b_inverse = inverse_mod(blind_factor)
        unblinded_point = ec_multiply(blinded_point, b_inverse)
        return unblinded_point

    # Public API
    def api_get_name(self) -> str:
        return self.name

    def api_get_public_data(self) -> set[str]:
        return self.pub_data

    def api_hash(self, point: str) -> str:
        ec_point = unpack_ec_point(point)
        new_point = ec_multiply(ec_point, self.secret_key)
        return pack_ec_point(new_point)

    # Test
    @abstractmethod
    def compare(self, other: AbstractAgent):
        raise NotImplementedError()
    def compare(self, other: Agent):
        other_name = other.api_get_name()
        other_data = other.api_get_public_data()

        external_hashes = set()
        for data in self.priv_data:
            data_blind, blind_factor = self._blind(data)
            external_blinded_hash = other.api_hash(pack_ec_point(data_blind))
            external_hash = self._unblind(unpack_ec_point(external_blinded_hash), blind_factor)
            external_hashes.add(pack_ec_point(external_hash))

        intersection = external_hashes.intersection(other_data)

        print(f'Compare {self.name}<>{other_name}')
        print(f'\tLocal: {len(self.priv_data)}')
        print(f'\tExternal: {len(other_data)}')
        print(f'\tIntersection: {len(intersection)}')
