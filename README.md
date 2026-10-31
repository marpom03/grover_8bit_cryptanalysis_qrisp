# Grover-Based Cryptanalysis of an 8-Bit Cipher

## Overview

This project explores quantum cryptanalysis of a simplified
8-bit block cipher using Grover's search algorithm.

The goal is to recover an encryption key using a quantum
oracle implemented with the Qrisp framework and compare
the results with a classical brute-force attack.

This project is developed as part of the Post-Quantum Cryptography course 
in the Master’s degree program in Cybersecurity at AGH University of Krakow.

## Objectives

- Design and implement a simplified 8-bit block cipher.
- Implement a reversible quantum version of the cipher.
- Construct a quantum oracle for key verification.
- Recover the encryption key using Grover's algorithm.
- Analyze the impact of Grover iterations on success probability.
- Compare quantum and classical key-search methods.

## Technologies

- Python
- Qrisp
- Quantum circuit simulation

## Project Structure

- `src/classical/` - Classical cipher and brute-force attack
- `src/quantum/` - Quantum cipher, oracle, and Grover search
- `src/experiments/` - Experimental evaluation
- `tests/` - Unit and integration tests
- `results/` - Experimental results and figures
- `docs/` - Project documentation and references

## Status

Project planning 

## Authors

- Marta Pomykała
- Zofia Mazur
