# BTLCAP — A Wasteland Community Currency

*White Paper Version 1.2 — Including the Bottlecaps (CAPC) AuxPoW Sidechain*

**White paper · version 1.1**
Last verified at **block height 4,487**, 3 November 2026.

> **Rename in progress — CAPS is becoming BTLCAP.** The ticker and name are
> changing from *CAPS* to *BTLCAP* (to avoid a clash with an unrelated project),
> along with the address spelling (`caps1…`/`C…` → `btlcap1…`/`B…`). This is a
> **rebrand plus a forward-only supply upgrade, not a relaunch** — the same
> chain, the same blocks, and every coin already mined carry over untouched. On
> the wire and on disk the software, ports and config keys stay `caps*`.

Website: caps-core.undergroundroots.ca · Explorer: caps.undergroundroots.ca
Wallet: wallet.undergroundroots.ca · Source: github.com/ShaeOJ/caps-core

---

## Abstract

BTLCAP is a small SHA-256d proof-of-work cryptocurrency with a
post-apocalyptic bottle-cap theme. It exists so that an ordinary person can
run an entire crypto stack end to end — mine a block, run a full node, read an
explorer, and hold their own keys — on a chain small enough to actually
understand.

BTLCAP is **not an investment**, has no market, and makes no promises about
price. Two facts are stated here rather than buried: block 1 contains a
**470,000 BTLCAP premine**, which is about **67.7% of all coins currently in
existence** (though only ~0.11% of the eventual 420,470,000 maximum); and the
network is currently **tiny and centralised** — roughly 1.4 TH/s, essentially
all of it from one operator. A single modern ASIC is millions of times that
hashrate. Anyone evaluating BTLCAP should read Section 7 before anything else.

---

## 1. Why BTLCAP exists

Most coins ask you to buy them. BTLCAP asks you to run one.

Learning how a blockchain actually works is harder than it should be. On large
chains you will never find a block, running a node is a spectator sport, and
the tooling hides the mechanics behind an exchange account. The useful parts —
the parts that teach you something — are only visible at small scale.

BTLCAP is deliberately small. A hobby ASIC, or even a CPU, can find blocks. A
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

## 2. What BTLCAP is not

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

BTLCAP is a fork of Bitcoin Silver, itself derived from Bitcoin Core (v24/25
era). The large majority of the codebase is unmodified upstream Bitcoin, which
is a deliberate choice: the consensus-critical code is the part you least want
a hobbyist rewriting. Changes are confined to chain parameters, the difficulty
algorithm, and branding.

### 3.1 Proof of work

BTLCAP uses **SHA-256d** (double SHA-256) — the same proof-of-work function as
Bitcoin. This makes BTLCAP mineable with ordinary SHA-256 ASIC hardware that
people already own, which is the point: the barrier to participation is a
miner you may already have in a cupboard. It also means BTLCAP shares a hash
function with chains that have astronomically more hashrate, with the
consequences described in Section 7.

### 3.2 Difficulty: LWMA

Block interval targets **5 minutes (300 seconds)**.

Rather than Bitcoin's 2016-block retarget, BTLCAP uses **LWMA** (Linearly
Weighted Moving Average) with a window of **N = 96 blocks**, recalculated
every block, with solve times clamped at 20× the target.

The reasoning is practical. On a small network, hashrate arrives and leaves in
large relative bursts — one miner connecting can multiply the network's
capacity. Under Bitcoin's retarget, a big miner leaving would strand the chain
at a difficulty nobody could meet, potentially for days. A per-block weighted
average tracks hashrate closely enough to keep blocks flowing.

This behaves as intended in practice: when BTLCAP first passed the N=96
window, difficulty ramped by roughly 67× to match the hashrate that had
arrived.

As a backstop, if no block is found for **60 minutes** (12× the target
spacing), difficulty resets to the minimum so that any miner can recover the
chain.

### 3.3 Addresses

- **bech32 (native segwit):** `btlcap1…` — the default, used by the web wallet
- **Legacy P2PKH:** addresses beginning with `B`
- During the rename the live network still issues the old `caps1…` / `C…`
  format; the new spelling activates at the coordinated cutover (Section 4.2).
  The keys and coins are identical in both — only the encoding changes.
