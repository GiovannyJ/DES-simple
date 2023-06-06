# What is DES

DES (Digital Encryption Standard) is a symmetric form of encryption adopted that was adopted in 1977 and retired in 2005. It was used by government agencies as a way to protect sensitive data. It has since been retired due to modern computing power being strong enough to brute force the 56bit key length in reasonable time. 

---

# Normal DES
| Rounds | Key Length | Sub-key Length | Input Length | S-box Length | Output Length |
|--------|------------|----------------|--------------|--------------|---------------|
| 16     | 56-bits    | 48-bits        | 64-bits      | 6-bit input -> 4-bit output | 64 bits       |

---

# Simple DES
| Rounds | Key Length | Sub-key Length | Input Length | S-box Length | Output Length |
|--------|------------|----------------|--------------|--------------|---------------|
| 5      | 9-bits     | 8-bits         | 12-bits      | 4-bit input -> 3-bit output | 12 bits       |
