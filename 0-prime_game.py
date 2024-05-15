#!/usr/bin/python3
"""
prime numbers
"""

def sieve_of_eratosthenes(n):
    """
    Generates a list of prime numbers up to the given
    limit n using the Sieve of Eratosthenes algorithm.
    """

    primes = [True] * (n + 1)
    primes[0] = primes[1] = False

    for i in range(2, int(n**0.5) + 1):
        if primes[i]:
            for j in range(i*i, n + 1, i):
                primes[j] = False

    return [i for i in range(n + 1) if primes[i]]

def isWinner(x, nums):
    """
    Determines the winner of each round and the overall
    winner of the game.
    """
    # Define a function to simulate the game for a given n
    def play_game(n):
        primes = sieve_of_eratosthenes(n)
        maria_turn = True

        while primes:
            if maria_turn:
                choice = primes[0]
                primes = [p for p in primes if p % choice != 0]
                maria_turn = False
            else:
                choice = primes[-1]
                primes = [p for p in primes if p % choice != 0]
                maria_turn = True
        
        return "Maria" if maria_turn else "Ben"

    # Count the number of wins for each player
    maria_wins = 0
    ben_wins = 0

    # Play each round and count the wins
    for n in nums:
        winner = play_game(n)
        if winner == "Maria":
            maria_wins += 1
        elif winner == "Ben":
            ben_wins += 1

    # Determine the overall winner
    if maria_wins > ben_wins:
        return "Maria"
    elif maria_wins < ben_wins:
        return "Ben"
    else:
        return None
