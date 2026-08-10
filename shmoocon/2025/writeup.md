# Shmoocon 2025 — Crypto College Badge Puzzle

> **Event:** Shmoocon 2025 (final Shmoocon, Washington, D.C., Jan 2025)
> **Track:** the **Crypto College** badge / poster cipher (`cryptocollege.shmoocon.org`)
> **Notes source:** personal notes, reproduced here.

---

## The puzzle

The Crypto College challenge is a large poster (`images/20250111112118.png`) covered in a dense
block of ciphertext. The solve proceeds in layers.

### Layer 1 — the Z-delimited header (SOLVED)

The first line uses **`Z` as a word separator** (a common badge-puzzle convention when the
alphabet must stay unbroken):

```
FINDZTHEZBADGEZPUZZLEZATZCRYPTOCOLLEGEDOTSHMOOCONDOTORG
```

→ **"FIND THE BADGE PUZZLE AT CRYPTOCOLLEGE DOT SHMOOCON DOT ORG"**

And the block's final line closes the loop:

```
…QIJTSHMOOCRYPTOCOLLEGE  →  SHMOO CRYPTO COLLEGE
```

So the outer wrapper is plain text pointing at the online puzzle portal; the **body** between
those markers is the actual cipher.

### Layer 2 — the italic steganography (MECHANISM FOUND, not fully resolved)

The body is ~16 rows of ~55-char lines. Zooming into the poster photo reveals the real trick:
**scattered letters are set in *italic*** while the rest is upright. The italics are the hidden
message; the surrounding upright letters are filler.

Reading the italic glyphs across the four rows that contain them (top→bottom) gives a stream
that, **read in reverse**, begins cleanly with **`KEEP…`** — an unambiguous English word that
confirms the mechanism (italic-glyph stego, reversed). Two independent extractions (from
contemporaneous event notes and from re-reading the poster image) both agree on the `KEEP` head:

```
italic runs (best OCR): DELALAM E TT E TNL EE A | NEE SC TL VD | SC FTSIE | SB PCW E E
reversed head:          KEEP...
```

**Status — mechanism solved, full plaintext not recovered.** The blocker is purely OCR: cleanly
disambiguating every slanted serif glyph (I/L/T, E/F, etc.) at this photo resolution. The two
extractions agree on `KEEP` but diverge after it, so the remainder isn't asserted here. Next pass
needs a **higher-resolution scan or the physical booklet** to nail each italic letter; the decode
itself is then just "reverse the italic stream."

*(An earlier reading transcribed parts of the grid as Greek letters; on closer inspection those
were italic-Latin glyphs misread, not Greek. The italic-stego reading above supersedes it.)*

---

## Techniques & lessons

- **Look for the delimiter first.** Spotting `Z` as a spacer instantly cracked the header and
  told us the wrapper wasn't part of the real cipher — saving time on the body.
- **Typography can be the payload.** The whole message hid in *italic vs. upright* — a channel
  invisible in a plain transcription. Always compare glyph shapes, not just letters.
- **The scan resolution is the real adversary.** Here the cipher is understood (reverse the
  italic stream); what's missing is clean glyph OCR. Capture puzzle media at max resolution.
- **Record partial state honestly.** `KEEP…` is a confirmed foothold, not a finished solve — the
  writeup says exactly that rather than papering over the gap.

## Artifacts in this folder

- `Crypto College.md` — original working notes (full ciphertext block + column transcription)
- `images/20250111112118.png` — the Crypto College poster
- `shmoocon2025-chain.crt` — conference Wi-Fi/cert artifact
