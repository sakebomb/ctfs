# Shmoocon 2024 — Battelle / Chrononaut CTF & Puzzles

> **Event:** Shmoocon 2024 (Washington, D.C., Jan 2024)
> **Tracks covered here:** the **Battelle "Chrononaut"** jeopardy CTF (`chrononaut.xyz`), the
> **Shmoocon Badge** puzzle, and the **Shmooganography** poster/AR hunt.
> **Notes source:** personal notes, reproduced here. Challenge binaries are archived privately
> and not included in this repo.
> **Flag format:** `battelle{...}`

---

## Badge Puzzle — "Get in the Zone" (SOLVED)

The badge presented six lines, each prefixed with a **time-zone abbreviation** and a
Caesar-shifted message. The trick has two layers:

1. **Each line is a Caesar cipher with a different shift.**
2. **The lines must be re-ordered by the time zone's UTC offset**, not the order printed.

Solving every line (brute the shift, keep the readable English):

| TZ | Offset | Ciphertext | Shift | Plaintext |
|------|--------|--------------------|:-----:|--------------------|
| EST | −5 | `LZW VASDK STGMFV` | 8 | **THE DIALS ABOUND** |
| NT | −3:30 | `PMSLB YLB PMSLB` | 2 | **ROUND AND ROUND** |
| GMT | +0 | `ZBER GUNA GVZR` | 13 | **MORE THAN TIME** |
| JST | +9 | `XLMW TEVEHMKQ` | 22 | **THIS PARADIGM** |
| AEST | +10 | `VHDUFK WKH JOREH` | 23 | **SEARCH THE GLOBE** |
| NZEST | +12 | `UP GJOE PSEFS` | 25 | **TO FIND ORDER** |

Read in offset order the messages chain into an instruction:

> *the dials abound → round and round → more than time → this paradigm → search the globe → to find order*

i.e. the badge is a **globe/clock dial** puzzle — spin the dials (time zones) "round and round"
to reveal the next stage. The reusable one-liner:

```python
def caesar(s, k):
    return ''.join(chr((ord(c)-65+k)%26+65) if c.isalpha() else c for c in s.upper())
# brute k in range(26), keep the line containing a common English word
```

> **Hint progression (from the badge):** "start with the badges to end up here next year",
> "Time is of the essence, so get in the Zone", "Stage 2: use the lessons from Stage 1".

---

## Shmooganography — poster / NFC / geo hunt

A multi-stage OSINT + stego hunt starting at `shmooganography.org/Welcome`.
(*The cipher printed at the top of the poster is a movie prop — a deliberate red herring.*)

**Stage 1 — the poster (`images/2024011217*.png`).** Five poster panels each carry a
20×4 grid of letters (below). The hint — *"Scan the poster with your eyes, but you may see more
when you get nearer"* — points to reading the columns / physical alignment up close.

```
IGIPPQMU SUSYEXEP BPTNKZDF ZLMGQDSY ZCXSGBDL
NALYODEH SSKRIPOE QREFAWFQ NLTJMAKY YGLIRWAF
PXHBEKYD SLQROJMH PZQREKQE IUITULPW LMBAXHHC
ZGSTOHBR DRJGLJIR WUGWTGDQ PRDEOAUU JOYXPOJG
```

**Stage 2 — geolocation.** Hint: *"latitude, longitude, and zoom may point you to a real
destination — unreal (out-of-range) values take you where you really want to be."* The decoded
coordinates are intentionally **invalid** map values; plugging the impossible lat/long/zoom into
the map viewer reveals the hidden target.

**NFC medallion.** The badge medallion carried three NFC tags. Tag 3 (NTAG215) decodes an NDEF
text record:

```
A048 0000 E110 3E0F 030D D101 0954 0265 6E6D 7573 6575 6DFE
                                  └ 65 6E6D 7573 6575 6D → "enmuseum"
```

Tag 1 payload: `en16/19364/24522`. Together these route to the museum destination for the hunt.

Related side-quests referenced on the posters: **Chill Out** village, **Radio Frequency CTF**,
**Hack Fortress**, and a **BOF** challenge (see the Chrononaut buffer-overflow below).

---

## Chrononaut CTF (`chrononaut.xyz`) — challenge log

A time-travel-themed jeopardy board run by the Battelle team. Captured challenges:

### Old Note — 50 (SOLVED, substitution cipher)

> *The worn parchment bears the mark of a distinguished leader…*

Ciphertext `yxqqbiib{bvbz4jb-bvbpxt_bz0knrzoba}` is a **monoalphabetic substitution** whose key is
seeded by the flag wrapper: `yxqqbiib` → `battelle`. Applying the same mapping:

**Flag:** `battelle{eyec4me_eyesaw_ic0nqu3red}` ("I came, I saw, I conquered" — Caesar/leader theme).

### Grandpa's First App — 100 (`grandpas_program.zip`, `nc jump.chrononaut.xyz 5002`)

*"SON, BACK IN MY DAY WE HAD PUNCH CARDS."* The archive is a folder of numbered images
(`0.png`–`35.png`) representing **punch cards** — decode the card columns to
Hollerith/EBCDIC characters to recover the input the remote service expects.

