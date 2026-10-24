#!/usr/bin/env python3
"""
Refresh the live figures in the CAPS white paper, regenerate every format, and
deploy.

The paper states its numbers (height, supply, difficulty, hashrate, peers) and
stamps itself "last verified at height N". Those drift continuously, so this
re-reads them from the node and rewrites only those values, then rebuilds the
.txt and the HTML page from the markdown so all three formats stay in sync.

Safety: if the node is unreachable or returns something implausible, it exits
without touching anything — a stale paper is better than one that publishes
zeros. Deploy only happens if the numbers actually changed.

Run:  refresh_stats.py [--dry-run] [--no-deploy]
"""
import json, re, subprocess, sys, io, os, datetime, textwrap, urllib.request

CLI       = "/root/caps-core/src/caps-cli"
DATADIR   = "/root/.caps"
REPO      = "/mnt/f/GitHub/caps-site/whitepaper"
HERE      = os.path.dirname(os.path.abspath(__file__))
POOL_API  = "https://asicpool.space/api/pools/caps"
VPS       = "vpsproxy"
WEBROOT   = "/var/www/caps-core/whitepaper"
PREMINE   = 470_000
MAX_SUPPLY = 21_000_000
S19_HPS   = 100e12            # a representative modern SHA-256 ASIC
EXPECTED_FIELDS = 17          # every tracked figure must be found (see main())

DRY  = "--dry-run" in sys.argv
NODEPLOY = "--no-deploy" in sys.argv or DRY


