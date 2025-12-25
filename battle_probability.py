"""
Risk Battle Probability Calculator

Computes exact probabilities for battle outcomes in the board game Risk.
Uses dynamic programming to calculate the probability distribution of outcomes.
"""

import click
from collections import defaultdict
from itertools import product


def roll_dice(num_dice):
    """Generate all possible dice roll combinations."""
    return product(range(1, 7), repeat=num_dice)


def compute_single_round_probabilities(attackers, defenders):
    """
    Compute probabilities for a single round of combat.
    Returns a dict mapping (attacker_losses, defender_losses) to probability.
    """
    outcomes = defaultdict(float)

    # Number of dice each side rolls
    attacker_dice = min(attackers, 3)
    defender_dice = min(defenders, 2)

    total_outcomes = 0

    # Enumerate all possible dice rolls
    for attacker_rolls in roll_dice(attacker_dice):
        for defender_rolls in roll_dice(defender_dice):
            total_outcomes += 1

            # Sort rolls in descending order
            a_sorted = sorted(attacker_rolls, reverse=True)
            d_sorted = sorted(defender_rolls, reverse=True)

            # Compare highest dice
            attacker_losses = 0
            defender_losses = 0

            # Compare the highest die from each side
            if a_sorted[0] > d_sorted[0]:
                defender_losses += 1
            else:
                attacker_losses += 1

            # If both sides rolled at least 2 dice, compare second highest
            if len(a_sorted) >= 2 and len(d_sorted) >= 2:
                if a_sorted[1] > d_sorted[1]:
                    defender_losses += 1
                else:
                    attacker_losses += 1

            outcomes[(attacker_losses, defender_losses)] += 1

    # Convert counts to probabilities
    return {k: v / total_outcomes for k, v in outcomes.items()}


def compute_battle_probabilities(attackers, defenders):
    """
    Compute the probability distribution of final outcomes when starting
    with the given number of attackers and defenders.

    Returns a dict mapping (remaining_attackers, remaining_defenders) to probability.
    """
    # Dynamic programming: states are (attackers, defenders) -> probability
    dp = defaultdict(float)
    dp[(attackers, defenders)] = 1.0

    # Process states until all battles are resolved
    while True:
        new_dp = defaultdict(float)
        changed = False

        for (a, d), prob in dp.items():
            # If battle is over, this is a final state
            if a == 0 or d == 0:
                new_dp[(a, d)] += prob
                continue

            changed = True
            # Compute single round outcomes
            round_probs = compute_single_round_probabilities(a, d)

            for (a_loss, d_loss), round_prob in round_probs.items():
                new_state = (a - a_loss, d - d_loss)
                new_dp[new_state] += prob * round_prob

        if not changed:
            break

        dp = new_dp

    return dict(dp)


def format_probability(prob):
    """Format probability as percentage with 4 decimal places."""
    return f"{prob * 100:.4f}%"


@click.command()
@click.option('-a', '--attackers', type=int, default=3, help='Number of attacking armies (default: 3)')
@click.option('-d', '--defenders', type=int, default=2, help='Number of defending armies (default: 2)')
@click.option('--verbose', is_flag=True, help='Show all possible outcomes')
def main(attackers, defenders, verbose):
    """
    Compute battle outcome probabilities for Risk.

    Calculates the exact probability distribution of outcomes when ATTACKERS
    armies attack DEFENDERS armies.
    """
    if attackers <= 0 or defenders <= 0:
        click.echo("Error: Both attackers and defenders must be positive.", err=True)
        return 1

    click.echo(f"\n{'=' * 60}")
    click.echo(f"Risk Battle Probability Calculator")
    click.echo(f"{'=' * 60}")
    click.echo(f"Initial: {attackers} attackers vs {defenders} defenders\n")

    # Compute probabilities
    outcomes = compute_battle_probabilities(attackers, defenders)

    # Separate attacker wins from defender wins
    attacker_wins = sum(prob for (a, d), prob in outcomes.items() if d == 0)
    defender_wins = sum(prob for (a, d), prob in outcomes.items() if a == 0)

    click.echo(f"Summary:")
    click.echo(f"  Attacker wins: {format_probability(attacker_wins)}")
    click.echo(f"  Defender wins: {format_probability(defender_wins)}")

    if verbose:
        click.echo(f"\nDetailed outcomes:")
        click.echo(f"{'Final State':<30} {'Probability':<15}")
        click.echo(f"{'-' * 45}")

        # Sort by probability (descending)
        for (a, d), prob in sorted(outcomes.items(), key=lambda x: x[1], reverse=True):
            state = f"{a} attackers, {d} defenders"
            click.echo(f"{state:<30} {format_probability(prob):<15}")
    else:
        click.echo(f"\nUse --verbose to see all possible final states")

    click.echo(f"\n{'=' * 60}\n")


if __name__ == '__main__':
    main()
