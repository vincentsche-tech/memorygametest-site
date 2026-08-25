# -*- coding: utf-8 -*-
"""Thicken Memory site core pages: +guide card, +3 FAQ items, +FAQPage JSON-LD.
Targets 600-800 visible words per core page. Reuses existing .card/.faq-item/.cta styles.
"""
import json, re, html

BASE = "https://www.memorygametest.com"

# ---- per-page content -------------------------------------------------------
PAGES = {
    "index.html": {
        "guide_card": '''  <div class="card">
    <h2>🧩 Understanding Your Memory</h2>
    <h3>Short-term vs long-term memory</h3>
    <p>Your brain handles memory in stages. Short-term (or working) memory holds a small amount of information for seconds — like a phone number you just heard. Long-term memory stores it for years. Our memory tests mostly challenge working memory, the scratchpad your brain uses every day.</p>
    <h3>When is the best time to train your brain?</h3>
    <p>Most people perform best on memory tasks in the late morning, after waking fully alert and before afternoon fatigue sets in. But consistency matters more than timing: a few minutes of daily practice builds stronger neural pathways than one long weekend session.</p>
  </div>

''',
        "new_faq": '''    <div class="faq-item"><b>How long does a memory test take?</b><p>Our quick tests take under a minute. The number memory test lasts as long as you keep going; the card game usually finishes in two to three minutes.</p></div>
    <div class="faq-item"><b>Is my score saved?</b><p>Yes — your best scores are stored privately in your browser's local storage on the same device. We don't upload or share them. Clearing your browser data resets them.</p></div>
    <div class="faq-item"><b>Are memory games suitable for kids?</b><p>Absolutely. The card-matching game is great for children and helps build focus and visual recall. We recommend adult supervision for very young kids online.</p></div>
''',
        "faq": [
            ("What is a memory test?", "A memory test measures how well you can remember and recall information — like a sequence of numbers or the position of matching cards. Our tests are fun, free, and take less than a minute."),
            ("Can memory games improve my memory?", "Yes! Regular practice with memory games trains your working memory, improves focus, and strengthens pattern recognition. Think of it as a workout for your brain."),
            ("What is the difference between photographic and eidetic memory?", "Photographic memory refers to recalling visual information with photographic accuracy, while eidetic memory is the ability to hold a vivid mental image for a short period. Both are rare and fascinating."),
            ("Are these memory tests scientifically accurate?", "Our tests are designed for fun and self-improvement, not medical diagnosis. If you have concerns about your memory, please consult a healthcare professional."),
            ("How long does a memory test take?", "Our quick tests take under a minute. The number memory test lasts as long as you keep going; the card game usually finishes in two to three minutes."),
            ("Is my score saved?", "Yes — your best scores are stored privately in your browser's local storage on the same device. We don't upload or share them. Clearing your browser data resets them."),
            ("Are memory games suitable for kids?", "Absolutely. The card-matching game is great for children and helps build focus and visual recall. We recommend adult supervision for very young kids online."),
        ],
    },
    "memory-game.html": {
        "guide_card": '''  <div class="card">
    <h2>🎯 Go Deeper With Memory Games</h2>
    <h3>Memory game variations to try</h3>
    <p>Beyond classic pairs, you can level up by racing the clock, limiting your flips, or playing themed decks (animals, flags, words). Each variation trains a different angle of visual recall and keeps practice fresh and engaging.</p>
    <h3>Who benefits most from memory games?</h3>
    <p>Students use them to sharpen focus before study sessions; older adults use them to keep visual recall nimble. Because they're low-pressure and fun, memory games are one of the easiest brain-training habits to stick with long term.</p>
  </div>

''',
        "new_faq": '''    <div class="faq-item"><b>Is there a time limit in the memory game?</b><p>No. Our game is untimed — you can play at your own pace. The built-in timer simply records how long you take so you can try to beat your personal best.</p></div>
    <div class="faq-item"><b>Can I play the memory game on mobile?</b><p>Yes. The board and buttons are touch-friendly and responsive, so you can flip cards with a tap on any phone or tablet right in your browser.</p></div>
    <div class="faq-item"><b>Why did my best score disappear?</b><p>Best scores are saved in your browser on this device. They reset if you clear browsing data, switch devices, or use private mode. Nothing is stored on our servers.</p></div>
''',
        "faq": [
            ("Is the memory game good for your brain?", "Yes! Card-matching games exercise working memory, visual recall, and concentration — all important cognitive skills that benefit from regular practice."),
            ("What's a good memory game score?", "Matching 8 pairs in under 20 moves is good; under 15 is excellent. Our players' average is about 20-25 moves."),
            ("Can adults benefit from memory games?", "Absolutely. Adults who play memory games regularly show improvements in focus, recall speed, and working memory. It's never too late to train your brain."),
            ("Is there a time limit in the memory game?", "No. Our game is untimed — you can play at your own pace. The built-in timer simply records how long you take so you can try to beat your personal best."),
            ("Can I play the memory game on mobile?", "Yes. The board and buttons are touch-friendly and responsive, so you can flip cards with a tap on any phone or tablet right in your browser."),
            ("Why did my best score disappear?", "Best scores are saved in your browser on this device. They reset if you clear browsing data, switch devices, or use private mode. Nothing is stored on our servers."),
        ],
    },
    "photographic-memory-test.html": {
        "guide_card": '''  <div class="card">
    <h2>🔬 The Science of Visual Memory</h2>
    <h3>What research actually shows</h3>
    <p>Scientists have studied eidetic imagery for decades, mostly in children, but the "photographic memory" of popular culture remains unproven in adults. What research confirms is that visual memory is a real, trainable skill that varies widely between people.</p>
    <h3>Everyday signs of strong visual memory</h3>
    <p>You may have above-average visual memory if you easily recall faces, remember where you parked, mentally picture book pages, or navigate familiar streets without a map. These are normal strengths — not proof of a photographic memory, but useful ones.</p>
  </div>

''',
        "new_faq": '''    <div class="faq-item"><b>What counts as a "normal" visual memory?</b><p>Most people remember visual details better than they expect when they actively pay attention. Above-average visual memory means you recall more detail than typical, but it's a spectrum, not a pass/fail test.</p></div>
    <div class="faq-item"><b>Can taking photos improve my memory?</b><p>Interestingly, over-relying on photos can weaken recall ("photo-taking impairment"). For training, study the scene with your eyes, then put the camera away and describe what you saw.</p></div>
    <div class="faq-item"><b>Is photographic memory linked to intelligence?</b><p>Not directly. Strong visual memory is a specific talent, not a measure of overall intelligence or IQ. Many people with average memory excel in other cognitive areas.</p></div>
''',
        "faq": [
            ("Does photographic memory really exist?", "True photographic memory (permanent, camera-perfect recall) has never been scientifically proven in adults. However, some people have remarkably strong visual memories that appear photographic."),
            ("How rare is photographic memory?", "If we define it as scientifically-proven perfect recall, it's essentially nonexistent in adults. Highly developed visual memory is more common but still unusual — roughly 2-10% of people show above-average visual recall."),
            ("Can I improve my memory with games?", "Yes. Memory games train working memory and visual recall. Regular practice (even 5-10 minutes daily) can improve your performance measurably."),
            ("What counts as a \"normal\" visual memory?", "Most people remember visual details better than they expect when they actively pay attention. Above-average visual memory means you recall more detail than typical, but it's a spectrum, not a pass/fail test."),
            ("Can taking photos improve my memory?", "Interestingly, over-relying on photos can weaken recall ('photo-taking impairment'). For training, study the scene with your eyes, then put the camera away and describe what you saw."),
            ("Is photographic memory linked to intelligence?", "Not directly. Strong visual memory is a specific talent, not a measure of overall intelligence or IQ. Many people with average memory excel in other cognitive areas."),
        ],
    },
    "eidetic-memory-test.html": {
        "guide_card": '''  <div class="card">
    <h2>🌟 Eidetic Memory in Daily Life</h2>
    <h3>Eidetic memory in children vs adults</h3>
    <p>Eidetic imagery is most often observed in children, who may describe a picture they just saw in surprising detail. It usually fades through the teen years. Adults rarely report true eidetic recall, though many keep strong, trainable visual memory.</p>
    <h3>Exercises to strengthen mental imagery</h3>
    <p>Try a daily "mind's eye" routine: study an object for 20 seconds, close your eyes, and redraw it from memory. Repeat with photos, then scenes. Over weeks, this visualization habit noticeably sharpens the imagery behind good recall.</p>
  </div>

''',
        "new_faq": '''    <div class="faq-item"><b>At what age does eidetic memory fade?</b><p>Eidetic imagery is most common in young children and typically declines during childhood and the teen years. By adulthood it is rare, which is why adult "eidetic" claims are treated with skepticism.</p></div>
    <div class="faq-item"><b>Can visualization replace eidetic memory?</b><p>Visualization won't give you true eidetic recall, but it builds the practical skill people value most: a vivid, controllable mental image you can use for study, navigation, and creativity.</p></div>
    <div class="faq-item"><b>Does eidetic memory mean high IQ?</b><p>No. Eidetic imagery is a specific perceptual trait, not a general intelligence marker. Some people with it have typical IQs, and many high-IQ people have ordinary visual memory.</p></div>
''',
        "faq": [
            ("Is eidetic memory real?", "Yes! Unlike photographic memory, eidetic memory is scientifically documented — the ability to hold a vivid mental image for a short period. It's most common in children."),
            ("What percentage of people have eidetic memory?", "Studies suggest 2-10% of children show eidetic imagery. It typically declines with age and is rare in adults."),
            ("Can eidetic memory be trained?", "True eidetic imagery in adults is rare and not reliably trainable. But visual memory skills — the practical benefits people associate with eidetic memory — can definitely be improved with practice."),
            ("At what age does eidetic memory fade?", "Eidetic imagery is most common in young children and typically declines during childhood and the teen years. By adulthood it is rare, which is why adult 'eidetic' claims are treated with skepticism."),
            ("Can visualization replace eidetic memory?", "Visualization won't give you true eidetic recall, but it builds the practical skill people value most: a vivid, controllable mental image you can use for study, navigation, and creativity."),
            ("Does eidetic memory mean high IQ?", "No. Eidetic imagery is a specific perceptual trait, not a general intelligence marker. Some people with it have typical IQs, and many high-IQ people have ordinary visual memory."),
        ],
    },
    "memory-test-online.html": {
        "guide_card": '''  <div class="card">
    <h2>📊 Getting the Most From Memory Tests</h2>
    <h3>Types of memory tests, explained</h3>
    <p>Broadly, memory tests fall into three buckets: verbal (remembering words or numbers), visual (recalling images or positions), and working-memory (holding info while using it). Our number and card games sample working and visual memory; combined, they sketch a useful personal baseline.</p>
    <h3>How to read your results over time</h3>
    <p>A single score means little; trends matter. Log your best number span and card moves weekly. Small, steady gains signal improving recall, while flat or dropping scores may mean fatigue, poor sleep, or distraction — useful feedback in itself.</p>
  </div>

''',
        "new_faq": '''    <div class="faq-item"><b>Are online memory tests reliable?</b><p>For fun and self-tracking, yes. Our tests give a consistent personal baseline you can watch improve. They are not clinical tools and shouldn't replace professional evaluation.</p></div>
    <div class="faq-item"><b>What age should I start memory training?</b><p>Any age. Children build focus, adults maintain sharpness, and older adults protect recall. The habit matters more than the starting point — a few minutes most days is enough.</p></div>
    <div class="faq-item"><b>Can a memory test detect a problem?</b><p>Our tests can't diagnose anything. If you notice a sudden, worrying drop in everyday memory, consult a healthcare professional rather than relying on an online game.</p></div>
''',
        "faq": [
            ("What is a good memory test score?", "For number recall, remembering 5-9 digits is average. For card matching, completing 8 pairs in under 20 moves is good. These are fun benchmarks, not medical diagnostics."),
            ("Do memory tests measure IQ?", "No. Working memory correlates with some cognitive abilities but is not IQ. Memory tests measure one specific skill: short-term recall."),
            ("How often should I take memory tests?", "Daily practice is great, but avoid over-testing. Try our tests 2-3 times per week and track your best scores for improvement."),
            ("Are online memory tests reliable?", "For fun and self-tracking, yes. Our tests give a consistent personal baseline you can watch improve. They are not clinical tools and shouldn't replace professional evaluation."),
            ("What age should I start memory training?", "Any age. Children build focus, adults maintain sharpness, and older adults protect recall. The habit matters more than the starting point — a few minutes most days is enough."),
            ("Can a memory test detect a problem?", "Our tests can't diagnose anything. If you notice a sudden, worrying drop in everyday memory, consult a healthcare professional rather than relying on an online game."),
        ],
    },
}