- Full version bytes in Appendix A.

---

## 4. Supply and emission

| Parameter | Value |
|---|---|
| Block reward | 500 BTLCAP |
| Block time | 5 minutes |
| Halving interval | 420,000 blocks (~4 years) |
| Maximum supply | ~420,470,000 BTLCAP (420,000,000 mined + 470,000 premine) |
| Coinbase maturity | 50 blocks |
| Premine | 470,000 BTLCAP in block 1 |

### 4.1 The premine, without spin

Block 1 contains **470,000 BTLCAP**.

At height 4,487, total supply is **694,300 BTLCAP**. The premine is therefore:

- **≈ 67.7% of all BTLCAP that currently exist**
- **≈ 0.11% of the 420,470,000 eventual maximum**
- **≈ 0.22% of the 210,000,000 that will be issued before the first halving**

Both the first number and the last two are true, and they tell different
stories. The first is what a sceptic will calculate today, so it is printed
here first. The chain is young — 4,487 blocks — so ordinary emission has not
yet had time to dilute the initial allocation. That dilution is mechanical and
predictable: at 500 BTLCAP per 5-minute block, roughly 144,000 BTLCAP are
issued per day, and the premine falls below 50% of supply within a few days of
continuous mining.

**What it is for:** seeding the mining pool and funding community prizes, tips
and perks. **Where it is:** held by the project operator in a known wallet.
**Commitment:** material spends from the premine will be disclosed publicly.

A reader who considers a 470,000-coin premine disqualifying is making a
reasonable judgement, and this document is not going to argue them out of it.

### 4.2 The rename + supply upgrade (in progress)

A combined rename and consensus upgrade is **rolling out now**. Two things
change together, in one coordinated cutover:

1. **Rename CAPS → BTLCAP.** The name, ticker and bottle-cap logo change, and
   addresses are re-spelled from `caps1…`/`C…` to `btlcap1…`/`B…`. This is a
   display/encoding change: the keys, the coins and the chain are untouched.
2. **A 500-reward / four-year-halving emission.** The block reward is **500
   BTLCAP** and the subsidy halves every **420,000 blocks** (~4 years at 5-minute
   spacing), so the first halving (500 → 250 BTLCAP) lands at block 420,000.

Because the maximum supply is nothing more than the sum of every block reward,
this schedule tops out near **420,470,000 BTLCAP** (420,000,000 mined over all
eras, plus the 470,000 premine). The amount issued before the first halving is
**210,000,000 BTLCAP**, and the premine's share of the eventual maximum is
about **0.11%** (470,000 of 420,470,000).

The point that matters most: **this is a forward-only change that requires no
new genesis block.** Every coin mined so far — including the block 1 premine —
is preserved exactly; balances, transaction history and keys are all
untouched. A new genesis would mean a brand-new chain starting from zero and
would discard every existing coin; that is explicitly *not* what this is.

The old and new emission rules are identical for every block up to height
420,000, where the first halving occurs, and the chain is years away from that
height. Nothing already on the chain changes. The emission change is a **hard
fork**: every node operator, the pool and all miners must run an upgraded
binary **before block 420,000** — the last height at which the two schedules
still agree. The address re-spelling is not a consensus change at all (it
cannot fork the chain); it is coordinated with the upgrade only so wallets,
the pool and the explorer all switch together. It is announced with reasoning
and lead time (Section 8).

---

## 5. The stack

Everything described here is live and open source.

### 5.1 Node

`capsd` / `caps-cli`, built from github.com/ShaeOJ/caps-core. Default P2P port
**12566**, RPC **12567**. Linux x86_64 binaries with SHA-256 checksums are
published on the website; Windows and macOS are currently build-from-source.
(The on-disk tool names stay `caps*` through the rebrand.)

### 5.2 Mining pool

A.S.I.C. Mining Pool (asicpool.space) runs BTLCAP in both **PROP**
(proportional) and **SOLO** modes at **0% fee**. SOLO rewards are paid
directly to the miner's address in the block's coinbase — the pool never
custodies them.

- ASIC: `stratum+tcp://asicpool.space:8433`
- CPU / low difficulty: `stratum+tcp://asicpool.space:8434`
- Username: your BTLCAP address. Password: `x`.

