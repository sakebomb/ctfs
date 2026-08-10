# Hackfortress 2023

> **Event:** Hackfortress (Cyphercon / Shmoocon era, artifacts dated Jan 2023)
> **Format:** 3 timed rounds, TF2-style attack/defense mashup with a shared scoreboard.
> **Challenge files:** archived privately; not included in this repo.
> **Status:** Round 1 solved end-to-end; Rounds 2–3 documented with setup + intended approach.

## Overview

Hackfortress bundles a grab-bag of short forensics / crypto / rev challenges delivered per
round. The files are a mix of **the challenge prompt** (README, hash to crack, wordlist) and
**candidate artifacts** (pcaps, ELF binaries, LUKS containers, a stego JPEG). Each round shares
the same React scoreboard dump (`Scoreboard.html` + `Scoreboard_files/`), which is just the UI,
not a challenge.

## Round 1 — SOLVED

### Custom hash crack (`hash_to_crack.txt`, `wordlist-salt.txt`, `README.md`)

The README specifies a bespoke hashing scheme:

1. For each char of the password, XOR its byte with the salt byte
2. Pack each XORed value as a **big-endian 4-byte signed int** (`struct.pack(">i", ...)`)
3. Concatenate, `sha1(...)`, then `base64` the digest

Target: `5ndTv/DlsISN09HVZcHk5QuL4AU=`
Wordlist: `wordlist-salt.txt` (7,776 `plaintext:salt` lines).

**Solve** — brute the wordlist through the documented scheme:

```python
import hashlib, base64, struct
target = "5ndTv/DlsISN09HVZcHk5QuL4AU="
for line in open("wordlist-salt.txt"):
    pw, salt = line.rstrip("\n").rsplit(":", 1)
    s = ord(salt)
    buf = b"".join(struct.pack(">i", b ^ s) for b in pw.encode())
    if base64.b64encode(hashlib.sha1(buf).digest()).decode() == target:
        print(pw, salt); break
```

**Answer:** password `tidal`, salt `P`.

### `honeystrings.file` (ELF, not stripped)

Pure `strings` challenge — the flag is embedded in plaintext:

```
$ strings honeystrings.file | grep -i flag
the flag is c0ngR@tz_sTr1nGz
```

**Answer:** `c0ngR@tz_sTr1nGz`

### `whatisthisv1.file` (squashfs)

`file` reports a SquashFS v4 image. Mount/extract and read the answer:

```
$ unsquashfs -d out whatisthisv1.file
$ cat out/answer.txt          # 6558d9f0b5717795bca63a93cce59883
                              # (notanswer1..5.txt are decoys)
```

**Answer:** `6558d9f0b5717795bca63a93cce59883`

### `whereisthefile` / `whereisthefile1` (pcap)

HTTP capture of a `GET /win.jpg` transfer (Python `SimpleHTTP` server). Carve the transferred
JPEG out of the stream (Wireshark → Export Objects → HTTP, or `tcpflow`) and inspect its EXIF /
content. The image is a Canon EOS photo with a full Adobe XMP block; the answer lives in the
carved file's metadata/pixels. `hash_to_crack.txt` also lists scanner IPs
(`125.63.27.153`, …) that correlate with the `access.log` recon noise.

### `logslogslogs.tar.gz` + `access.log`

Nginx-style access log full of opportunistic scanner traffic (`.env` probes, ThinkPHP RCE,
phpMyAdmin path sweeps, `masscan` UA). Log-analysis question — identify the attacker IP /
successful request pattern from the noise.

## Round 2 — setup + approach

| File | What it is | Intended path |
|------|-----------|---------------|
| `maybeakey` | PEM **RSA private key** | Key material for a later decrypt / SSH / signature step |
| `whatisthisv2` | **LUKS2** container (aes, sha256, key_size 64) | Unlock with a recovered passphrase, then mount |
| `the_darkness.file` | ELF (not stripped) | Reverse for a comparison / password check |
| `sud-1.elf` | ELF (stripped) | Reverse; likely a crackme |
| `earth.jpg` / `earth.zip` | JPEG (zip just wraps it) | Stego — no plaintext flag in `strings`, so LSB / appended-data / steghide |
| `cloudtrail.json` + `cloudtrail.py` | AWS CloudTrail log + starter filter | Find the malicious API call; the `.py` filters `apigateway.amazonaws.com` `AwsApiCall` events |

**Approach:** the CloudTrail task is a log-triage question (run/extend `cloudtrail.py` to isolate the
anomalous event). `earth.jpg` is stego (nothing in `strings`; try `steghide`, `zsteg`, appended
archive). `maybeakey` (RSA) plus the LUKS2 container suggests a chained decrypt.

## Round 3 — setup + approach

| File | What it is | Intended path |
|------|-----------|---------------|
| `whatisthisv3.file` | **LUKS1** container (aes-xts-plain64, 251k iters) | Brute the passphrase |
| `bruteforce-luks/` | Compiled `bruteforce-luks` tool (source + binary) | The provided cracker |
| `rockyou/rockyou.txt` | Full rockyou wordlist (14.3M lines) | Dictionary for the LUKS brute |
| `shellcode3.zip` | Java Meterpreter stager (`Payload.class`, `metasploit.dat`) | Reverse the payload |
| `metasploit.dat` | Config | Reveals **LHOST=172.16.11.10, LPORT=443** |
| `oss_security_fresh.pcapng` | pcapng capture | Network forensics — trace the C2 / exploit traffic |
| `cloudtrail.json` + `cloudtrail.py` | CloudTrail again | Log triage |

**Approach:** the intended round-3 crypto solve is explicit — run the bundled `bruteforce-luks`
against `whatisthisv3.file` with `rockyou.txt`:

```
$ ./bruteforce-luks/bruteforce-luks -f rockyou/rockyou.txt -t 4 whatisthisv3.file
```

The Java payload + pcapng pair is a network-forensics question: the payload config gives the C2
endpoint (`172.16.11.10:443`), which you then locate in `oss_security_fresh.pcapng`.

## Techniques that transferred

- **`file` first, always** — squashfs, LUKS1 vs LUKS2, ELF stripped/not all fell out of `file`.
- **`strings | grep -i flag`** solved an entire challenge (honeystrings) in one line.
- **Read the provided starter code** — `cloudtrail.py` and `bruteforce-luks` *are* the intended
  tooling; the challenge is using them, not rebuilding them.
- **Decoys are labeled** (`notanswer1..5.txt`) — trust the odd-one-out (`answer.txt`).

## Lessons Learned

- Round 1's custom-hash task is a clean example of "implement the spec exactly" — the big-endian
  **signed** int pack (`>i`, 4 bytes/char) is the only subtlety; `>I` or 1-byte packing fails.
- For LUKS bruting, use the container's own iteration count as a time estimate before launching
  rockyou — LUKS1 @ 251k iters is slow per guess.
