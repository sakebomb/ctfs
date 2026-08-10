# Next CTF Quick Guide

**When you participate in your next CTF, follow this workflow to organize it properly.**

## During the Competition

### 1. Create Competition Directory

```bash
cd ~/code/conferences/ctfs/[YEAR]
mkdir [event-name]
cd [event-name]
```

**Example:** `~/code/conferences/ctfs/2027/defcon-35-ctf`

### 2. Organize as You Go

**For simple writeups** (quick CTFs):
```
2027/other-ctf/
├── README.md (competition overview)
├── web/
│   ├── challenge-1.md
│   └── challenge-2.md
├── crypto/
│   └── challenge-3.md
└── misc/
    └── challenge-4.md
```

**For substantial projects** (agent-based, custom tooling):
```
2027/major-ctf/  (or create separate repo)
├── agents/
├── docs/
├── scripts/
└── README.md
```

### 3. Writeup Template

Use this for each challenge:

```markdown
# Challenge Name

**Category:** Web  
**Points:** 100  
**Difficulty:** Medium

## Challenge Description

[Paste challenge text or screenshot]

## Solution Approach

### Reconnaissance
- What you discovered first
- Enumeration steps

### Exploitation
1. Step-by-step process
2. Key insights
3. Payloads used

### Flag Extraction
- How you got the flag
- Final command/request

## Code/Tools Used

```python
# Minimal working exploit
```

## Key Lessons

- What technique this teaches
- Common pitfalls avoided
- Transferable patterns

## References

- Related CVE or technique documentation
- Tools used
```

## After the Competition

### 1. Decide: Standalone Repo or Portfolio Entry?

**Create standalone repo if:**
- Built custom agents/tools (>1000 lines of code)
- Placed in top 20
- Want to showcase specific skills (AI, reversing, etc.)
- Substantial documentation value

**Add to portfolio if:**
- Quick weekend CTF
- Simple writeups (no major tooling)
- Building breadth/volume

### 2. If Standalone Repo

```bash
# Copy publishing checklist
cp ~/code/conferences/defcon/halctf/CTF_PUBLISHING_CHECKLIST.md .

# Follow the checklist step-by-step
# (PII scan, documentation cleanup, security review, etc.)

# Publish to GitHub
git init
git add .
git commit -m "Initial commit: [CTF Name] - [Event] ([Ranking])"
git remote add origin https://github.com/sakebomb/[repo-name].git
git push -u origin main
```

### 3. Update CTF Portfolio

**Add entry to main README.md:**

```markdown
| 2027 | [Event Name] | Rank | Categories | [Link] | Status |
```

**Create summary file:**

```bash
# For standalone repo
cat > 2027/[event-name]/summary.md << EOF
# Event Name - Year

[Quick summary with link to full repo]
EOF

# For portfolio entry
# Files are already in 2027/[event-name]/ - just ensure README exists
```

**Update categories:**

Link challenges to category pages:

```markdown
# categories/web.md

### [Challenge Name] (Event - Year)
Brief description, technique, [link to writeup]
```

### 4. Update Lessons Learned

If you discovered new patterns, add to `lessons-learned.md`:

```markdown
### [New Pattern Name] (Event Year)

**Problem:** ...
**Solution:** ...
**Key Takeaway:** ...
```

### 5. Commit and Push

```bash
cd ~/code/conferences/ctfs
git add .
git commit -m "Add [Event Name] writeups and lessons"
git push origin main
```

## Quick Reference: File Locations

| What | Where |
|------|-------|
| Competition writeups | `~/code/conferences/ctfs/[YEAR]/[event]/` |
| Standalone projects | `~/code/conferences/[event]/` |
| HalCTF full repo | `~/code/conferences/defcon/halctf/` |
| Portfolio index | `~/code/conferences/ctfs/README.md` |
| Lessons learned | `~/code/conferences/ctfs/lessons-learned.md` |
| Publishing checklist | `~/code/conferences/defcon/halctf/CTF_PUBLISHING_CHECKLIST.md` |

## Publishing Decision Tree

```
New CTF Completed
    │
    ├─ Built substantial tooling (>1000 LOC)?
    │  ├─ Yes → Standalone repo + summary in portfolio
    │  └─ No  → Add directly to portfolio
    │
    ├─ Top 20 ranking?
    │  ├─ Yes → Standalone repo (showcase piece)
    │  └─ No  → Portfolio or standalone (your choice)
    │
    └─ Teaching value?
       ├─ High → Standalone repo with detailed writeups
       └─ Medium → Portfolio entry
```

## Tips

### During Competition
- **Document as you go** - Take screenshots, save payloads
- **Track failed attempts** - Failures are learning opportunities
- **Note time spent** - Helps estimate effort for writeups

### After Competition
- **Write while fresh** - Do writeups within 48 hours
- **Focus on technique** - Not just "here's the flag"
- **Be honest** - Document what didn't work and why
- **Link resources** - Reference tools, CVEs, blog posts

### Publishing
- **Check for secrets** - Even "expired" credentials should be rotated
- **Add security disclaimers** - For CTF-specific unsafe patterns
- **Professional styling** - No emojis, no all-caps filenames
- **Test build** - Verify Docker images build before publishing

## Example Timeline

**Weekend CTF (2 days):**
- Day 1-2: Compete, document as you go
- Day 3: Write final writeups (2-3 hours)
- Day 4: Publish to portfolio (30 minutes)

**Week-long CTF with tooling:**
- Week 1: Compete, build agents
- Week 2: Polish code, write docs (6-8 hours)
- Week 3: Publish standalone repo (3 hours with checklist)

## Maintenance

**Monthly:**
- Review open issues/questions on published repos
- Update dependencies if security alerts

**Quarterly:**
- Review lessons-learned.md, consolidate similar patterns
- Update portfolio README with stats
- Refresh category indexes

**Yearly:**
- Create new year directory: `mkdir ~/code/conferences/ctfs/[YEAR]`
- Archive old competition credentials
- Review and update publishing checklist

---

**Keep this guide handy!** Pin it or bookmark for quick access when starting your next CTF.

**Last Updated:** August 2026
