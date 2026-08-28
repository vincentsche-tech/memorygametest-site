#!/usr/bin/env python3
"""Phase 1: rewrite 5 core pages' title/desc/og/twitter to align with SERP top-3 patterns.
- Add "Free" to title (mandatory in winners)
- Add specific promise: time + result
- Keep ≤60 char title, ≤160 char desc
- 3-tag sync: <title>, og:title, twitter:title + meta description trio
- Idempotent: re-run safe (only rewrites if old string present)
- memory-game.html SKIPPED (different vertical, leave as-is)
"""
import os, re, sys, html
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) or os.chdir('.')

CHANGES = {
    'index.html': {
        'old_t': 'Memory Test &amp; Memory Game – Play Free Online Memory Tests',
        'new_t': 'Free Memory Test Online – 5 Min, Instant Results',
        'old_d': 'Play free memory games and take memory tests online. Test your photographic and eidetic memory with our fun, free memory challenges.',
        'new_d': 'Free memory test online – number memory challenge, short term recall, instant score in 5 minutes. No signup, no download.',
    },
    'memory-test-online.html': {
        'old_t': 'Memory Test Online – 3 Free Tests to Measure Your Memory',
        'new_t': 'Memory Test Online – 3 Free Tests, Instant Results',
        'old_d': 'Take free memory tests online: number memory, card matching, and visual recall. Measure your working memory and improve it with daily practi…',
        'new_d': '3 free memory tests: number memory, card matching, visual recall. Instant results, no signup. See your score and improve daily.',
    },
    'photographic-memory-test.html': {
        'old_t': 'Photographic Memory Test – Can You Recall Like a Camera?',
        'new_t': 'Photographic Memory Test – Free, Honest Visual Recall',
        'old_d': 'Take a photographic memory test online. Learn what photographic memory really is, how to test it, and whether it can be trained.',
        'new_d': 'Free photographic memory test online. Find out in 5 minutes if you have it. Learn how it differs from eidetic memory.',
    },
    'eidetic-memory-test.html': {
        'old_t': 'Eidetic Memory Test – Do You Have Vivid Mental Imagery?',
        'new_t': 'Eidetic Memory Test – Free, Honest Visual Recall',
        'old_d': 'Take an eidetic memory test online. Learn what eidetic memory is, how it differs from photographic memory, and how to test yours.',
        'new_d': 'Free eidetic memory test online. Test vivid mental imagery in 5 minutes. Learn how it differs from photographic memory.',
    },
}

def wc(c):
    c2 = re.sub(r'<(script|style|head)[^>]*>.*?</\1>', ' ', c, flags=re.S)
    c2 = re.sub(r'<[^>]+>', ' ', c2)
    return len(re.findall(r"\S+", html.unescape(c2)))

def rewrite(fn, chg):
    p = os.path.join('.', fn)
    c = open(p, encoding='utf-8').read()
    orig = c
    if chg['old_t'] not in c:
        print(f"  SKIP {fn}: old title not present (already rewritten?)")
        return False
    c = c.replace(f'<title>{chg["old_t"]}</title>', f'<title>{chg["new_t"]}</title>', 1)
    c = c.replace(f'<meta name="description" content="{chg["old_d"]}">',
                  f'<meta name="description" content="{chg["new_d"]}">', 1)
    c = c.replace(f'<meta property="og:title" content="{chg["old_t"]}">',
                  f'<meta property="og:title" content="{chg["new_t"]}">', 1)
    c = c.replace(f'<meta property="og:description" content="{chg["old_d"]}">',
                  f'<meta property="og:description" content="{chg["new_d"]}">', 1)
    c = c.replace(f'<meta name="twitter:title" content="{chg["old_t"]}">',
                  f'<meta name="twitter:title" content="{chg["new_t"]}">', 1)
    c = c.replace(f'<meta name="twitter:description" content="{chg["old_d"]}">',
                  f'<meta name="twitter:description" content="{chg["new_d"]}">', 1)
    if c == orig:
        return False
    open(p, 'w', encoding='utf-8').write(c)
    print(f"  OK {fn}: {len(chg['new_t'])}ch title / {len(chg['new_d'])}ch desc | {wc(c)} words total")
    return True

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    if dry: print("=== DRY RUN ===\n")
    for fn, chg in CHANGES.items():
        if dry:
            print(f"  [DRY] {fn}: title {len(chg['new_t'])}ch / desc {len(chg['new_d'])}ch")
            assert len(chg['new_t']) <= 60, f"❌ {fn} title >60!"
            assert len(chg['new_d']) <= 160, f"❌ {fn} desc >160!"
        else:
            rewrite(fn, chg)
    if not dry:
        print("\n=== validation ===")
        ok = True
        for fn, chg in CHANGES.items():
            c = open(fn, encoding='utf-8').read()
            if chg['new_t'] not in c: print(f"  ❌ {fn}: new title missing"); ok = False
            if chg['old_t'] in c: print(f"  ❌ {fn}: old title still present"); ok = False
            if chg['new_d'] not in c: print(f"  ❌ {fn}: new desc missing"); ok = False
            n = c.count(chg['new_t'])
            if n < 3: print(f"  ❌ {fn}: new title only appears {n} times (need ≥3)"); ok = False
        print("✅ all 4 pages: title/desc + 3-tag sync OK" if ok else "❌ validation failed")
