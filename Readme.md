# Simple 64-Bit Custom Hashing Algorithm: Code Report

## 1. Introduction
**Definition of Hashing:** Hashing is the process of taking input data (like a password or a file) of any size and converting it into a fixed-length string of text using a mathematical function. 
**Why we are using this:** This project demonstrates a custom 64-bit hashing algorithm built from scratch. It specifically incorporates four major cryptographic techniques: Substitution, Shifting, Rotation, and Permutation. 

## 2. Program Setup and Determinism
**What it is:** A hash algorithm must be "deterministic." This means for a specific input (like "Hello"), the output must always be exactly the same, every single time.
**How it is implemented in code:**
We fulfill this by starting the program with a fixed list of 8 hexadecimal bytes called an Initialization Vector (IV). 
```python
hash_state = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0]
```
Because we start from these exact numbers and never use random number generators (like time or random modules), the math will always calculate the exact same final result for the same input word.


## 3. The Core Hash Loop (The 4 Components)
The code takes the user's string, cuts it into 8-byte blocks, and loops over them, applying mathematical operations. 

### A) Substitution (Confusion)
**Definition:** In cryptography, substitution creates "confusion" by replacing input values dynamically so their relationship to the output becomes highly complex.
**Why we use it:** To hide the relationship between the original text and the hashed output, making it look incredibly messy and random instead of predictable.
**How it is implemented in code:** 
We loop through each byte and apply a non-linear algebraic equation: we multiply the byte by `31`, add `17`, and get the remainder modulo `256`.
```python
block[j] = (block[j] * 31 + 17) % 256
```

### B) Bit Shifting (Pre-Image Resistance)
**Definition:** Pre-image resistance requires a hash to act as a "One-Way Function"—you cannot reverse engineer it back to the original text. Bit shifting moves bits left or right, dropping the edge bits entirely out of existence.
**Why we use it:** Because bits are permanently destroyed by falling off the edge, it is mathematically impossible to reverse the calculation backward to find the original word. You physically lose the data required to reverse it.
**How it is implemented in code:**
We use a bitwise left shift (`<< 1`) mixed with `& 0xFF` (which limits it mathematically to an 8-bit size). The bits on the left edge are permanently lost and replaced with `0`s on the right.
```python
block[j] = (block[j] << 1) & 0xFF 
```

### C) Rotation (Circular Shift)
**Definition:** Rotation is similar to shifting, but instead of bits falling off the edge and being destroyed, they "wrap around" to the other side.
**Why we use it:** This creates the "Avalanche Effect," where changing a single tiny letter causes massive, drastic changes across the entire final hashed string.
**How it is implemented in code:**
We use Python's bitwise right-shift `>>` and bitwise left-shift `<<` combined with a bitwise OR `|` to create a circular rotation of 3 bits to the right. This safely relocates all the bits to different positions.
```python
block[j] = ((block[j] >> 3) | (block[j] << 5)) & 0xFF
```

### D) Permutation (Diffusion)
**Definition:** Permutation is the act of shuffling or physically changing the positions of the data bytes. 
**Why we use it:** It creates "Diffusion." A single small change in one spot of the original text spreads out and influences the entire resulting hash instead of just a localized spot.
**How it is implemented in code:**
To accomplish this, we completely swap and scramble the physical locations of our 8 bytes. For example, we put the 7th byte at the very front (index 0), the 0th byte in the second spot (index 1), and so on.
```python
block = [
    block[7], block[0], block[5], block[6], 
    block[3], block[2], block[1], block[4]
]
```
