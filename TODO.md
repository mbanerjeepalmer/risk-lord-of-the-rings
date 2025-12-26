# RISK
_more fun with maths!_

## Question 1: What are the attack/defence probabilities?
_'Eight into four is a decent ratio'_
Write a python script that helps compute the probability in risk
- different numbers of attackers and defenders
- compute the probabilities of different outcomes between three attackers and two defenders in the board game risk. make it a cli using click

TODO:
- Roll limit: on a 3 vs 1, but for a single dice roll.

This is the current output for the battle probabilities. Make a table using rich and use the columns as attack and defence losses. also colour code it
```
2:26:23 on master ✖ ✹ ✭)──> uv run battle_probability.py -a 3 -d 2 --verbose                                                                                         ──(Fri,Dec26)─┘

============================================================
Risk Battle Probability Calculator
============================================================
Initial: 3 attackers vs 2 defenders

Summary:
  Attacker wins: 65.5954%
  Defender wins: 34.4046%

Detailed outcomes:
Final State                    Probability    
---------------------------------------------
3 attackers, 0 defenders       37.1656%       
0 attackers, 2 defenders       21.8071%       
2 attackers, 0 defenders       19.4315%       
0 attackers, 1 defenders       12.5975%       
1 attackers, 0 defenders       8.9982%    
```
## Question 2: which is the most bonus-efficient region to take?

For each territory in a region, how many bonus troops do I receive?


## Question 3: How vulnerable is a given region?

- 