GRID_ANCHOR_DEFAULT = '  <div class="card">\n    <h2>More Memory Tests &amp; Guides</h2>'
GRID_ANCHOR_INDEX = '  <div class="card">\n    <h2>📚 Memory Tests &amp; Guides</h2>'
FAQ_CLOSE_ANCHOR = "  </div>\n</main>"


def build_faq_jsonld(url, faq_list):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faq_list
        ],
    }
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, indent=2, ensure_ascii=False)
        + "\n</script>\n"
    )


def visible_words(t):
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[^\sa-zA-Z0-9'-]", " ", t)
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*", t))


for fn, spec in PAGES.items():
    src = open(fn, encoding="utf-8").read()
    before = visible_words(src)

    # 1) insert guide card before the "More Memory Tests" grid card
    anchor = GRID_ANCHOR_INDEX if fn == "index.html" else GRID_ANCHOR_DEFAULT
    assert anchor in src, f"{fn}: grid anchor missing"
    src = src.replace(anchor, spec["guide_card"] + anchor, 1)

    # 2) append new FAQ items inside the FAQ card (before its closing </div></main>)
    assert FAQ_CLOSE_ANCHOR in src, f"{fn}: faq-close anchor missing"
    src = src.replace(FAQ_CLOSE_ANCHOR, spec["new_faq"] + FAQ_CLOSE_ANCHOR, 1)

    # 3) inject FAQPage JSON-LD before </head>
    assert "</head>" in src, f"{fn}: </head> missing"
    url = re.search(r'<link rel="canonical" href="([^"]+)"', src).group(1)
    ld = build_faq_jsonld(url, spec["faq"])
    src = src.replace("</head>", ld + "</head>", 1)

    open(fn, "w", encoding="utf-8").write(src)
    after = visible_words(src)
    print(f"{fn:28s} {before:4d} -> {after:4d}  (+{after-before}, FAQ={len(spec['faq'])})")

print("DONE")