Running BTLCAP through a single pool is a centralisation risk, not a feature;
see Section 7.3.

### 5.3 Explorer

An Eiquidus block explorer at caps.undergroundroots.ca — blocks, transactions,
address balances and history, with a public `/ext/` API.

### 5.4 Web wallet

A **non-custodial** browser wallet at wallet.undergroundroots.ca.

- BIP39 mnemonic → BIP32 HD (BIP84, P2WPKH) using BTLCAP network parameters
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

### 5.5 Mobile vault app (Caps Vault)

An open-source Android native application combining secure credential
management, cryptographic identity custody, and full BTLCAP wallet integration.

- Master encryption key derived client-side via PBKDF2-HMAC-SHA256 from user
  passphrase + hardware-backed biometric authentication (Fingerprint / Face Unlock).
- Embedded non-custodial wallet with native `btlcap1…` SegWit address management
  and client-side ECDSA transaction signing.
- Interactive 3D bottlecap collection renderer and offline vault cache.
- Zero telemetry, no cloud storage, fully offline-capable.

### 5.6 Bottlecaps (CAPC) Sidechain & Digital Collectibles

A dedicated merged-mined sidechain utilizing Auxiliary Proof of Work (AuxPoW)
to introduce verifiable digital wasteland trading cards without energy overhead.

- **Zero Energy Overhead:** Mainnet miners simultaneously mine BTLCAP and
  the Bottlecaps sidechain. Blocks submitted on the pool carry auxiliary
  merkle proofs, securing the sidechain using BTLCAP's primary SHA-256d hashrate.
- **Automated Miner Drops:** Every mined block triggers a deterministic
  1-of-1 card drop directly to the block finder across 5 procedural rarity
  tiers: Scrap (Tier 1), Brass (Tier 2), Silver (Tier 3), Gilded Gold (Tier 4),
  and Quantum Glow (Tier 5).
- **Single-Use Seals:** Ownership is bound to unspent transaction outputs
  (UTXOs). Card transfers are validated on-chain via `CAPC\x02` (`OP_TRANSFER`)
  payloads, ensuring peer-to-peer non-custodial trading.
- **The Wasteland Forge Studio:** End users can mint custom 1-of-1 bottlecaps
  by drawing vector strokes or uploading badge emblems. Forging burns 50 BCAP
  on mainnet via `CAPC\x04` (`OP_FORGE`), permanently anchoring the artwork's
  SHA-256 recipe hash into chain history.

---

## 6. Current state of the network

Measured at height 4,487, 3 November 2026:

| Metric | Value |
|---|---|
| Block height | 4,487 |
| Total supply | 694,300 BTLCAP |
| Difficulty | ~98205.10 |
| Network hashrate | ~1.4 TH/s |
| Reachable peers (seed node) | 1 |
| Chain size on disk | < 1 MB |

This is a young, small network. The numbers are printed so nobody has to
guess.

---

## 7. Security model and honest limitations

This is the most important section of this document.

### 7.1 Proof-of-work security is negligible

BTLCAP network hashrate is approximately **1.4 TH/s**. A single modern SHA-256
ASIC — for example an Antminer S19 at ~100 TH/s — is roughly **0.0 million
times** the entire BTLCAP network.

The consequence is unambiguous: **anyone with one second-hand miner, or a few
dollars of rented hashrate, can reorganise the BTLCAP chain at will.** BTLCAP
does not have meaningful proof-of-work security in absolute terms and does not
claim to. Any statement that BTLCAP is "secured by SHA-256 like Bitcoin" would
be technically true about the algorithm and dangerously misleading about the
security, and is not made here.

### 7.2 Why that is survivable today, and what would change it

Double-spend attacks are economically motivated: an attacker reorganises a
chain to reverse a payment they have already converted into something else.
BTLCAP has no exchange, no market and no liquid off-ramp. There is, at
present, nothing to steal. The realistic threat is **vandalism** — someone
reorganising the chain to prove they can — which is disruptive but not
profitable.

This is an argument about the *current* stakes, not a defence of weak
security. If BTLCAP ever acquired a liquid market while hashrate remained this
low, the risk profile would change materially and this section would need
rewriting before, not after.

**Do not treat BTLCAP as a settlement layer for anything valuable.**

### 7.3 Centralisation

