from agent.blinding_agent import BlindingAgent


def main():
    alice = BlindingAgent('Alice')
    bob = BlindingAgent('Bob')

    alice.handshake(bob)
    bob.handshake(alice)

    alice.run_comparison_test()
    bob.run_comparison_test()


if __name__ == '__main__':
    main()
