from agent.abstract_agent import AbstractAgent
from agent.blinding_agent import BlindingAgent
from agent.double_encryption_agent import DoubleEncryptionAgent


def main():
    do_test(DoubleEncryptionAgent)
    do_test(BlindingAgent)


def do_test(klass: type[AbstractAgent]):
    print(f'@@--')
    print(f'Running test with {klass.__name__}')
    alice = klass('Alice')
    bob = klass('Bob')

    alice.handshake(bob)
    bob.handshake(alice)

    alice.run_comparison_test()
    bob.run_comparison_test()
    print(f'--@@')


if __name__ == '__main__':
    main()
