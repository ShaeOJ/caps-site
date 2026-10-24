import io, re, sys
src, dst = sys.argv[1], sys.argv[2]
out = []
for line in io.open(src, encoding='utf-8').read().split('\n'):
    s = line.rstrip()
    s = (s.replace('—','--').replace('–','-').replace('’',"'")
          .replace('⭐','*').replace('“','"').replace('”','"')
          .replace('≈','~').replace('·','-').replace('²','^2')
          .replace('→','->'))
    if s.startswith('```'):                      # drop code fences, keep content indented
        out.append(''); continue
    if re.match(r'^\|[\s:-]+\|', s):             # markdown table separator row
        continue
    if s.startswith('|'):                        # table row -> aligned-ish plain text
        cells = [c.strip() for c in s.strip('|').split('|')]
        out.append('    ' + '  |  '.join(cells)); continue
    m = re.match(r'^(#{1,6})\s+(.*)', s)
    if m:
        lvl, txt = len(m.group(1)), m.group(2)
        txt = re.sub(r'\*\*(.+?)\*\*', r'\1', txt)
        if lvl == 1:
            out += ['', '=' * 74, txt.upper(), '=' * 74]
        elif lvl == 2:
            out += ['', txt, '-' * len(txt)]
        else:
            out += ['', txt]
        continue
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)       # bold
    s = re.sub(r'(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)', r'\1', s)  # italic
    s = re.sub(r'`([^`]+)`', r'\1', s)           # inline code
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', s)  # links
    s = s.replace('—', '--').replace('–', '-').replace('’', "'").replace('⭐', '*')
    s = s.replace('“', '"').replace('”', '"').replace('≈', '~').replace('·', '-')
    s = s.replace('²', '^2').replace('→', '->')
    out.append(s)
txt = '\n'.join(out)
txt = re.sub(r'\n{4,}', '\n\n\n', txt)
io.open(dst, 'w', encoding='utf-8', newline='\r\n').write(txt)   # CRLF for Notepad
print('wrote', dst)
