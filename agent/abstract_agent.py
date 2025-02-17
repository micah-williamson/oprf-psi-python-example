from __future__ import annotations
import random
from abc import ABC, abstractmethod

from ecdsa.ellipticcurve import Point

from crypto import bytes_to_ec_point, ec_multiply, inverse_mod, pack_ec_point, gen_secret

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
        self.priv_data: set[bytes] = set(data[:random.randint(PRIVATE_SET_SIZE_MIN, PRIVATE_SET_SIZE_MAX)])
        self.pub_data: set[str] = {self._enc(i) for i in self.priv_data}

    def _enc(self, val: bytes) -> str:
        ec_point = bytes_to_ec_point(val)
        new_point = ec_multiply(ec_point, self.secret_key)
        return pack_ec_point(new_point)

    ###############################################################################################
    # Handshake Logic #############################################################################
    ###############################################################################################

    @abstractmethod
    def handshake(self, server: AbstractAgent):
        """Runs handshake logic from the client"""
        raise NotImplementedError()

    ###############################################################################################
    # Public API ##################################################################################
    ###############################################################################################
    def api_get_name(self) -> str:
        return self.name

    ###############################################################################################
    # Agent Testing ###############################################################################
    ###############################################################################################

    @abstractmethod
    def run_comparison_test(self):
        raise NotImplementedError()
