# -*- coding: utf-8 -*-
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------- palette ----------
PLUM   = RGBColor(0x4A, 0x1F, 0x3D)   # deep aubergine
PLUM2  = RGBColor(0x6E, 0x33, 0x5C)
ROSE   = RGBColor(0xC9, 0x6F, 0x8A)   # accent
GOLD   = RGBColor(0xC8, 0x9B, 0x3C)
INK    = RGBColor(0x2B, 0x25, 0x2A)
GREY   = RGBColor(0x6B, 0x63, 0x68)
LIGHT  = RGBColor(0xF6, 0xF1, 0xF4)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
CARD   = RGBColor(0xFB, 0xF8, 0xFA)
LINEC  = RGBColor(0xE3, 0xD8, 0xDF)
GREEN  = RGBColor(0x2E, 0x7D, 0x5B)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

def slide():
    return prs.slides.add_slide(BLANK)

def rect(s, x, y, w, h, fill, line=None, line_w=None, shadow=False, round_=False):
    shp = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,
        x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = line_w or Pt(1)
    shp.shadow.inherit = False
    return shp

def txt(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        space_after=4, line_spacing=1.0):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Pt(2)
    tf.margin_top = tf.margin_bottom = Pt(2)
    if isinstance(runs[0], tuple): runs = [runs]
    first = True
    for para in runs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align; p.space_after = Pt(space_after); p.line_spacing = line_spacing
        for (t, size, color, bold, *rest) in para:
            r = p.add_run(); r.text = t
            r.font.size = Pt(size); r.font.color.rgb = color; r.font.bold = bold
            r.font.name = 'Arial'
            if rest and rest[0] == 'i': r.font.italic = True
    return tb

def header(s, kicker, title, num):
    rect(s, 0, 0, SW, Inches(1.15), PLUM)
    rect(s, 0, Inches(1.15), SW, Pt(3), ROSE)
    txt(s, Inches(0.6), Inches(0.16), Inches(11), Inches(0.35),
        [[(kicker, 12, ROSE, True)]])
    txt(s, Inches(0.6), Inches(0.44), Inches(11.5), Inches(0.62),
        [[(title, 27, WHITE, True)]], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(12.4), Inches(0.16), Inches(0.7), Inches(0.4),
        [[(num, 12, ROSE, True)]], align=PP_ALIGN.RIGHT)

def bullet(s, x, y, w, items, size=15, gap=6):
    tb = s.shapes.add_textbox(x, y, w, Inches(4)); tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        p.space_after = Pt(gap); p.line_spacing = 1.05
        if isinstance(it, str): it = [(it, size, INK, False)]
        # bullet dot
        d = p.add_run(); d.text = '•  '; d.font.size = Pt(size); d.font.color.rgb = ROSE; d.font.bold = True; d.font.name='Arial'
        for (t, sz, col, bd, *rest) in it:
            r = p.add_run(); r.text = t; r.font.size = Pt(sz); r.font.color.rgb = col; r.font.bold = bd; r.font.name='Arial'
            if rest and rest[0]=='i': r.font.italic=True
    return tb

def footer(s):
    txt(s, Inches(0.6), Inches(7.12), Inches(9), Inches(0.3),
        [[('Attune', 9, GREY, True), ('  ·  the measurement layer for hormone therapy  ·  Milestone #2  ·  2026-07-03', 9, GREY, False)]])

# ============================================================ 1 TITLE
s = slide()
rect(s, 0, 0, SW, SH, PLUM)
rect(s, 0, Inches(4.6), SW, Pt(3), ROSE)
txt(s, Inches(0.9), Inches(2.0), Inches(11.5), Inches(1.0),
    [[('Attune', 54, WHITE, True), ('   ', 54, WHITE, False), ('[working name]', 16, ROSE, False, 'i')]])
txt(s, Inches(0.95), Inches(3.15), Inches(11), Inches(1.2),
    [[('The measurement layer for hormone therapy —', 24, ROSE, False)],
     [('turning "dose by feel" into engineering.', 24, WHITE, True)]], line_spacing=1.1)
txt(s, Inches(0.95), Inches(4.9), Inches(11.5), Inches(1.6),
    [[('Menopause & perimenopause hormone therapy · US + Canada', 15, WHITE, False)],
     [('Milestone Presentation #2', 14, ROSE, True), ('     |     Discovery-stage venture', 14, RGBColor(0xD9,0xC7,0xD2), False)],
     [('Team: [Founder name] · [advisors]        2026-07-03', 12, RGBColor(0xC9,0xB5,0xC2), False)]],
    line_spacing=1.3)