Stated plainly:

- Essentially **all current hashrate is a single operator**.
- The seed node reports **2 connections** — the network is close to
  self-contained.
- One person currently runs the node, the pool, the explorer and the wallet.

This means BTLCAP today is closer to a well-documented single-operator system
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
treasury. BTLCAP is a project run by one person, which is stated here rather
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

If the operator disappears, BTLCAP does not automatically die — but it will
only continue if other people are already running nodes. That is the honest
answer, and it is another reason Section 7.3 matters.

Consensus changes — such as the 500-reward / four-year halving schedule
described in Section 4.2 — will be announced publicly with the reasoning and
lead time, and will require node operators to upgrade voluntarily.

---

## 9. Roadmap

This is a statement of direction, not a set of promises, and deliberately
carries no dates.

### Shipped
- Chain live on mainnet (SHA-256d, LWMA difficulty)
- Mining pool: PROP + SOLO, 0% fee, ASIC and CPU ports
- Block explorer
- Non-custodial web wallet with reproducible builds
- Public website with Linux, Windows, and macOS node binaries
- **BTLCAP rebrand & 420M supply schedule:** 500 BCAP block reward, 420,000-block halving interval, and native `btlcap1…` SegWit addresses
- **Built-in DNS seed node discovery:** automatic peer mesh via `caps.undergroundroots.ca`
- **Mobile vault app (Caps Vault):** Android release with biometric authentication, key management, and 3D collectible viewer
- **Bottlecaps (CAPC) sidechain:** AuxPoW merged mining on the pool, procedural card drops, single-use UTXO seals, and custom 50 BCAP Forge Studio

### Near term — ecosystem utility
- **Wasteland Trading Post:** Trustless on-chain P2P card swaps and exchange
- Wallet improvements: receive-address rotation, clearer backup flow, offline/PWA use
- **Independent miners and a second pool**, so the current pool is not a
  chokepoint and Section 7.3 stops being true

### Medium term — make it genuinely used
- Community tipping and merchant checkout integrations
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
- No claim that BTLCAP is a store of value or a hedge against anything

---

## 10. How to participate

**Mine it**
```
stratum+tcp://asicpool.space:8433   # ASIC
stratum+tcp://asicpool.space:8434   # CPU / low difficulty
username: <your address>            password: x
```
Today the network still uses `caps1…` addresses; they become `btlcap1…` at the
cutover (Section 4.2).

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

The most useful thing you can do for BTLCAP is run a node and mine from your
own hardware.

---

## Appendix A — Chain parameters

| Parameter | Mainnet | Regtest |
|---|---|---|
| bech32 HRP | `btlcap` | `btlcaprt` |
| P2PKH version byte | `0x19` (addresses start `B`) | `0x6F` (111) |
| P2SH version byte | `0x32` | `0xC4` (196) |
| WIF / secret key | `0x99` | `0xEF` (239) |
| BIP32 xpub / xprv | `0x0488B21E` / `0x0488ADE4` | `0x043587CF` / `0x04358394` |
| P2P port | 12566 | — |
| RPC port | 12567 | — |
| PoW algorithm | SHA-256d | SHA-256d |
| Target block time | 300 s | 300 s |
| Difficulty algorithm | LWMA, N = 96 | — |
| Emergency difficulty reset | after 60 min without a block | — |
| Block reward | 500 BTLCAP | 500 BTLCAP |
| Halving interval | 420,000 blocks | 420,000 blocks |
| Maximum supply | ~420,470,000 BTLCAP | — |
| Coinbase maturity | 50 blocks | 50 blocks |
| Wallet derivation path | `m/84'/0'/0'/{0,1}/i` (BIP84, P2WPKH) | same |

These are the parameters of the chain after the Section 4.2 upgrade. The
address re-spelling and the 500-reward / 420,000-block halving roll out
together at the cutover; until then the live network still uses the `caps`
HRP, the `0x1C`/`C` P2PKH byte and the 50-reward / 210,000-block schedule. No
coin already mined is affected by either change.

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

*BTLCAP (formerly CAPS) is a community project of undergroundroots. It is not
an investment, and nothing in this document is financial advice. All figures
were verified at block height 4,487 on 3 November 2026 and will drift as the
chain grows.*