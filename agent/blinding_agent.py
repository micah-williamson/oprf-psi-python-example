from __future__ import annotations
from agent.abstract_agent import AbstractAgent
from crypto import pack_ec_point, unpack_ec_point, ec_multiply


class BlindingAgent(AbstractAgent):

    def api_hash(self, point: str) -> str:
        ec_point = unpack_ec_point(point)
        new_point = ec_multiply(ec_point, self.secret_key)
        return pack_ec_point(new_point)

    def compare(self, other: BlindingAgent):
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
