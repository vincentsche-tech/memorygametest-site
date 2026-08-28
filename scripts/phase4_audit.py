import re, html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_PAGES = [
    "index.html", "photographic-memory-test.html", "eidetic-memory-test.html",
    "memory-test-online.html", "memory-game.html", "short-term-memory-test.html",
    "working-memory-test.html", "long-term-memory-test.html",
]
INFO_PAGES = ["about.html", "contact.html", "privacy-policy.html", "terms.html"]
NEW_PAGES = ["short-term-memory-test.html", "working-memory-test.html", "long-term-memory-test.html"]
ALL = TEST_PAGES + INFO_PAGES

def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()

def meta_tag(s, name):
    # name or property
    m = re.search(r'<meta\s+(?:name|property)="%s"\s+content="([^"]*)"' % re.escape(name), s)
    return html.unescape(m.group(1)) if m else None

def title(s):
    m = re.search(r"<title>([^<]*)</title>", s)
    return html.unescape(m.group(1)) if m else None

def count_words(s):
    m = re.search(r"<main>.*</main>", s, re.S)
    body = m.group(0) if m else s
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    text = html.unescape(text)
    return len(re.findall(r"[A-Za-z0-9']+", text))

def visible_faq(s):
    items = re.findall(r'<div class="faq-item"><b>([^<]*)</b><p>(.*?)</p></div>', s, re.S)
    out = []
    for q, a in items:
        out.append((html.unescape(q).strip(), html.unescape(re.sub(r"<[^>]+>", "", a)).strip()))
    return out

def jsonld_faq(s):
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    for b in blocks:
        try:
            data = json.loads(b)
        except Exception:
            continue
        if isinstance(data, dict) and data.get("@type") == "FAQPage":
            out = []
            for e in data.get("mainEntity", []):
                q = e["name"].strip()
                a = e["acceptedAnswer"]["text"].strip()
                out.append((q, a))
            return out
    return None

problems = []
print("=== Phase 4 Audit — %d pages ===" % len(ALL))
for p in ALL:
    s = read(p)
    t = title(s)
    md = meta_tag(s, "description")
    ogt = meta_tag(s, "og:title")
    ogd = meta_tag(s, "og:description")
    twt = meta_tag(s, "twitter:title")
    twd = meta_tag(s, "twitter:description")
    # title sync
    if not (t and ogt and twt and t == ogt == twt):
        problems.append(f"[{p}] TITLE not synced: title={t!r} og={ogt!r} tw={twt!r}")
    if t and len(t) > 60:
        problems.append(f"[{p}] TITLE too long ({len(t)} > 60): {t!r}")
    # desc sync
    if md is not None and not (md == ogd == twd):
        problems.append(f"[{p}] DESC not synced: meta={md!r} og={ogd!r} tw={twd!r}")
    if md is not None and len(md) > 160:
        problems.append(f"[{p}] DESC too long ({len(md)} > 160): {md!r}")
    # FAQ checks only where FAQPage JSON-LD present
    jf = jsonld_faq(s)
    vf = visible_faq(s)
    if jf is not None:
        if len(jf) < 5:
            problems.append(f"[{p}] FAQ count {len(jf)} < 5")
        if len(jf) != len(vf):
            problems.append(f"[{p}] FAQ count mismatch JSON({len(jf)}) vs visible({len(vf)})")
        else:
            for (jq, ja), (vq, va) in zip(jf, vf):
                if jq != vq or ja != va:
                    problems.append(f"[{p}] FAQ mismatch Q={jq[:40]!r}")
    # word count for new pages
    if p in NEW_PAGES:
        wc = count_words(s)
        if wc < 800:
            problems.append(f"[{p}] word count {wc} < 800")
        else:
            print(f"  {p}: {wc} words OK")
    # canonical (it's a <link rel="canonical">, not <meta>)
    can = re.search(r'<link rel="canonical" href="([^"]*)"', s)
    if can is None:
        problems.append(f"[{p}] missing canonical")

# sitemap coverage
sm = read("sitemap.xml")
for p in TEST_PAGES + NEW_PAGES:
    loc = "https://www.memorygametest.com/" + ("" if p == "index.html" else p)
    if loc not in sm:
        problems.append(f"[sitemap] missing {loc}")

print("\n=== RESULT ===")
if problems:
    print("PROBLEMS (%d):" % len(problems))
    for x in problems:
        print("  -", x)
    sys.exit(1)
else:
    print("ALL CHECKS PASSED ✅")