# ============================================================ 2 PROBLEM (v2 per working-draft discussion)
s = slide(); header(s, 'PROBLEM', 'A therapy dosed "by feel" — and no one records the feeling', '02'); footer(s)
rows2 = [
    ('~1,000,000 / yr', 'women start menopause hormone therapy in the US + Canada (est.) — perimenopause is the fastest-growing segment'),
    ('"Dose by feel."', 'NAMS/ACOG guidelines: titrate by her symptoms, not blood levels — yet no system records those symptoms'),
    ('3–6 months of trial & error', 'each dose change takes 4–6 weeks to judge; her doctor re-doses from a 15-minute recall'),
    ('7.4 yrs  vs  1 yr', 'symptoms last a median 7.4 years — half of women quit within 1; 62% stop abruptly against advice, 84% relapse'),
]
ry = Inches(1.45)
for i,(stat, desc) in enumerate(rows2):
    if i % 2 == 0:
        rect(s, Inches(0.6), ry, Inches(12.1), Inches(1.0), LIGHT)
    txt(s, Inches(0.85), ry, Inches(3.9), Inches(1.0),
        [[(stat, 20, PLUM if i != 3 else ROSE, True)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)
    txt(s, Inches(4.9), ry, Inches(7.6), Inches(1.0),
        [[(desc, 13.5, INK, False)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)
    ry = Emu(int(ry) + int(Inches(1.0)) + int(Inches(0.06)))
# hook banner
rect(s, Inches(0.6), Inches(5.85), Inches(12.1), Inches(0.85), PLUM, round_=True)
txt(s, Inches(0.9), Inches(5.85), Inches(11.5), Inches(0.85),
    [[('Titration is a craft run on recall. ', 18, WHITE, True),
      ('It should be a data problem.', 18, GOLD, True)]],
    anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.6), Inches(6.8), Inches(12.1), Inches(0.35),
    [[('$13B/yr out-of-pocket on low-evidence workarounds  ·  symptomatic women incur +45% healthcare costs', 11, GREY, False)]])
notes2 = s.notes_slide.notes_text_frame
notes2.text = (
    "SCRIPT (~80s):\n"
    "Every year, about a million women in the US and Canada start hormone therapy for menopause — and perimenopause is the fastest-growing segment. "
    "The clinical guideline for this therapy is explicit: adjust the dose by her symptoms, not blood levels. But no one — no system — records those symptoms. "
    "So she enters three to six months of trial and error. Each dose change takes four to six weeks to judge. In those weeks she can't tell whether worsening anxiety means too little estrogen or too much, and late-night searches return horror stories. "
    "Her doctor decides the next step from what she can recall in a fifteen-minute visit. "
    "The result: her symptoms will last a median of 7.4 years, but half of women abandon the therapy within one. And to be precise — informed discontinuation is a good outcome; the problem is that 62% stop abruptly, against medical advice, in an information vacuum — and 84% of them relapse. "
    "Then they spend thirteen billion dollars a year on supplements that don't work. "
    "The problem isn't the medicine. Titration is a craft run on recall. It should be a data problem.\n\n"
    "Q&A AMMO:\n"
    "- ~1M/yr: MY ESTIMATE (say so proactively). Logic: ~2.5-3M current US users (JAMA: ~5% of postmenopausal women) x ~50% first-year discontinuation, with a growing stock — a 10-20k/month inflow could not sustain the pool. Validating with a claims-data slice. Supporting: Epic Research +86% Rx since 2021; Truveta: 1 in 20 women 45-54 hold an estrogen Rx.\n"
    "- Dose by feel: NAMS 2022 Hormone Therapy Position Statement; ACOG concurs. Hormone levels fluctuate too much to guide dosing.\n"
    "- 3-6 months / 4-6 weeks: clinical consensus; full effect up to 12 weeks.\n"
    "- 7.4 years: SWAN study, JAMA Internal Medicine 2015, n=1,449 (Black women: median 10.1 yrs). If challenged 'symptom duration is not treatment duration': correct — the point is symptoms run in YEARS, abandonment happens in MONTHS, and 62% of it is against medical advice.\n"
    "- Half quit yr 1: PubMed 10614674 — 48% (younger) to 62% (older); side-effects are the top stated reason (64-87%). Pharmacy DB: only 54-69% still on the ORIGINAL regimen at 1 yr.\n"
    "- 62% abrupt / 84% relapse: BJOG 2025 systematic review (69 studies).\n"
    "- $13B: AARP survey (>$10B of it on non-medical products). +45%: actuarial analysis cited by Elektra Health.\n"
    "ETHICS FRAME (say aloud, esp. to women's-health investors): our goal is not retention maximisation — informed quitting is a good outcome; panic quitting against advice is the system failure we target."
)

# ============================================================ 3 SOLUTION
s = slide(); header(s, 'SOLUTION', 'Make titration a monitored "season" — with a start, an end, and a graduation', '03'); footer(s)
cols = [
    ('For her', ROSE, ['30-second structured daily check-in (SMS-first)',
                       '“Expected-band” feedback: is what you feel on the normal trajectory? (day 18, dose X)',
                       'Answers “is this normal?” before she rips off the patch']),
    ('For the clinician', PLUM, ['A one-page dose–symptom curve auto-sent 48h before the visit',
                                 'Red-flag symptoms auto-triaged',
                                 'Turns “not great?” into an 8-week record']),
    ('For the system', PLUM2, ['Structured data → one nurse oversees hundreds (exception-based)',
                               'Billable: RTM in the US (~$94/patient/mo)',
                               'Builds a dose↔response dataset that exists nowhere today']),
]
cx = Inches(0.6); cw = Inches(3.94); gap = Inches(0.14)
for i,(t, col, items) in enumerate(cols):
    x = Emu(int(cx) + i*(int(cw)+int(gap)))
    rect(s, x, Inches(1.5), cw, Inches(4.9), CARD, line=LINEC, line_w=Pt(1), round_=True)
    rect(s, x, Inches(1.5), cw, Inches(0.62), col, round_=False)
    txt(s, x, Inches(1.5), cw, Inches(0.62), [[(t, 17, WHITE, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    bullet(s, Emu(int(x)+Emu(Inches(0.22))), Inches(2.35), Emu(int(cw)-Emu(Inches(0.44))), items, size=13, gap=9)
txt(s, Inches(0.6), Inches(6.6), Inches(12), Inches(0.5),
    [[('Mechanism proven: ', 13, PLUM, True),
      ('Basch et al., JAMA 2017 (n=766) — structured symptom self-report + alerts kept cancer patients on treatment 2 months longer and extended survival 5.2 months.', 13, GREY, False)]], line_spacing=1.05)

# ============================================================ 4 MARKET — customer
s = slide(); header(s, 'MARKET · CUSTOMER PROFILE', 'Who we serve: women in the titration window', '04'); footer(s)
rect(s, Inches(0.6), Inches(1.45), Inches(6.0), Inches(5.4), CARD, line=LINEC, line_w=Pt(1), round_=True)
txt(s, Inches(0.85), Inches(1.65), Inches(5.5), Inches(0.5), [[('Primary user — “Sarah, 51”', 18, PLUM, True)]])
bullet(s, Inches(0.85), Inches(2.35), Inches(5.5),
    ['Just started HRT (or a non-hormonal menopause drug)',
     'In month 0–6: the highest-anxiety, highest-search, highest-quit window',
     [('Canada twist: ', 13, PLUM, True), ('may have no family doctor — nobody owns her post-prescription 24 weeks', 13, INK, False)],
     'Already paying out of pocket: copays, compounded HRT, supplements',
     'What she wants is not “fewer hot flashes” — it is “feel like myself again”'], size=13.5, gap=9)
rect(s, Inches(6.85), Inches(1.45), Inches(5.85), Inches(5.4), CARD, line=LINEC, line_w=Pt(1), round_=True)
txt(s, Inches(7.1), Inches(1.65), Inches(5.4), Inches(0.5), [[('Who pays (≠ the user)', 18, PLUM, True)]])
bullet(s, Inches(7.1), Inches(2.35), Inches(5.4),
    [[('Pharma', 14, ROSE, True), (' — launch-stage drug makers buying adherence + real-world evidence', 13.5, INK, False)],
     [('Virtual clinics', 14, ROSE, True), (' — embed us to cut first-year churn & win renewals', 13.5, INK, False)],
     [('Payers / RTM (US)', 14, ROSE, True), (' — monitoring reimbursed per patient-month', 13.5, INK, False)],
     [('Group benefits (Canada)', 14, ROSE, True), (' — Manulife/Sun Life; HRT claims +20.7% in 3 yrs', 13.5, INK, False)],
     [('She (DTC assist)', 14, ROSE, True), (' — low-price tier; mainly the data & patient engine', 13.5, INK, False)]], size=13.5, gap=10)

# ============================================================ 5 MARKET — size
s = slide(); header(s, 'MARKET · SIZE (ESTIMATE)', 'TAM / SAM / SOM — the on-treatment subset, US + Canada', '05'); footer(s)
funnel = [
    ('TAM', '~$0.5–1.5B / yr', 'All women on / starting hormone-related therapy in US+CA (~3.2M today, growing 20%+/yr) × $150–580 monitoring value + pharma RWE line', PLUM, Inches(12.1)),
    ('SAM', '~$150–300M / yr', 'Reachable in 3–5 yrs via virtual clinics + pharmacist channel (CA) + DTC + one pharma line', PLUM2, Inches(9.4)),
    ('SOM', '~$5–12M ARR', '36-month obtainable: 1 pharma pilot + 2 clinic design partners + 10–20k DTC subscribers', ROSE, Inches(6.6)),
]
y = Inches(1.7)
for (lab, val, sub, col, w) in funnel:
    xoff = Emu((int(SW)-int(w))//2)
    rect(s, xoff, y, w, Inches(1.35), col, round_=True)
    txt(s, Emu(int(xoff)+Emu(Inches(0.3))), y, Inches(1.6), Inches(1.35),
        [[(lab, 26, WHITE, True)]], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Emu(int(xoff)+Emu(Inches(1.9))), y, Inches(2.5), Inches(1.35),
        [[(val, 21, WHITE, True)]], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Emu(int(xoff)+Emu(Inches(4.5))), y, Emu(int(w)-Emu(Inches(4.7))), Inches(1.35),
        [[(sub, 12.5, WHITE, False)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)
    y = Emu(int(y)+Emu(Inches(1.55)))
txt(s, Inches(0.6), Inches(6.75), Inches(12.1), Inches(0.5),
    [[('Estimates. ', 12, PLUM, True, 'i'),
      ('Most-uncertain input = annual new-starts; to be validated with a Komodo/Truveta/IQVIA claims slice. No RTM code in Canada → revenue re-routes to benefits + pharmacist channel.', 12, GREY, False, 'i')]], line_spacing=1.05)

# ============================================================ 6 INDUSTRY / WHY NOW
s = slide(); header(s, 'MARKET · INDUSTRY & WHY NOW', 'Five inflection points landed in the same 18 months', '06'); footer(s)
items = [
    ('Regulatory', 'FDA removed HRT’s 20-year boxed warning (2025). US prescribing +86% since 2021; 1 in 20 women 45–54 now on estrogen.'),
    ('Reimbursement', '2026 brought the biggest-ever RTM expansion — treatment-response monitoring is billable per month for the first time.'),
    ('Supply', 'Virtual menopause clinics reached scale (Midi ~$1B) and now compete on “proof of outcomes” — our data is their renewal ammo.'),
    ('Drugs', 'Two non-hormonal launches (Veozah 2023, Lynkuet 2025) head-to-head — both need differentiating real-world evidence.'),
    ('Window', 'Fertility’s history rhymes: 2026–2028 is the payer-consolidation window. The measurement layer must claim its spot before a category winner internalises it.'),
]
y = Inches(1.5)
for i,(t, d) in enumerate(items):
    rect(s, Inches(0.6), y, Inches(0.5), Inches(0.95), ROSE if i%2 else PLUM, round_=True)
    txt(s, Inches(0.6), y, Inches(0.5), Inches(0.95), [[(str(i+1), 18, WHITE, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(1.3), y, Inches(2.4), Inches(0.95), [[(t, 15, PLUM, True)]], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(3.7), y, Inches(9.0), Inches(0.95), [[(d, 13, INK, False)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)
    y = Emu(int(y)+Emu(Inches(1.06)))

# ============================================================ 7 COMPETITION
s = slide(); header(s, 'COMPETITION', 'Everyone touches the patient — nobody owns the titration loop', '07'); footer(s)
rows = [
    ('Category', 'What they have', 'Structural gap', True),
    ('Virtual clinics (Midi, Evernow, Blair CA)', '6–12 wk video visits + reactive messaging', 'Point-sampling; passive inbox; blind weeks 2–5'),
    ('Tracker apps (Balance, HRTMe)', 'Symptom diary', 'No dose-alignment, no clinical loop, no billing'),
    ('Hormone hardware (Clair, Eli)', 'Hormone levels (inferred / tested)', 'Not the variable guidelines dose by'),
    ('Big-device makers / Apple Health', 'Mature sleep/weight tracking; could bundle follow-up Qs', 'Horizontal data collection — not treatment management'),
]
x0 = Inches(0.6); w1=Inches(3.9); w2=Inches(4.0); w3=Inches(4.2); y=Inches(1.5); rh=Inches(1.0)
for i,row in enumerate(rows):
    head = (len(row)==4)
    fill = PLUM if head else (CARD if i%2 else LIGHT)
    rect(s, x0, y, w1, rh, fill, line=LINEC, line_w=Pt(0.5))
    rect(s, Emu(int(x0)+int(w1)), y, w2, rh, fill, line=LINEC, line_w=Pt(0.5))
    rect(s, Emu(int(x0)+int(w1)+int(w2)), y, w3, rh, fill, line=LINEC, line_w=Pt(0.5))
    tc = WHITE if head else INK
    bd = True if head else False
    txt(s, Emu(int(x0)+Emu(Inches(0.12))), y, Emu(int(w1)-Emu(Inches(0.2))), rh, [[(row[0], 12.5, PLUM if head else PLUM, True)]] if not head else [[(row[0],13,WHITE,True)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)
    txt(s, Emu(int(x0)+int(w1)+Emu(Inches(0.12))), y, Emu(int(w2)-Emu(Inches(0.2))), rh, [[(row[1], 12.5, tc, bd)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)
    c3 = ROSE if (not head and i==4) else tc
    txt(s, Emu(int(x0)+int(w1)+int(w2)+Emu(Inches(0.12))), y, Emu(int(w3)-Emu(Inches(0.2))), rh, [[(row[2], 12.5, c3, bd or (not head and i==4))]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)
    y = Emu(int(y)+int(rh))
txt(s, Inches(0.6), Inches(6.7), Inches(12.1), Inches(0.5),
    [[('The device threat, answered: ', 13, PLUM, True),
      ('sensors and diaries are the collection layer — their data flows INTO our treatment loop. Glucometers didn’t kill diabetes-management; they created it.', 13, INK, False)]], line_spacing=1.05)

# ============================================================ 8 UVP
s = slide(); header(s, 'UNIQUE VALUE PROPOSITION', 'The titration crisis doesn’t happen during the appointment', '08'); footer(s)
rect(s, Inches(0.6), Inches(1.45), Inches(12.1), Inches(1.15), PLUM, round_=True)
txt(s, Inches(0.9), Inches(1.45), Inches(11.5), Inches(1.15),
    [[('“Cardiology always had follow-ups — iRhythm still built a billion-dollar company because ', 15, WHITE, False),
      ('arrhythmias don’t happen in the clinic', 15, GOLD, True),
      ('.” We are the ambulatory monitor for hormone therapy.', 15, WHITE, False)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1)
gaps = [
    ('Continuous, not point-sampled', 'We upgrade the input to the same visit — record, not recall.'),
    ('Proactive, not a passive inbox', 'The quitters are exactly the ones who never message.'),
    ('Covers the weeks 2–5 blind window', 'We reach her before she quits — visits come too late.'),
    ('A cross-patient interpretation engine', 'Day-level dose-aligned data no single clinic has. Copyable UI; un-copyable dataset.'),
    ('Monitoring made economic', 'Structured + billable → scales; a reactive inbox never does.'),
    ('Neutral & portable', 'Records follow the patient across GP / clinic / pharmacist.'),
]
cw=Inches(3.94); ch=Inches(1.55); gx=Inches(0.14); gy=Inches(0.16)
for i,(t,d) in enumerate(gaps):
    r=i//3; c=i%3
    x=Emu(int(Inches(0.6))+c*(int(cw)+int(gx)))
    y=Emu(int(Inches(2.95))+r*(int(ch)+int(gy)))
    rect(s, x, y, cw, ch, CARD, line=LINEC, line_w=Pt(1), round_=True)
    txt(s, Emu(int(x)+Emu(Inches(0.2))), Emu(int(y)+Emu(Inches(0.12))), Emu(int(cw)-Emu(Inches(0.4))), Inches(0.6),
        [[(t, 13.5, PLUM, True)]], line_spacing=1.0)
    txt(s, Emu(int(x)+Emu(Inches(0.2))), Emu(int(y)+Emu(Inches(0.72))), Emu(int(cw)-Emu(Inches(0.4))), Inches(0.8),
        [[(d, 12, INK, False)]], line_spacing=1.02)

# ============================================================ 9 TEAM
s = slide(); header(s, 'TEAM', 'Founder-led, advisor-backed', '09'); footer(s)
mem = [
    ('[Founder name]', 'Founder & CEO', 'Based in Canada. Running the discovery: pharmacist, physician & pharma-industry interviews. [1–2 lines of relevant background].'),
    ('[Clinical advisor]', 'Menopause / OB-GYN advisor', 'NAMS-certified clinician to co-design the PRO instrument and red-flag protocol. [To confirm].'),
    ('[Technical lead]', 'Product / Engineering', 'Owns the SMS-first check-in, one-page clinician summary and data pipeline. [To recruit].'),
]
cx=Inches(0.6); cw=Inches(3.94); gap=Inches(0.14)
for i,(n,role,d) in enumerate(mem):
    x=Emu(int(cx)+i*(int(cw)+int(gap)))
    rect(s, x, Inches(1.6), cw, Inches(4.4), CARD, line=LINEC, line_w=Pt(1), round_=True)
    circ = s.shapes.add_shape(MSO_SHAPE.OVAL, Emu(int(x)+Emu(Inches(1.42))), Inches(1.95), Inches(1.1), Inches(1.1))
    circ.fill.solid(); circ.fill.fore_color.rgb = PLUM if i==0 else ROSE; circ.line.fill.background(); circ.shadow.inherit=False
    txt(s, x, Inches(3.25), cw, Inches(0.5), [[(n, 16, PLUM, True)]], align=PP_ALIGN.CENTER)
    txt(s, x, Inches(3.75), cw, Inches(0.45), [[(role, 13, ROSE, True)]], align=PP_ALIGN.CENTER)
    txt(s, Emu(int(x)+Emu(Inches(0.25))), Inches(4.35), Emu(int(cw)-Emu(Inches(0.5))), Inches(1.5),
        [[(d, 12.5, INK, False)]], align=PP_ALIGN.CENTER, line_spacing=1.08)
txt(s, Inches(0.6), Inches(6.35), Inches(12), Inches(0.5),
    [[('Advisors sought: ', 13, PLUM, True), ('a health-economics / reimbursement advisor (RTM + Canadian MedsCheck) and a pharma medical-affairs contact.', 13, GREY, False)]])

# ============================================================ 10 BUSINESS MODEL — Lean Canvas
s = slide(); header(s, 'BUSINESS MODEL · LEAN CANVAS', 'How the pieces fit', '10'); footer(s)
# 5 columns top (2 rows in outer cols) + bottom two
def canv(x, y, w, h, title, items, col=PLUM):
    rect(s, x, y, w, h, CARD, line=LINEC, line_w=Pt(1))
    rect(s, x, y, w, Inches(0.32), col)
    txt(s, Emu(int(x)+Emu(Inches(0.1))), y, Emu(int(w)-Emu(Inches(0.15))), Inches(0.32),
        [[(title, 10.5, WHITE, True)]], anchor=MSO_ANCHOR.MIDDLE)
    tb=s.shapes.add_textbox(Emu(int(x)+Emu(Inches(0.1))), Emu(int(y)+Emu(Inches(0.38))), Emu(int(w)-Emu(Inches(0.2))), Emu(int(h)-Emu(Inches(0.42))))
    tf=tb.text_frame; tf.word_wrap=True; first=True
    for it in items:
        p=tf.paragraphs[0] if first else tf.add_paragraph(); first=False
        p.space_after=Pt(2); p.line_spacing=0.98
        r=p.add_run(); r.text='– '+it; r.font.size=Pt(9.5); r.font.color.rgb=INK; r.font.name='Arial'

top_y=Inches(1.45); top_h=Inches(2.55); bot_y=Inches(4.05); bot_h=Inches(1.5); metr_y=Inches(5.6); metr_h=Inches(1.35)
u=Inches(0.6); cw=Inches(2.42)
xs=[Emu(int(u)+i*int(cw)) for i in range(5)]
canv(xs[0], top_y, cw, Emu(int(top_h)+int(bot_h)+Emu(Inches(0.05))), 'PROBLEM',
     ['3–6 mo titration black box','~50% quit yr 1 (side-effects)','Clinicians dose on faulty recall','No dose↔response record exists'])
canv(xs[1], top_y, cw, top_h, 'SOLUTION',
     ['30-sec daily check-in','Expected-band feedback','1-page clinician summary','Red-flag triage'])
canv(xs[2], top_y, cw, Emu(int(top_h)+int(bot_h)+Emu(Inches(0.05))), 'UVP',
     ['“Know if you’re on track — before you quit”','The measurement layer for hormone therapy','iRhythm for titration'], col=ROSE)
canv(xs[3], top_y, cw, top_h, 'UNFAIR ADVANTAGE',
     ['Cross-clinic day-level dose-symptom dataset','Guideline-aligned','Provider-neutral & portable'], col=ROSE)
canv(xs[4], top_y, cw, Emu(int(top_h)+int(bot_h)+Emu(Inches(0.05))), 'CUSTOMER SEGMENTS',
     ['Users: women starting HRT / menopause meds','Beachhead: month 0–6, esp. Canada w/o family doctor','Payers: pharma, clinics, RTM, benefits'])
canv(xs[1], bot_y, cw, bot_h, 'CHANNELS',
     ['Embed in virtual clinics','Pharmacist channel (CA)','DTC landing page','Pharma partnerships'])
canv(xs[3], bot_y, cw, bot_h, 'COST STRUCTURE',
     ['Product & engineering','Clinical / regulatory (SaMD)','Data infra + pilot'])
# metrics + revenue bottom band (two half-width boxes)
rect(s, u, metr_y, Emu(int(cw)*2+int(Inches(0.05))), metr_h, CARD, line=LINEC, line_w=Pt(1))
rect(s, u, metr_y, Emu(int(cw)*2+int(Inches(0.05))), Inches(0.32), PLUM2)
txt(s, Emu(int(u)+Emu(Inches(0.1))), metr_y, Inches(4), Inches(0.32), [[('KEY METRICS', 10.5, WHITE, True)]], anchor=MSO_ANCHOR.MIDDLE)
txt(s, Emu(int(u)+Emu(Inches(0.15))), Emu(int(metr_y)+Emu(Inches(0.4))), Emu(int(cw)*2-int(Inches(0.2))), Inches(1),
    [[('– 8-wk check-in completion >60%   – 6-mo treatment-retention lift', 10, INK, False)],
     [('– titration rounds reduced   – RTM $ captured / patient', 10, INK, False)]], line_spacing=1.05)
rx=Emu(int(u)+int(cw)*3+int(Inches(0.05)))
rect(s, rx, metr_y, Emu(int(cw)*2-int(Inches(0.0))), metr_h, CARD, line=LINEC, line_w=Pt(1))
rect(s, rx, metr_y, Emu(int(cw)*2-int(Inches(0.0))), Inches(0.32), GREEN)
txt(s, Emu(int(rx)+Emu(Inches(0.1))), metr_y, Inches(4), Inches(0.32), [[('REVENUE STREAMS', 10.5, WHITE, True)]], anchor=MSO_ANCHOR.MIDDLE)
txt(s, Emu(int(rx)+Emu(Inches(0.15))), Emu(int(metr_y)+Emu(Inches(0.4))), Emu(int(cw)*2-int(Inches(0.2))), Inches(1),
    [[('– Pharma: adherence + RWE contracts ($50k–5M)   – RTM billing share (US, ~$94/pt/mo)', 10, INK, False)],
     [('– Clinic subscription / DTC assist ($10–15/mo)   – Canada: benefits + MedsCheck-linked', 10, INK, False)]], line_spacing=1.05)

# ============================================================ 11 LANDING PAGE
s = slide(); header(s, 'LANDING PAGE', 'Smoke-test to measure real demand & price', '11'); footer(s)
# mock browser
rect(s, Inches(0.6), Inches(1.5), Inches(6.4), Inches(5.1), WHITE, line=LINEC, line_w=Pt(1.2), round_=True)
rect(s, Inches(0.6), Inches(1.5), Inches(6.4), Inches(0.5), LIGHT, round_=True)
for k in range(3):
    dot=s.shapes.add_shape(MSO_SHAPE.OVAL, Emu(int(Inches(0.8))+k*int(Inches(0.28))), Inches(1.65), Inches(0.16), Inches(0.16))
    dot.fill.solid(); dot.fill.fore_color.rgb=LINEC; dot.line.fill.background(); dot.shadow.inherit=False
txt(s, Inches(1.9), Inches(1.55), Inches(4.8), Inches(0.4), [[('  attune.health', 11, GREY, False)]], anchor=MSO_ANCHOR.MIDDLE)
rect(s, Inches(0.9), Inches(2.25), Inches(5.8), Inches(1.5), PLUM, round_=True)
txt(s, Inches(1.1), Inches(2.4), Inches(5.4), Inches(1.2),
    [[('Started HRT? Know if you’re on track —', 18, WHITE, True)],
     [('before you give up on it.', 18, GOLD, True)]], line_spacing=1.05, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(1.1), Inches(3.95), Inches(5.4), Inches(0.9),
    [[('A 30-second daily check-in tells you what your symptoms mean, and gives your doctor the full picture.', 12.5, INK, False)]], line_spacing=1.1)
btn=rect(s, Inches(1.1), Inches(4.95), Inches(3.0), Inches(0.6), ROSE, round_=True)
txt(s, Inches(1.1), Inches(4.95), Inches(3.0), Inches(0.6), [[('Get early access — $12/mo', 13, WHITE, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(1.1), Inches(5.75), Inches(5.4), Inches(0.6), [[('Enter email  ▸  ', 12, GREY, False), ('[waitlist]', 12, PLUM, True)]])
# right: what we measure
txt(s, Inches(7.4), Inches(1.7), Inches(5.4), Inches(0.5), [[('What the page tests', 17, PLUM, True)]])
bullet(s, Inches(7.4), Inches(2.35), Inches(5.4),
    ['Headline demand: visit → email conversion rate',
     [('Price signal: ', 13.5, PLUM, True), ('$12/mo shown up-front to filter for willingness to pay', 13.5, INK, False)],
     'Message A/B: “on track before you quit” vs “feel like yourself again”',
     'Segment capture: newly-started vs considering; Canada vs US',
     [('Output: ', 13.5, PLUM, True), ('a real conversion number for Milestone #3 — the hardest slide to fake', 13.5, INK, False)]], size=13.5, gap=11)
txt(s, Inches(7.4), Inches(5.9), Inches(5.4), Inches(0.8),
    [[('Status: ', 12.5, ROSE, True), ('copy + design ready; live smoke-test with small paid traffic is the next build. [Insert live URL / QR before the talk].', 12.5, GREY, False, 'i')]], line_spacing=1.05)

# ============================================================ 12 DISCOVERY INTERVIEWS
s = slide(); header(s, 'DISCOVERY INTERVIEWS', '3 conversations so far — pain confirmed, two buyer signals', '12'); footer(s)
txt(s, Inches(0.6), Inches(1.4), Inches(12), Inches(0.5),
    [[('Interviews conducted to date: ', 15, PLUM, True), ('3', 15, ROSE, True),
      ('  (1 formal + 2 expert conversations).  Round of 19 planned: 5 pharmacists · 5 prescribers · 10 patients.', 14, INK, False)]])
iv = [
    ('1 · Community pharmacist (Canada)', PLUM,
     ['“Compliance is an issue for us.” — named it a real problem, unprompted',
      'Endorsed continuous tracking + patient education as the top levers',
      'Framed it as a chronic-medication need (fits our titration-season design)',
      'Signal: pharmacists can adapt/renew Rx in 7 CA provinces → possible channel']),
    ('2 · ENT physician (peer)', ROSE,
     ['Big-device tracking (sleep, weight) is already mature & trusted',
      'Suggested folding follow-up questions into that tracking',
      'Read both ways: validates the mechanism AND flags the device-maker threat',
      'Our answer: they’re the collection layer; we’re the treatment loop']),
    ('3 · Health-industry contact (US conf, last wk)', PLUM2,
     ['Reported: pharma actively wants post-prescription real-world data',
      'Directly validates our primary buyer (Astellas’ OPTION-VMS proves the spend)',
      'Turns the pharma line from hypothesis → corroborated signal',
      'Next: get a medical-affairs intro for price discovery']),
]
cx=Inches(0.6); cw=Inches(3.94); gap=Inches(0.14)
for i,(t,col,items) in enumerate(iv):
    x=Emu(int(cx)+i*(int(cw)+int(gap)))
    rect(s, x, Inches(2.05), cw, Inches(4.5), CARD, line=LINEC, line_w=Pt(1), round_=True)
    rect(s, x, Inches(2.05), cw, Inches(0.7), col, round_=False)
    txt(s, Emu(int(x)+Emu(Inches(0.15))), Inches(2.05), Emu(int(cw)-Emu(Inches(0.3))), Inches(0.7),
        [[(t, 12.5, WHITE, True)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=0.98)
    bullet(s, Emu(int(x)+Emu(Inches(0.18))), Inches(2.9), Emu(int(cw)-Emu(Inches(0.36))), items, size=11.5, gap=7)
txt(s, Inches(0.6), Inches(6.75), Inches(12.1), Inches(0.4),
    [[('Honest read: ', 12, PLUM, True), ('small n, some primed questions. Next round asks only about past behaviour (Mom Test) and probes willingness to pay.', 12, GREY, False, 'i')]])

# ============================================================ 13 CLOSING / ASK
s = slide()
rect(s, 0, 0, SW, SH, PLUM)
rect(s, 0, Inches(2.2), SW, Pt(3), ROSE)
txt(s, Inches(0.9), Inches(0.8), Inches(11.5), Inches(1.2),
    [[('The one line', 15, ROSE, True)],
     [('Half of women quit hormone therapy in year one because', 26, WHITE, True)],
     [('no one records what happens between prescriptions. We do.', 26, WHITE, True)]], line_spacing=1.12)
txt(s, Inches(0.9), Inches(2.6), Inches(11.5), Inches(0.5), [[('Next 90 days', 15, GOLD, True)]])
bullet(s, Inches(0.9), Inches(3.15), Inches(11.5),
    [[('Validation: ', 15, ROSE, True), ('19 behaviour-based interviews + live landing-page smoke test (real conversion number)', 15, WHITE, False)],
     [('Data: ', 15, ROSE, True), ('buy a claims slice to nail annual new-starts and titration-change rates', 15, WHITE, False)],
     [('Buyers: ', 15, ROSE, True), ('one pharma medical-affairs intro (price discovery) + one clinic design partner', 15, WHITE, False)],
     [('Compliance: ', 15, ROSE, True), ('a $5–10k SaMD/regulatory scoping call on the red-flag boundary', 15, WHITE, False)]],
    size=15, gap=10)
txt(s, Inches(0.9), Inches(6.4), Inches(11.5), Inches(0.7),
    [[('Attune', 20, WHITE, True), ('  —  turning “dose by feel” into engineering.', 17, RGBColor(0xD9,0xC7,0xD2), False)]])

prs.save('/tmp/claude-0/-home-user-13-wishes/f0238e70-e502-5fa0-a299-1a7016d75faf/scratchpad/Attune_Milestone2.pptx')
print('saved', len(prs.slides.__iter__.__self__._sldIdLst), 'slides')