### New Recruit's Overflow — 100 & buffer-overflow work (`nc jump.chrononaut.xyz 5001`)

Classic **stack buffer overflow / ret2shellcode**. Working notes show the standard workflow:

1. `cyclic -n 8 500` → feed into the target under gdb → read the fault address `8000003FF766`
2. `cyclic -l 8000003FF766` → recover the offset to saved RIP
3. Pad + return into a 24-byte execve(`/bin/sh`) shellcode stub (also a `/dev/tty` dup2 stub)

Candidate gadget/return addresses noted: `0x4011df`, `0x401269`, `0x40126a`.

### XOR me a Question — 100 (SOLVED, repeating-key XOR)

> *A perplexing SMS arrives, filled with cryptic symbols from a time traveler.*

The provided `message.bin` (2,535 bytes) is **repeating-key XOR**. Solve without any crib:

1. **Key-length detection** — normalized Hamming distance across blocks minimizes at **20**.
2. **Per-column single-byte solve** — score each column by English-letter frequency.

The recovered key is `titortitortitortitor` — i.e. the repeating word **`titor`**, a nod to
[John Titor](https://en.wikipedia.org/wiki/John_Titor), the famous "time traveler" hoax. Fittingly,
the plaintext *is* Titor's 2036 message ("I remember 2036 very clearly…"), ending in the flag:

```python
data = open("message.bin","rb").read()
key  = b"titor"
dec  = bytes(data[i] ^ key[i % 5] for i in range(len(data)))
# → "...The vice president is the president of the senate...
#    battelle{gravity_distortion_time_displacement_unit}"
```

**Flag:** `battelle{gravity_distortion_time_displacement_unit}`

### Multiversal Product Code — 200 (SOLVED mechanic, 3D Data-Matrix cube)

> *…the geeks can't figure it out, but they scanned it so they made that part easy on you.*

`multiversal.tar` contains two OpenSCAD-exported STL meshes, `black.stl` and `white.stl`. Their
volumes (2,715 + 3,117) sum to exactly **5,832 = 18³** — the two parts *perfectly partition* an
18×18×18 voxel cube. So `white = NOT black`; voxelizing just the black mesh gives the full pattern.

Voxelizing (point-in-mesh test on each cell center via `trimesh`, 2,715 cells = exact match) and
reading each of the **6 outer faces**, every face is a valid **Data Matrix** barcode (the solid
L-finder + alternating clock-track borders confirm it). Decoded with `zxing-cpp`:

| Face | Data Matrix payload |
|------|---------------------|
| −X | `/4NPtxDk` |
| +X | `/NIRi3cb` |
| −Y | `/4FEUAvw` |
| +Y | `/ul1FOtp` |
| −Z | `/MGUy4E3` |
| +Z | `/7EsSRlG` |

Each face is a 7-char base64 slug prefixed with `/` — i.e. **six URL-shortener paths** (the
"product code" being scannable from every dimension = "multiversal"). Resolving the slugs required
the 2024 live infrastructure, so the final flag wasn't recoverable offline — but the full
mechanic (partition → voxelize → per-face Data Matrix → slugs) is solved.

*Reproduction:* `trimesh` + `zxing-cpp` in a throwaway venv; see the repo's tooling notes.

### riscV Business — 100 (Hardware, *requires Badge*)

RISC-V hardware challenge gated behind the physical badge; flag submitted as `battelle{}`.

### Other challenges captured (setup documented)

| Challenge | Pts | Type | Files / entry | Intended approach |
|-----------|-----|------|---------------|-------------------|
| Pair of Secrets | 200 | crypto | `public1/2.pem`, `encrypted1/2.bin` | **RSA common-modulus / shared-factor** — two pubkeys "used to encrypt instead of private"; `gcd(n1,n2)` or common-modulus attack |
| Timeline Simulation | 300 | rev/misc | `timeline_simulator.tar` | Find the one valid PRNG **seed** that wins |
| UGC Highlander | 100 | misc | `magma_moutain.bsp.zip` | Extract secrets from a **TF2 `.bsp` map** file |
| I CAN't see | 300 | ICS/auto | `can_data.zip` | Decode a **CAN bus** capture into a message |
| Time Jump Planner | 400 | pwn | `jump_planner_release.tar`, `nc :5000` | Bypass the anti-exploit **wrapper** around a known-vuln tool |

---

## Techniques & lessons

- **Multi-shift Caesar keyed by metadata** — the badge's shifts weren't fixed; the *time-zone
  offset* both ordered the lines and hinted the theme. When a puzzle labels each line with data,
  that label usually *is* a parameter.
- **Flag-wrapper as cipher crib** — `yxqqbiib` = `battelle` instantly gave 8 substitution pairs,
  enough to unwrap the whole "Old Note" flag.
- **Read the provided scaffolding** — the pwn notes show cyclic→offset→shellcode is the intended
  path; the challenge is execution, not discovery.

## Artifacts in this folder

- `Badge.md`, `Chrononaut.md`, `Shmooganography 24.md` — original working notes
- `images/` — poster panels, badge/medallion, and side-quest photos referenced above
- `shmoocon2024-chain.crt` — conference Wi-Fi/cert artifact
