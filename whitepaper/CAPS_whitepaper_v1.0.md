# CAPS — A Wasteland Community Currency

**White paper · version 1.0**
Last verified at **block height 649**, 24 October 2026.

Website: caps-core.undergroundroots.ca · Explorer: caps.undergroundroots.ca
Wallet: wallet.undergroundroots.ca · Source: github.com/ShaeOJ/caps-core

---

## Abstract

CAPS is a small SHA-256d proof-of-work cryptocurrency with a post-apocalyptic
bottle-cap theme. It exists so that an ordinary person can run an entire
crypto stack end to end — mine a block, run a full node, read an explorer, and
hold their own keys — on a chain small enough to actually understand.

CAPS is **not an investment**, has no market, and makes no promises about
price. Two facts are stated here rather than buried: block 1 contains a
**470,000 CAPS premine**, which is about **93.6% of all coins currently in
existence** (though only ~2.24% of the eventual 21,000,000 maximum); and the
network is currently **tiny and centralised** — roughly 23 MH/s, essentially
all of it from one operator. A single modern ASIC is millions of times that
hashrate. Anyone evaluating CAPS should read Section 7 before anything else.

---

## 1. Why CAPS exists

Most coins ask you to buy them. CAPS asks you to run one.

Learning how a blockchain actually works is harder than it should be. On large
chains you will never find a block, running a node is a spectator sport, and
the tooling hides the mechanics behind an exchange account. The useful parts —
the parts that teach you something — are only visible at small scale.

CAPS is deliberately small. A hobby ASIC, or even a CPU, can find blocks. A
full node syncs in seconds. The pool, explorer and wallet are all open source
and documented. Nothing requires permission from anyone.

Three pillars:

1. **A themed collectible.** A wasteland bottle-cap currency with its own art
   and lore — something to earn, hold and trade for the fun of it.
2. **Learn the whole stack.** Mine → run a node → explore → self-custody, with
   no gatekeeping and no step you have to take on trust.
3. **A community currency.** Tips, prizes and perks inside the undergroundroots
   community. Value from being used, not from hype.

---

## 2. What CAPS is not

Stated plainly, because it is easier to be clear now than to be misunderstood
later:

- **Not an investment, and not offered as one.** No returns, no yield, no
  price target, no expectation of profit from anyone else's effort.
- **Not a security.** There is no issuance sale, no presale, no ICO.
- **Not a store of value.** See Section 7: the chain's proof-of-work security
  is negligible in absolute terms.
- **No market.** There is no exchange listing, no market maker, and none is
  promised.
- **No treasury or foundation.** Nobody is raising money against this.

If you are looking for an asset that goes up, this is the wrong document.

---

## 3. Design and consensus

CAPS is a fork of Bitcoin Silver, itself derived from Bitcoin Core (v24/25
era). The large majority of the codebase is unmodified upstream Bitcoin, which
is a deliberate choice: the consensus-critical code is the part you least want
a hobbyist rewriting. Changes are confined to chain parameters, the difficulty
algorithm, and branding.

### 3.1 Proof of work

CAPS uses **SHA-256d** (double SHA-256) — the same proof-of-work function as
Bitcoin. This makes CAPS mineable with ordinary SHA-256 ASIC hardware that
people already own, which is the point: the barrier to participation is a
miner you may already have in a cupboard. It also means CAPS shares a hash
function with chains that have astronomically more hashrate, with the
consequences described in Section 7.

### 3.2 Difficulty: LWMA

Block interval targets **5 minutes (300 seconds)**.

Rather than Bitcoin's 2016-block retarget, CAPS uses **LWMA** (Linearly
Weighted Moving Average) with a window of **N = 96 blocks**, recalculated
every block, with solve times clamped at 20× the target.

The reasoning is practical. On a small network, hashrate arrives and leaves in
large relative bursts — one miner connecting can multiply the network's
capacity. Under Bitcoin's retarget, a big miner leaving would strand the chain
at a difficulty nobody could meet, potentially for days. A per-block weighted
average tracks hashrate closely enough to keep blocks flowing.

