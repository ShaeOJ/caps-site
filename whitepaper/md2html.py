#!/usr/bin/env python3
"""Render the CAPS white paper markdown into a themed standalone HTML page."""
import io, re, sys, html, datetime

# Assets are served with max-age=604800, so a changed stylesheet would be
# held stale for a week — which once left the beta modal unstyled and
# rendering below the footer. Version every local asset reference.
ASSET_V = datetime.datetime.now().strftime('%Y%m%d%H%M')

src, dst = sys.argv[1], sys.argv[2]
lines = io.open(src, encoding='utf-8').read().split('\n')

def inline(t):
    t = html.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)([^*]+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    # bare urls / hostnames -> links
    t = re.sub(r'(?<![">/\w])((?:https?://|www\.)[^\s<)]+)', r'<a href="\1">\1</a>', t)
    t = re.sub(r'(?<![">/\w.])((?:caps-core|caps|wallet)\.undergroundroots\.ca)(?![\w<])',
               r'<a href="https://\1">\1</a>', t)
    t = re.sub(r'(?<![">/\w.])(github\.com/ShaeOJ/[\w-]+)', r'<a href="https://\1">\1</a>', t)
    t = re.sub(r'(?<![">/\w.])(asicpool\.space)(?![\w:<])', r'<a href="https://\1">\1</a>', t)
    return t

out, i = [], 0
toc = []
while i < len(lines):
    ln = lines[i]; s = ln.strip()

    if s.startswith('```'):                                  # code block
        i += 1; buf = []
        while i < len(lines) and not lines[i].strip().startswith('```'):
            buf.append(html.escape(lines[i])); i += 1
        i += 1
        out.append('<pre><code>' + '\n'.join(buf) + '</code></pre>'); continue

    if s.startswith('|'):                                    # table
        rows = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            r = lines[i].strip().strip('|')
            if not re.match(r'^[\s:|-]+$', r):
                rows.append([c.strip() for c in r.split('|')])
            i += 1
        if rows:
            head, body = rows[0], rows[1:]
            t = ['<div class="tw"><table><thead><tr>' +
                 ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>']
            for r in body:
                t.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>')
            t.append('</tbody></table></div>')
            out.append('\n'.join(t))
        continue

    m = re.match(r'^(#{1,6})\s+(.*)', s)                     # heading
    if m:
        lvl, txt = len(m.group(1)), m.group(2)
        aid = re.sub(r'[^a-z0-9]+', '-', txt.lower()).strip('-')
        if lvl == 1:
            out.append(f'<h1>{inline(txt)}</h1>')
        else:
            out.append(f'<h{lvl} id="{aid}">{inline(txt)}</h{lvl}>')
            if lvl == 2 and not txt.lower().startswith('appendix'):
                toc.append((aid, txt))
            elif lvl == 2:
                toc.append((aid, txt))
        i += 1; continue

    if re.match(r'^(---+|\*\*\*+)$', s):                     # hr
        out.append('<hr>'); i += 1; continue

    if re.match(r'^[-*]\s+', s):                             # bullet list
        items = []
        while i < len(lines) and re.match(r'^[-*]\s+', lines[i].strip()):
            buf = [re.sub(r'^[-*]\s+', '', lines[i].strip())]; i += 1
            while i < len(lines) and lines[i].startswith('  ') and lines[i].strip() \
                  and not re.match(r'^[-*]\s+', lines[i].strip()):
                buf.append(lines[i].strip()); i += 1
            items.append(' '.join(buf))
        out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>'); continue

    if re.match(r'^\d+\.\s+', s):                            # numbered list
        items = []
        while i < len(lines) and re.match(r'^\d+\.\s+', lines[i].strip()):
            buf = [re.sub(r'^\d+\.\s+', '', lines[i].strip())]; i += 1
            while i < len(lines) and lines[i].startswith('  ') and lines[i].strip() \
                  and not re.match(r'^\d+\.\s+', lines[i].strip()):
                buf.append(lines[i].strip()); i += 1
            items.append(' '.join(buf))
        out.append('<ol>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ol>'); continue

    if not s:                                                # blank
        i += 1; continue

    buf = []                                                 # paragraph
    while i < len(lines) and lines[i].strip() and not re.match(
            r'^(#{1,6}\s|[-*]\s|\d+\.\s|\||```|---+$)', lines[i].strip()):
        buf.append(lines[i].strip()); i += 1
    out.append('<p>' + inline(' '.join(buf)) + '</p>')

body = '\n'.join(out)
nav = '\n'.join(f'<li><a href="#{a}">{html.escape(t)}</a></li>' for a, t in toc)

page = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>CAPS White Paper v1.0</title>
<meta name="description" content="The CAPS white paper: design, consensus, supply and emission, the premine stated plainly, and an honest account of the network's security limitations.">
<meta property="og:title" content="CAPS White Paper v1.0">
<meta property="og:description" content="Design, consensus, supply, and an honest account of CAPS's security limitations.">
<meta property="og:image" content="/assets/caps-og.png">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="stylesheet" href="/assets/style.css?v={ASSET_V}">
<link rel="stylesheet" href="/assets/paper.css?v={ASSET_V}">
</head><body>
<canvas id="bgfx" aria-hidden="true"></canvas>
<div class="scanlines" aria-hidden="true"></div>

<header class="site-nav">
  <a class="brand" href="/"><img src="/assets/caps-logo.png" alt="" width="34" height="34"><span>CAPS</span></a>
  <nav>
    <a href="/#about">About</a>
    <a href="/#specs">Specs</a>
    <a href="/#start">Get started</a>
    <a href="/#downloads">Downloads</a>
    <a class="ext" href="https://caps.undergroundroots.ca">Explorer &#8599;</a>
  </nav>
</header>

<main class="paper">
  <div class="paper-actions">
    <a class="btn" href="/whitepaper/CAPS_whitepaper_v1.0.txt">Plain text &#8595;</a>
    <a class="btn" href="/whitepaper/CAPS_whitepaper_v1.0.md">Markdown &#8595;</a>
  </div>
  <aside class="toc"><h2>Contents</h2><ul>{nav}</ul></aside>
  <article>
{body}
  </article>
</main>

<footer class="site-foot">
  <div class="foot-links">
    <a href="/">Home</a>
    <a href="https://github.com/ShaeOJ/caps-core">GitHub</a>
    <a href="https://caps.undergroundroots.ca">Explorer</a>
    <a href="https://wallet.undergroundroots.ca">Wallet</a>
    <a href="https://asicpool.space">Pool</a>
  </div>
  <p>CAPS &middot; a community project of <a href="https://undergroundroots.ca">undergroundroots</a>. Not an investment &mdash; a wasteland currency you actually use.</p>
</footer>
<script src="/assets/bgfx.js?v={ASSET_V}" defer></script>
<script src="/assets/beta-notice.js?v={ASSET_V}" defer></script>
</body></html>
'''
io.open(dst, 'w', encoding='utf-8').write(page)
print('wrote', dst, len(page), 'bytes;', len(toc), 'toc entries')
