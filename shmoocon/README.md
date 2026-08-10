# Shmoocon

Shmoocon was an annual hacker conference in Washington, D.C. (2005–2025). Its badge/poster
puzzles and the Battelle-run **Chrononaut** CTF were highlights. 2025 was the final Shmoocon.

## Writeups

| Year | Track | Highlights | Status |
|------|-------|-----------|--------|
| [2025](./2025/writeup.md) | Crypto College badge | Z-delimited header solved; italic-stego body reads `KEEP…` reversed (OCR-limited) | Partial |
| [2024](./2024/writeup.md) | Battelle Chrononaut CTF, Badge, Shmooganography | Badge Caesar puzzle & multiple `battelle{}` flags solved | Solved (core) |
| 2022 | — | artifacts only (`shmoocon2022.pdf`, cert chain) | Artifacts |

## Notable solves

- **2024 Badge — "Get in the Zone"** — six per-line Caesar ciphers re-ordered by UTC offset into
  a single instruction. Fully worked in [2024/writeup.md](./2024/writeup.md).
- **2024 Chrononaut "Old Note"** — substitution cipher cracked via the `battelle{}` flag-wrapper
  crib → `battelle{eyec4me_eyesaw_ic0nqu3red}`.
- **2024 Chrononaut "XOR me a Question"** — repeating-key XOR, key `titor` (John Titor) →
  `battelle{gravity_distortion_time_displacement_unit}`.
- **2024 Chrononaut "Multiversal Product Code"** — 3D-printed cube whose 6 faces are each a Data
  Matrix; voxelized and decoded all six to URL-shortener slugs.
- **2025 Crypto College** — `Z`-delimited header decodes to the portal URL; italic-letter stego
  body reads `KEEP…` reversed (full decode OCR-limited).

## Source

Working notes are reproduced from personal notes taken during each event. Large challenge
binaries (Chrononaut executables, punch-card images) are archived privately and are not included
in this repo.
