from __future__ import annotations

from ecdsa.ellipticcurve import Point

from agent.abstract_agent import AbstractAgent
from crypto import pack_ec_point, unpack_ec_point, ec_multiply, gen_secret, bytes_to_ec_point, \
    inverse_mod


class BlindingAgent(AbstractAgent):

    def __init__(self, *args):
        super().__init__(*args)
        self._servers: dict[str, tuple[BlindingAgent, set[str]]] = {}

    ###############################################################################################
    # Handshake Logic #############################################################################
    ###############################################################################################

    def handshake(self, server: BlindingAgent):
        """Runs handshake logic from the client"""
        self._servers[server.api_get_name()] = (server, server.api_get_public_data())

    ###############################################################################################
    # Internal Logic ##############################################################################
    ###############################################################################################

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

    ###############################################################################################
    # Public API ##################################################################################
    ###############################################################################################

    def api_hash(self, point: str) -> str:
        ec_point = unpack_ec_point(point)
        new_point = ec_multiply(ec_point, self.secret_key)
        return pack_ec_point(new_point)

    def api_get_public_data(self) -> set[str]:
        return self.pub_data

    ###############################################################################################
    # Agent Testing ###############################################################################
    ###############################################################################################

    def run_comparison_test(self):
        for server_name, server_props in self._servers.items():
            server, server_data = server_props
            print(f'Comparing {self.name}<>{server_name}')

            external_hashes = set()
            for data in self.priv_data:
                data_blind, blind_factor = self._blind(data)
                external_blinded_hash = server.api_hash(pack_ec_point(data_blind))
                external_hash = self._unblind(unpack_ec_point(external_blinded_hash), blind_factor)
                external_hashes.add(pack_ec_point(external_hash))

            intersection = external_hashes.intersection(server_data)

            print(f'\tLocal: {len(self.priv_data)}')
            print(f'\tExternal: {len(server_data)}')
            print(f'\tIntersection: {len(intersection)}')