This behaves as intended in practice: when CAPS first passed the N=96 window,
difficulty ramped by roughly 67× to match the hashrate that had arrived.

As a backstop, if no block is found for **60 minutes** (12× the target
spacing), difficulty resets to the minimum so that any miner can recover the
chain.

### 3.3 Addresses

- **bech32 (native segwit):** `caps1…` — the default, used by the web wallet
- **Legacy P2PKH:** addresses beginning with `C`
- Full version bytes in Appendix A.

---

## 4. Supply and emission

| Parameter | Value |
|---|---|
| Block reward | 50 CAPS |
| Block time | 5 minutes |
| Halving interval | 210,000 blocks (~2 years) |
| Maximum supply | 21,000,000 CAPS |
| Coinbase maturity | 50 blocks |
| Premine | 470,000 CAPS in block 1 |

### 4.1 The premine, without spin

Block 1 contains **470,000 CAPS**.

At height 649, total supply is **502,400 CAPS**. The premine is therefore:

- **≈ 93.6% of all CAPS that currently exist**
- **≈ 2.24% of the 21,000,000 eventual maximum**
- **≈ 4.5% of the 10,500,000 that will be issued before the first halving**

Both the first number and the last two are true, and they tell different
stories. The first is what a sceptic will calculate today, so it is printed
here first. The chain is young — 649 blocks — so ordinary emission has not yet
had time to dilute the initial allocation. That dilution is mechanical and
predictable: at 50 CAPS per 5-minute block, roughly 14,400 CAPS are issued per
day, and the premine falls below 50% of supply at around block 9,400 (~33 days
of continuous mining from genesis).

**What it is for:** seeding the mining pool and funding community prizes, tips
and perks. **Where it is:** held by the project operator in a known wallet.
**Commitment:** material spends from the premine will be disclosed publicly.

A reader who considers a 470,000-coin premine disqualifying is making a
reasonable judgement, and this document is not going to argue them out of it.

---

## 5. The stack

Everything described here is live and open source.

### 5.1 Node

`capsd` / `caps-cli`, built from github.com/ShaeOJ/caps-core. Default P2P port
**12566**, RPC **12567**. Linux x86_64 binaries with SHA-256 checksums are
published on the website; Windows and macOS are currently build-from-source.

### 5.2 Mining pool

A.S.I.C. Mining Pool (asicpool.space) runs CAPS in both **PROP**
(proportional) and **SOLO** modes at **0% fee**. SOLO rewards are paid
directly to the miner's address in the block's coinbase — the pool never
custodies them.

- ASIC: `stratum+tcp://asicpool.space:8433`
- CPU / low difficulty: `stratum+tcp://asicpool.space:8434`
- Username: your CAPS address. Password: `x`.

Running CAPS through a single pool is a centralisation risk, not a feature;
see Section 7.3.

### 5.3 Explorer

An Eiquidus block explorer at caps.undergroundroots.ca — blocks, transactions,
address balances and history, with a public `/ext/` API.

### 5.4 Web wallet

A **non-custodial** browser wallet at wallet.undergroundroots.ca.

- BIP39 mnemonic → BIP32 HD (BIP84, P2WPKH) using CAPS network parameters
- Keys are generated, encrypted and used **only in the browser**; the server
  never receives them
- Seed encrypted at rest with scrypt (N=2¹⁷) → AES-GCM in IndexedDB
- Transactions are built and signed client-side; the server only relays the
  signed hex to a node
- Strict Content-Security-Policy, no third-party scripts, no analytics

Crucially, the wallet has a **reproducible build**: a clean clone of the
public repository, built with `npm ci`, produces a bundle byte-identical to
the one the site serves. You do not have to trust the operator — you can
verify:

```sh
git clone https://github.com/ShaeOJ/caps-web-wallet && cd caps-web-wallet/web
npm ci && npm run build
sha256sum dist/app.js
curl -s https://wallet.undergroundroots.ca/app.js | sha256sum   # must match
```

Its limits are described honestly in Section 7.4.

---

## 6. Current state of the network

Measured at height 649, 24 October 2026:

| Metric | Value |
|---|---|
| Block height | 649 |
| Total supply | 502,400 CAPS |
| Difficulty | ~1.56 |
| Network hashrate | ~23 MH/s |
| Reachable peers (seed node) | 2 |
| Chain size on disk | < 1 MB |

This is a young, small network. The numbers are printed so nobody has to
guess.

---

## 7. Security model and honest limitations

This is the most important section of this document.

### 7.1 Proof-of-work security is negligible

CAPS network hashrate is approximately **23 MH/s**. A single modern SHA-256
ASIC — for example an Antminer S19 at ~100 TH/s — is roughly **4.4 million
times** the entire CAPS network.

The consequence is unambiguous: **anyone with one second-hand miner, or a few
dollars of rented hashrate, can reorganise the CAPS chain at will.** CAPS does
not have meaningful proof-of-work security in absolute terms and does not
claim to. Any statement that CAPS is "secured by SHA-256 like Bitcoin" would
be technically true about the algorithm and dangerously misleading about the
security, and is not made here.

### 7.2 Why that is survivable today, and what would change it

Double-spend attacks are economically motivated: an attacker reorganises a
chain to reverse a payment they have already converted into something else.
CAPS has no exchange, no market and no liquid off-ramp. There is, at present,
nothing to steal. The realistic threat is **vandalism** — someone reorganising
the chain to prove they can — which is disruptive but not profitable.

This is an argument about the *current* stakes, not a defence of weak
security. If CAPS ever acquired a liquid market while hashrate remained this
low, the risk profile would change materially and this section would need
rewriting before, not after.

**Do not treat CAPS as a settlement layer for anything valuable.**

### 7.3 Centralisation

Stated plainly:

- Essentially **all current hashrate is a single operator**.
- The seed node reports **2 connections** — the network is close to
  self-contained.
- One person currently runs the node, the pool, the explorer and the wallet.

This means CAPS today is closer to a well-documented single-operator system
than to a decentralised network. The most valuable contribution anyone can
make is not buying anything — it is **running an independent node, or mining
from somewhere else.**

### 7.4 The web wallet's trust boundary

The wallet is genuinely non-custodial: keys never leave the browser, and this
is verifiable in the source. But a web wallet **serves the key-handling code
on every page load**. If the hosting infrastructure or the source repository
were compromised, an attacker could serve modified JavaScript that exfiltrates
seeds, and a Content-Security-Policy cannot prevent same-origin code from
doing so.

Mitigations in place: reproducible builds and published hashes (Section 5.4),
branch protection on the repository, strict security headers, and a backend
that is not reachable from the public internet.

Mitigations **not** possible in JavaScript: secure memory zeroing, and defence
against malware or a hostile browser extension on the user's own machine.

Recommendation: treat the web wallet as a **hot wallet** — appropriate for
mining payouts and community-scale amounts. Hardware-wallet and
offline-signing support are on the roadmap.

### 7.5 Single-operator continuity risk

If the current operator stopped, the pool, explorer and wallet would go
offline. The chain itself would survive only as long as someone runs a node.
See Section 8.

---

## 8. Governance and continuity

There is no foundation, no governance token, no voting mechanism, and no
treasury. CAPS is a project run by one person, which is stated here rather
than dressed up as decentralisation.

What makes that survivable:

- **Everything is open source.** Node, pool, explorer, wallet and website are
  all published.
- **Chain parameters are documented** (Appendix A), so anyone can build a
  compatible node.
- **Nothing requires permission.** Anyone may run a node, start a competing
  pool, host an explorer, or fork the project entirely.
- **No infrastructure holds user funds.** The wallet is non-custodial and SOLO
  mining pays directly to the coinbase.

If the operator disappears, CAPS does not automatically die — but it will only
continue if other people are already running nodes. That is the honest answer,
and it is another reason Section 7.3 matters.

Consensus changes, if any are ever needed, will be announced publicly with the
reasoning and lead time, and will require node operators to upgrade
voluntarily.

---

## 9. Roadmap

This is a statement of direction, not a set of promises, and deliberately
carries no dates.