def rpc(method, *args):
    out = subprocess.run([CLI, f"-datadir={DATADIR}", method, *map(str, args)],
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise RuntimeError(f"{method} failed: {out.stderr.strip()[:200]}")
    t = out.stdout.strip()
    try:
        return json.loads(t)
    except Exception:
        return t


def collect():
    height = int(rpc("getblockcount"))
    chain  = rpc("getblockchaininfo")
    net    = rpc("getnetworkinfo")
    utxo   = rpc("gettxoutsetinfo")
    supply = float(utxo["total_amount"])
    diff   = float(chain["difficulty"])
    peers  = int(net["connections"])
    # network hashrate: prefer the pool's figure, fall back to difficulty math
    try:
        with urllib.request.urlopen(POOL_API, timeout=15) as r:
            hps = float(json.load(r)["stats"]["networkHashrate"])
    except Exception:
        hps = diff * 2**32 / 300.0
    return dict(height=height, supply=supply, diff=diff, peers=peers, hps=hps)


def sane(s):
    """Refuse to publish obviously broken readings."""
    if s["height"] < 1 or s["supply"] <= PREMINE or s["diff"] <= 0 or s["hps"] <= 0:
        return False
    # supply must equal premine + 50/block (allow fees/rounding slack)
    expected = PREMINE + 50 * (s["height"] - 1)
    return abs(s["supply"] - expected) < max(1000, expected * 0.02)


def fmt_hashrate(h):
    for unit, d in (("TH/s", 1e12), ("GH/s", 1e9), ("MH/s", 1e6), ("kH/s", 1e3)):
        if h >= d:
            v = h / d
            return f"{v:.0f} {unit}" if v >= 10 else f"{v:.1f} {unit}"
    return f"{h:.0f} H/s"


def apply(md, s):
    H   = f"{s['height']:,}"
    SUP = f"{s['supply']:,.0f}"
    PCT = f"{PREMINE / s['supply'] * 100:.1f}"
    MAXPCT = f"{PREMINE / MAX_SUPPLY * 100:.2f}"
    HR  = fmt_hashrate(s["hps"])
    MULT = f"{S19_HPS / s['hps'] / 1e6:.1f} million"
    DATE = datetime.date.today().strftime("%-d %B %Y") if os.name != "nt" else \
           datetime.date.today().strftime("%d %B %Y").lstrip("0")

    subs = [
        # header + footer stamps
        (r"Last verified at \*\*block height [\d,]+\*\*, .*?\.",
         f"Last verified at **block height {H}**, {DATE}."),
        (r"verified at block\s+height [\d,]+ on .*? and will drift",
         f"verified at block height {H} on {DATE} and will drift"),
        # abstract
        (r"about \*\*[\d.]+% of all coins currently in existence\*\*",
         f"about **{PCT}% of all coins currently in existence**"),
        (r"only ~[\d.]+% of the eventual 21,000,000 maximum",
         f"only ~{MAXPCT}% of the eventual 21,000,000 maximum"),
        (r"roughly [\d.]+ [kMGT]H/s, essentially all of it",
         f"roughly {HR}, essentially all of it"),
        # section 4.1
        (r"At height [\d,]+, total supply is \*\*[\d,]+ CAPS\*\*",
         f"At height {H}, total supply is **{SUP} CAPS**"),
        (r"- \*\*≈ [\d.]+% of all CAPS that currently exist\*\*",
         f"- **≈ {PCT}% of all CAPS that currently exist**"),
        (r"- \*\*≈ [\d.]+% of the 21,000,000 eventual maximum\*\*",
         f"- **≈ {MAXPCT}% of the 21,000,000 eventual maximum**"),
        (r"The chain is young — [\d,]+ blocks —",
         f"The chain is young — {H} blocks —"),
        # section 6 table
        (r"Measured at height [\d,]+, .*?:", f"Measured at height {H}, {DATE}:"),
        (r"\| Block height \| [\d,]+ \|", f"| Block height | {H} |"),
        (r"\| Total supply \| [\d,]+ CAPS \|", f"| Total supply | {SUP} CAPS |"),
        (r"\| Difficulty \| ~[\d.]+ \|", f"| Difficulty | ~{s['diff']:.2f} |"),
        (r"\| Network hashrate \| ~[\d.]+ [kMGT]H/s \|",
         f"| Network hashrate | ~{HR} |"),
        (r"\| Reachable peers \(seed node\) \| \d+ \|",
         f"| Reachable peers (seed node) | {s['peers']} |"),
        # section 7.1
        (r"CAPS network hashrate is approximately \*\*[\d.]+ [kMGT]H/s\*\*",
         f"CAPS network hashrate is approximately **{HR}**"),
        (r"is roughly \*\*[\d.]+ million\s+times\*\* the entire CAPS network",
         f"is roughly **{MULT} times** the entire CAPS network"),
    ]
    # The markdown is hand-wrapped, and re-wrapping can move a line break into
    # the middle of any of these phrases. Match any whitespace (including a
    # newline) wherever a pattern has a literal space, so a reflow can never
    # silently stop a field from updating.
    changed = 0
    for pat, rep in subs:
        md, n = re.subn(pat.replace(" ", r"\s+"), rep, md, flags=re.S)
        changed += n
    return rewrap(md), changed


WRAP = 78

def rewrap(md):
    """Some substitutions span wrapped lines and collapse them into one long
    line. Re-wrap only the prose paragraphs that ended up over-long, leaving
    code blocks, tables, headings and lists exactly as they were — otherwise
    the .md (which readers download) degrades into unwrapped walls of text."""
    out, fence = [], False
    for block in md.split("\n\n"):
        if block.strip().startswith("```") or fence:
            if block.count("```") % 2:
                fence = not fence
            out.append(block); continue
        lines = block.split("\n")
        prose = (lines and not any(l.lstrip().startswith(("|", "#", ">", "- ", "* ", "```"))
                                   or re.match(r"^\s*\d+\.\s", l) or l.startswith("    ")
                                   for l in lines))
        if prose and any(len(l) > WRAP for l in lines):
            out.append(textwrap.fill(" ".join(l.strip() for l in lines), width=WRAP,
                                     break_long_words=False, break_on_hyphens=False))
        else:
            out.append(block)
    return "\n\n".join(out)


def main():
    try:
        s = collect()
    except Exception as e:
        print(f"[refresh] node unreachable ({e}); leaving the paper untouched", flush=True)
        return 0
    if not sane(s):
        print(f"[refresh] implausible readings {s}; refusing to publish", flush=True)
        return 1

    src = os.path.join(REPO, "CAPS_whitepaper_v1.0.md")
    before = io.open(src, encoding="utf-8").read()
    after, hits = apply(before, s)

    # Every field must still be found. If an edit to the paper reworded one of
    # the tracked phrases, that number would silently freeze while the rest kept
    # updating — a stale figure in a document whose whole point is accuracy.
    if hits < EXPECTED_FIELDS:
        print(f"[refresh] only {hits}/{EXPECTED_FIELDS} fields matched — the paper's "
              f"wording probably changed. Fix the patterns in apply(); NOT publishing.",
              file=sys.stderr, flush=True)
        return 1
    print(f"[refresh] height={s['height']} supply={s['supply']:,.0f} "
          f"diff={s['diff']:.2f} hps={fmt_hashrate(s['hps'])} peers={s['peers']} "
          f"({hits} fields matched)", flush=True)

    if after == before:
        print("[refresh] no change", flush=True); return 0
    if DRY:
        print("[refresh] dry run — not writing", flush=True); return 0

    io.open(src, "w", encoding="utf-8").write(after)
    # rebuild the other two formats from the markdown
    txt = os.path.join(REPO, "CAPS_whitepaper_v1.0.txt")
    htm = os.path.join(REPO, "index.html")
    subprocess.run([sys.executable, os.path.join(HERE, "md2txt.py"), src, txt], check=True)
    t = io.open(txt, encoding="utf-8", newline="").read().replace("**", "")
    io.open(txt, "w", encoding="utf-8", newline="").write(t)
    subprocess.run([sys.executable, os.path.join(HERE, "md2html.py"), src, htm], check=True)

    if os.path.getsize(htm) < 15000 or os.path.getsize(txt) < 10000:
        print("[refresh] regenerated files look truncated; NOT deploying", flush=True)
        return 1
    if NODEPLOY:
        print("[refresh] built, deploy skipped", flush=True); return 0

    subprocess.run(["scp", "-q", "-o", "BatchMode=yes", src, txt, htm, f"{VPS}:/tmp/"], check=True)
    subprocess.run(["ssh", "-o", "BatchMode=yes", VPS, "bash", "-s"], check=True, text=True,
        input=f"""set -e
sudo -n cp /tmp/CAPS_whitepaper_v1.0.md /tmp/CAPS_whitepaper_v1.0.txt /tmp/index.html {WEBROOT}/
sudo -n chown www-data:www-data {WEBROOT}/*
sudo -n chmod 644 {WEBROOT}/*
""")
    print("[refresh] deployed", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
