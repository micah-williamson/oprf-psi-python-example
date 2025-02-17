from __future__ import annotations

from agent.abstract_agent import AbstractAgent
from crypto import pack_ec_point, unpack_ec_point, ec_multiply


class DoubleEncryptionAgent(AbstractAgent):

    def __init__(self, *args):
        super().__init__(*args)
        self._servers: list[DoubleEncryptionAgent] = []
        self._clients: dict[str, tuple[DoubleEncryptionAgent, set[str]]] = {}

    ###############################################################################################
    # Handshake Logic #############################################################################
    ###############################################################################################

    def handshake(self, server: DoubleEncryptionAgent):
        """Runs handshake logic from the client"""
        server_set = server.api_get_public_data()
        double_enc_set = {pack_ec_point(ec_multiply(unpack_ec_point(x), self.secret_key)) for x in server_set}
        server.establish_client(self, double_enc_set)
        self._servers.append(server)

    def establish_client(self, client: DoubleEncryptionAgent, shared_enc_set: set[str]):
        self._clients[client.api_get_name()] = (client, shared_enc_set)

    ###############################################################################################
    # Public API ##################################################################################
    ###############################################################################################

    def api_check_intersection(self, client: DoubleEncryptionAgent, point: str) -> bool:
        client_name = client.api_get_name()
        shared_set = self._clients[client_name][1]

        ec_point = unpack_ec_point(point)
        new_point = ec_multiply(ec_point, self.secret_key)
        needle = pack_ec_point(new_point)

        return needle in shared_set

    def api_get_public_data(self) -> set[str]:
        return self.pub_data

    ###############################################################################################
    # Agent Testing ###############################################################################
    ###############################################################################################

    def run_comparison_test(self):
        for server in self._servers:
            server_name = server.api_get_name()
            print(f'Comparing {self.name}<>{server_name}')

            intersection = set()
            for member in self.priv_data:
                if server.api_check_intersection(self, self._enc(member)):
                    intersection.add(member)

            print(f'\tLocal: {len(self.priv_data)}')
            print(f'\tExternal: {len(server.api_get_public_data())}')
            print(f'\tIntersection: {len(intersection)}')
