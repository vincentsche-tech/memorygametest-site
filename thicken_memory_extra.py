# -*- coding: utf-8 -*-
"""Second pass: push index / memory-game / memory-test-online past 600 words.
Adds an extra guide section + a 4th FAQ item (visible + FAQPage JSON-LD)."""
import json, re, html

EXTRA = {
    "index.html": {
        "section": '''    <h3>Do memory games actually change your brain?</h3>
    <p>Brain-imaging studies show that repeated cognitive practice can strengthen the networks involved in attention and recall. You won't grow a "photographic" memory overnight, but steady training makes everyday remembering feel easier — finding words, following instructions, and learning new skills all draw on the same working-memory system our games exercise.</p>
''',
        "section_anchor": "one long weekend session.</p>\n  </div>",
        "faq": ("Why does my memory feel worse some days?",
                "Memory fluctuates with sleep, stress, hydration, and attention. A bad score after a poor night's sleep is normal and temporary — it reflects your state, not your ability. Train when rested to see your true baseline."),
    },
    "memory-game.html": {
        "section": '''    <h3>Turn memory games into a daily habit</h3>
    <p>The biggest gains come from routine, not marathon sessions. Try pairing the game with an existing habit — one round with your morning coffee, or a quick match while waiting in line. Because it's free and instantly playable, the memory game fits into gaps in your day far more easily than most brain-training programs.</p>
''',
        "section_anchor": "stick with long term.</p>\n  </div>",
        "faq": ("Why does my memory game score vary day to day?",
                "Scores naturally swing with focus, sleep, and mood. A slower day doesn't mean your memory got worse — it means your attention dipped. Play consistently and watch the trend, not any single round."),
    },
    "memory-test-online.html": {
        "section": '''    <h3>Make memory testing a weekly ritual</h3>
    <p>Pick a consistent day and time each week, then run one number round and one card game, and jot down your best scores in a notes app. A light, regular check-in reveals slow improvement that a one-off test hides — and turns an idle curiosity into a genuinely useful self-tracking habit.</p>
''',
        "section_anchor": "useful feedback in itself.</p>\n  </div>",
        "faq": ("Why track memory test scores week by week?",
                "A single result is noisy. Weekly tracking smooths out off days and shows whether your recall is trending up, flat, or slipping — the kind of signal that helps you spot fatigue, stress, or genuine progress."),
    },
}

FAQ_CLOSE_ANCHOR = "  </div>\n</main>"
JSONLD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def build_faq_jsonld(url, faq_list):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq_list
        ],
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>")


def find_faqpage_block(src):
    for m in JSONLD_RE.finditer(src):
        try:
            obj = json.loads(m.group(1))
        except Exception:
            continue
        if obj.get("@type") == "FAQPage":
            return m
    return None


def existing_faq_list(src):
    m = find_faqpage_block(src)
    obj = json.loads(m.group(1))
    return [(e["name"], e["acceptedAnswer"]["text"]) for e in obj["mainEntity"]]


def replace_faqpage_block(src, new_block):
    m = find_faqpage_block(src)
    return src[:m.start()] + new_block + src[m.end():]


def visible_words(t):
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[^\sa-zA-Z0-9'-]", " ", t)
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*", t))


for fn, spec in EXTRA.items():
    src = open(fn, encoding="utf-8").read()
    before = visible_words(src)

    # extra guide section: insert before the matched closing </div> of the added guide card
    assert spec["section_anchor"] in src, f"{fn}: section anchor missing"
    old_close = spec["section_anchor"].replace("</p>\n  </div>", "</p>\n" + spec["section"] + "  </div>")
    src = src.replace(spec["section_anchor"], old_close, 1)

    # 4th FAQ item (visible) before FAQ card close
    faq_div = ('    <div class="faq-item"><b>%s</b><p>%s</p></div>\n'
               % (spec["faq"][0], spec["faq"][1]))
    assert FAQ_CLOSE_ANCHOR in src, f"{fn}: faq-close anchor missing"
    src = src.replace(FAQ_CLOSE_ANCHOR, faq_div + FAQ_CLOSE_ANCHOR, 1)

    # regenerate FAQPage JSON-LD with the 4th entry appended (without touching WebApplication)
    lst = existing_faq_list(src) + [spec["faq"]]
    url = re.search(r'<link rel="canonical" href="([^"]+)"', src).group(1)
    src = replace_faqpage_block(src, build_faq_jsonld(url, lst))

    open(fn, "w", encoding="utf-8").write(src)
    after = visible_words(src)
    print(f"{fn:28s} {before:4d} -> {after:4d}  (+{after-before}, FAQ={len(lst)})")

print("DONE")
