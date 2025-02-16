from agent import Agent


def main():
    alice = Agent('Alice')
    bob = Agent('Bob')

    alice.compare(bob)
    bob.compare(alice)


if __name__ == '__main__':
    main()