### Shipped
- Chain live on mainnet (SHA-256d, LWMA difficulty)
- Mining pool: PROP + SOLO, 0% fee, ASIC and CPU ports
- Block explorer
- Non-custodial web wallet with reproducible builds
- Public website with Linux node binaries and checksums

### Near term — lower the barrier to running CAPS
- **Windows and macOS node binaries** (currently Linux-only) — the single
  biggest accessibility gap
- **A one-command node setup and published seed addresses.** At this size,
  node count is a more meaningful decentralisation metric than hashrate
- Wallet improvements: receive-address rotation, clearer backup flow, offline/PWA use

### Medium term — make it genuinely used
- Community tipping and prizes actually circulating — the community-currency
  pillar has to be demonstrated, not asserted
- **Independent miners and a second pool**, so the current pool is not a
  chokepoint and Section 7.3 stops being true
- Hardware-wallet / offline signing support

### Long term — resilience
- Node diversity across operators and locations
- Revisiting attack posture *if* hashrate ever grows enough to matter
- A boring, well-documented upgrade process

### Explicitly not on the roadmap
These are commitments, not omissions:
- No exchange-listing promises, market making, or price targets
- No presale, ICO, staking yields, or "rewards programmes"
- No treasury raise and no governance token
- No claim that CAPS is a store of value or a hedge against anything

---

## 10. How to participate

**Mine it**
```
stratum+tcp://asicpool.space:8433   # ASIC
stratum+tcp://asicpool.space:8434   # CPU / low difficulty
username: <your caps1… address>     password: x
```

**Run a node** — minimal `caps.conf`:
```
server=1
daemon=1
txindex=1
rpcuser=choose_a_user
rpcpassword=choose_a_strong_password
addnode=caps.undergroundroots.ca
```
Start `capsd`, then check progress with `caps-cli getblockchaininfo`.

**Hold it** — create a wallet at wallet.undergroundroots.ca, write down the
12-word phrase offline, and verify the bundle hash (Section 5.4).

**Explore it** — caps.undergroundroots.ca

**Read or fork the code** — github.com/ShaeOJ/caps-core

The most useful thing you can do for CAPS is run a node and mine from your own
hardware.

---

## Appendix A — Chain parameters

| Parameter | Mainnet | Regtest |
|---|---|---|
| bech32 HRP | `caps` | `capsrt` |
| P2PKH version byte | `0x1C` (addresses start `C`) | `0x6F` (111) |
| P2SH version byte | `0x1D` | `0xC4` (196) |
| WIF / secret key | `0x9C` | `0xEF` (239) |
| BIP32 xpub / xprv | `0x0488B21E` / `0x0488ADE4` | `0x043587CF` / `0x04358394` |
| P2P port | 12566 | — |
| RPC port | 12567 | — |
| PoW algorithm | SHA-256d | SHA-256d |
| Target block time | 300 s | 300 s |
| Difficulty algorithm | LWMA, N = 96 | — |
| Emergency difficulty reset | after 60 min without a block | — |
| Block reward | 50 CAPS | 50 CAPS |
| Halving interval | 210,000 blocks | 210,000 blocks |
| Maximum supply | 21,000,000 CAPS | — |
| Coinbase maturity | 50 blocks | 50 blocks |
| Wallet derivation path | `m/84'/0'/0'/{0,1}/i` (BIP84, P2WPKH) | same |

## Appendix B — Repositories

| Component | Repository |
|---|---|
| Node (Caps Core) | github.com/ShaeOJ/caps-core |
| Web wallet | github.com/ShaeOJ/caps-web-wallet |
| Website | github.com/ShaeOJ/caps-site |

## Appendix C — Verifying what you run

**Node binaries:** download `SHA256SUMS.txt` from
caps-core.undergroundroots.ca and run `sha256sum -c SHA256SUMS.txt`.

**Web wallet:** see Section 5.4. A matching hash proves the served code is the
published source. A mismatch means **do not enter your seed phrase**.

---

*CAPS is a community project of undergroundroots. It is not an investment, and
nothing in this document is financial advice. All figures were verified at
block height 649 on 24 October 2026 and will drift as the chain grows.*