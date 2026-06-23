import streamlit as st
import pandas as pd
import datetime
import random
import time

st.set_page_config(
    page_title="PhishGuard — Phishing Awareness Training",
    page_icon="logo.png",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #ffffff; color: #1a1a1a; }
    .main-title { font-family: 'Space Grotesk', sans-serif; font-size: 2.6rem; font-weight: 700; color: #1a1a1a; text-align: center; margin-bottom: 0.2rem; }
    .subtitle { font-size: 1rem; color: #555; text-align: center; margin-bottom: 2rem; }
    .feature-card { background: #f7f7f7; border-radius: 12px; padding: 1.2rem 1.4rem; border: 1px solid #e5e5e5; margin: 0.5rem 0; }
    .feature-card h4 { color: #111; margin: 0 0 0.3rem 0; font-size: 0.95rem; font-weight: 600; }
    .feature-card p { color: #555; margin: 0; font-size: 0.85rem; }
    .scenario-box { background: #fafafa; border-radius: 10px; padding: 1.3rem 1.5rem; border: 1px solid #e5e5e5; white-space: pre-wrap; line-height: 1.7; margin: 1rem 0; color: #333; font-family: 'Courier New', monospace; font-size: 0.88rem; }
    .feedback-correct { background: #e8f9ee; border-radius: 10px; padding: 1rem 1.5rem; border-left: 4px solid #22c55e; margin: 1rem 0; color: #14532d; }
    .feedback-wrong { background: #fde8e8; border-radius: 10px; padding: 1rem 1.5rem; border-left: 4px solid #ef4444; margin: 1rem 0; color: #7f1d1d; }
    .answer-correct { background: #e8f9ee; border-radius: 8px; padding: 0.8rem 1rem; border-left: 3px solid #22c55e; margin: 0.5rem 0; color: #14532d; font-size: 0.9rem; }
    .answer-wrong { background: #fde8e8; border-radius: 8px; padding: 0.8rem 1rem; border-left: 3px solid #ef4444; margin: 0.5rem 0; color: #7f1d1d; font-size: 0.9rem; }
    .progress-label { font-size: 0.82rem; color: #888; text-align: right; margin-bottom: 0.3rem; }
    .badge { font-size: 1rem; font-weight: 700; padding: 0.5rem 1.5rem; border-radius: 20px; display: inline-block; margin: 0.5rem 0; }
    .badge-advanced { background: #e8f9ee; color: #14532d; border: 1px solid #22c55e; }
    .badge-intermediate { background: #fef9c3; color: #92400e; border: 1px solid #f59e0b; }
    .badge-beginner { background: #fde8e8; color: #7f1d1d; border: 1px solid #ef4444; }
    .diff-easy { background: #e8f9ee; color: #14532d; padding: 2px 10px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; }
    .diff-medium { background: #fef9c3; color: #92400e; padding: 2px 10px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; }
    .diff-hard { background: #fde8e8; color: #7f1d1d; padding: 2px 10px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; }
    hr { border-color: #e5e5e5; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ===== QUESTIONS =====
PRE_QUESTIONS = [
    {"q": "What is phishing?", "options": ["A fishing sport", "A cyberattack that tricks users into revealing sensitive information", "A software bug", "A firewall technique"], "a": "A cyberattack that tricks users into revealing sensitive information"},
    {"q": "Which is a common sign of a phishing email?", "options": ["Personalized greeting with full name", "Urgent language demanding immediate action", "Email from a known colleague", "Professional company logo"], "a": "Urgent language demanding immediate action"},
    {"q": "What should you do before clicking a link in an email?", "options": ["Click it if it looks safe", "Check only the sender name", "Hover over the link to verify the real URL", "Forward it to friends first"], "a": "Hover over the link to verify the real URL"},
    {"q": "Which URL is most likely legitimate?", "options": ["https://kaspi-bank-security.com/verify", "https://kaspi.kz/account", "https://kaspi.support-login.net", "https://secure-kaspi-verify.com"], "a": "https://kaspi.kz/account"},
    {"q": "What is spear phishing?", "options": ["A phishing attack targeting a large random group", "A targeted attack on a specific person or organization", "A phishing attack via phone calls", "A type of malware"], "a": "A targeted attack on a specific person or organization"},
]

POST_QUESTIONS = [
    {"q": "Which psychological technique do phishing attacks most commonly use?", "options": ["Humor and entertainment", "Urgency and fear", "Logical reasoning", "Financial rewards only"], "a": "Urgency and fear"},
    {"q": "A delivery company emails asking for $1.99 to release your package. This is most likely:", "options": ["A legitimate delivery fee", "A phishing scam", "A loyalty reward", "A government customs tax"], "a": "A phishing scam"},
    {"q": "What does a phishing email often pretend to be?", "options": ["A random advertisement", "A trusted organization like a bank or university", "A personal blog post", "A software update from your own PC"], "a": "A trusted organization like a bank or university"},
    {"q": "Which is the safest action when receiving a suspicious email?", "options": ["Reply asking for more information", "Click the link to verify if it is real", "Delete it and report it as phishing", "Forward it to colleagues to check"], "a": "Delete it and report it as phishing"},
    {"q": "What is vishing?", "options": ["Phishing via fake websites", "Phishing via voice calls or phone", "Phishing via USB drives", "Phishing via social media messages"], "a": "Phishing via voice calls or phone"},
]

SCENARIOS = [
    {"id": 1, "type": "Banking Phishing", "difficulty": "Easy", "message": "From: security@kaspi-bank-verify.com\nSubject: Urgent: Suspicious Activity Detected\n\nDear Customer,\n\nWe detected suspicious login on your account.\nIt will be SUSPENDED in 24 hours unless you verify NOW:\n\nhttps://kaspi-bank-security.com/verify\n\nKaspi Bank Security Team", "is_phishing": True, "hint": "Look carefully at the email domain and the link URL.", "explanation": "PHISHING. The domain 'kaspi-bank-security.com' is fake — real Kaspi domain is kaspi.kz. Urgency is a classic pressure tactic."},
    {"id": 2, "type": "Fake Delivery Scam", "difficulty": "Easy", "message": "From: delivery@dhl-support-center.net\nSubject: Your package is waiting!!!\n\nYour package #KZ847291 could NOT be delivered!!!\nPay a $1.99 customs fee IMMEDIATELY:\n\nhttp://dhl-delivery-fee.com/pay\n\nDHL Support", "is_phishing": True, "hint": "Real delivery companies never ask for payment via email links.", "explanation": "PHISHING. Real delivery companies do not ask for payment via email links."},
    {"id": 3, "type": "Cryptocurrency Giveaway", "difficulty": "Easy", "message": "From: giveaway@elon-crypto-official.com\nSubject: YOU WON — Claim 0.5 BTC NOW\n\nCONGRATULATIONS!!!\nYou were randomly selected to receive 0.5 BTC.\n\nTo claim, send 0.01 BTC first:\nhttps://crypto-giveaway-official.com/claim\n\nHURRY — offer expires in 1 hour!", "is_phishing": True, "hint": "Would anyone really give you free Bitcoin?", "explanation": "PHISHING. No legitimate giveaway asks you to send money first."},
    {"id": 4, "type": "Legitimate Bank Email", "difficulty": "Easy", "message": "From: noreply@kaspi.kz\nSubject: Your monthly statement is ready\n\nDear Customer,\n\nYour monthly statement for October 2024 is now available.\nView it in the official Kaspi app or at kaspi.kz.\n\nDo not reply to this email.\n\nKaspi Bank", "is_phishing": False, "hint": "Check the sender domain. Does it ask you to click suspicious links?", "explanation": "LEGITIMATE. Email from official kaspi.kz domain. No suspicious links, no threats."},
    {"id": 5, "type": "Fake Microsoft Support", "difficulty": "Easy", "message": "From: support@microsoft-helpdesk-center.com\nSubject: CRITICAL: Your PC has a virus!!!\n\nWARNING! A critical virus was detected.\nCall IMMEDIATELY at +1-800-FAKE-NUM or click:\n\nhttps://microsoft-support-fix.com/scan\n\nMicrosoft Security Team", "is_phishing": True, "hint": "Does Microsoft contact users like this?", "explanation": "PHISHING. Microsoft never sends unsolicited virus alerts."},
    {"id": 6, "type": "University Account Suspension", "difficulty": "Medium", "message": "From: admin@university-portal-support.com\nSubject: Student account update required\n\nDear Student,\n\nAll students must verify credentials by Friday.\n\nhttps://university-account-reset.com/login\n\nIT Department", "is_phishing": True, "hint": "Is this the official university domain?", "explanation": "PHISHING. Real university emails come from official domains, not 'university-portal-support.com'."},
    {"id": 7, "type": "Instagram Verification", "difficulty": "Medium", "message": "From: security@instagram-verify-account.com\nSubject: Action required on your Instagram\n\nUnusual activity detected. Verify within 12 hours:\n\nhttps://instagram-account-confirm.com\n\nInstagram Security Team", "is_phishing": True, "hint": "What is Instagram's real domain?", "explanation": "PHISHING. Real Instagram emails come from instagram.com."},
    {"id": 8, "type": "Fake Job Offer", "difficulty": "Medium", "message": "From: hr@google-careers-hiring.com\nSubject: Job opportunity at Google\n\nRemote position at Google — $4,500/month.\nPay a $50 processing fee to proceed:\nhttps://google-jobs-apply.com/register\n\nGoogle HR Team", "is_phishing": True, "hint": "Does any real company charge application fees?", "explanation": "PHISHING. Legitimate companies never charge fees."},
    {"id": 9, "type": "Legitimate Password Reset", "difficulty": "Medium", "message": "From: noreply@github.com\nSubject: Reset your GitHub password\n\nWe received a reset request. Click within 1 hour:\n\nhttps://github.com/password_reset/token_abc123\n\nIf you did not request this, ignore this email.\n\nGitHub Security", "is_phishing": False, "hint": "Where does the email come from and where does the link go?", "explanation": "LEGITIMATE. From github.com, link goes to github.com. No threats."},
    {"id": 10, "type": "QR Code Phishing", "difficulty": "Medium", "message": "From: rewards@starbucks-loyalty-program.net\nSubject: Your free drink reward is waiting\n\nClaim your free drink before it expires:\nhttps://starbucks-free-reward.com/qr-scan\n\nOffer expires in 48 hours.\n\nStarbucks Rewards Team", "is_phishing": True, "hint": "Is this the official Starbucks domain?", "explanation": "PHISHING. 'starbucks-loyalty-program.net' is not starbucks.com."},
    {"id": 11, "type": "Spear Phishing — University", "difficulty": "Hard", "message": "From: hr.department@sdu-edu.kz\nSubject: Scholarship application shortlisted\n\nYour scholarship has been shortlisted.\nConfirm your details by December 1st:\n\nhttps://sdu-edu.kz/scholarship/confirm\n\nKeep this confidential.\n\nScholarship Committee", "is_phishing": True, "hint": "Compare sender domain to the real sdu.edu.kz very carefully.", "explanation": "PHISHING. 'sdu-edu.kz' uses dash instead of dot. Real domain is sdu.edu.kz."},
    {"id": 12, "type": "Smishing — Bank SMS", "difficulty": "Hard", "message": "SMS from: Halyk Bank\n\nA new device was linked to your account.\nCancel immediately:\nhttps://halyk.kz-secure-login.com/cancel\n\nHalyk Bank Security", "is_phishing": True, "hint": "Look very carefully at the full URL.", "explanation": "PHISHING. The real domain is 'kz-secure-login.com', not halyk.kz. Subdomain attack."},
    {"id": 13, "type": "Legitimate University Email", "difficulty": "Hard", "message": "From: registrar@sdu.edu.kz\nSubject: Transcript request — action required\n\nYour transcript request was processed.\nConfirm delivery address within 5 business days:\n\nhttps://portal.sdu.edu.kz/transcripts\n\nRegistrar Office\nSuleyman Demirel University", "is_phishing": False, "hint": "Check both the sender and link domain.", "explanation": "LEGITIMATE. Both sender and link use official sdu.edu.kz domain."},
    {"id": 14, "type": "Vishing — Fake Bank Call", "difficulty": "Hard", "message": "[Voicemail]\n\nThis is Sarah from Kaspi Bank fraud prevention.\nWe placed a hold on your account.\n\nCall back: +7 (727) 259-0000\nOr visit: https://kaspi.kz/verify", "is_phishing": True, "hint": "Should you call back a number from a fraud voicemail?", "explanation": "PHISHING. Real banks never ask you to call a voicemail number."},
    {"id": 15, "type": "CEO Fraud", "difficulty": "Hard", "message": "From: ceo@yourcompany-group.com\nSubject: Urgent — Confidential transfer\n\nI am in a meeting. Process a $3,200 wire transfer today.\nDo not discuss with others until done.\n\nDavid Chen\nCEO", "is_phishing": True, "hint": "Why must this be confidential? Why email instead of call?", "explanation": "PHISHING. CEO fraud. Always verify financial requests through a separate channel."},
]

# ===== INIT SESSION STATE =====
def init_state():
    defaults = {
        'page': 'home',
        'name': '',
        'difficulty': 'Easy',
        'pre_score': 0,
        'post_score': 0,
        'training_score': 0,
        'current': 0,
        'answers': [],
        'pre_answers': [],
        'post_answers': [],
        'show_feedback': False,
        'last_correct': None,
        'last_explanation': '',
        'filtered_scenarios': [],
        'timer_start': None,
        'time_taken': [],
        'show_pre_results': False,
        'show_post_results': False,
        'post_submitted': False,
        'pre_submitted': False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def clear_radio_keys():
    for i in range(len(PRE_QUESTIONS)):
        st.session_state.pop(f"pre_{i}", None)
    for i in range(len(POST_QUESTIONS)):
        st.session_state.pop(f"post_{i}", None)

# ===== SIDEBAR =====
with st.sidebar:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("logo.png", width=50)
    with col2:
        st.markdown("### PhishGuard")
    st.markdown("---")

    nav_items = [
        ("home.png",     "Home",           "home"),
        ("about.png",    "About Phishing", "about"),
        ("pretest.png",  "Pre-Test",       "pretest"),
        ("training.png", "Training",       "trainer"),
        ("posttest.png", "Post-Test",      "posttest"),
        ("results.png",  "Results",        "results"),
    ]

    for icon, label, pg in nav_items:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(icon, width=22)
        with col2:
            # Home and About always accessible
            if pg in ["home", "about"]:
                if st.button(label, use_container_width=True, key=f"nav_{pg}"):
                    st.session_state.page = pg
                    st.rerun()
            else:
                # Other pages need name
                if st.session_state.name:
                    if st.button(label, use_container_width=True, key=f"nav_{pg}"):
                        st.session_state.page = pg
                        st.rerun()
                else:
                    st.button(label, use_container_width=True, key=f"nav_{pg}", disabled=True)

    st.markdown("---")
    if st.session_state.name:
        st.success(f"User: {st.session_state.name}")
    diff = st.session_state.difficulty
    color = "🟢" if diff == "Easy" else "🟡" if diff == "Medium" else "🔴"
    st.info(f"{color} Difficulty: **{diff}**")
    st.markdown("---")
    st.caption("PhishGuard v2.0 | Bachelor Thesis")

# ===== PAGE ROUTING =====
page = st.session_state.page

# ===== HOME =====
if page == "home":
    # Logo centered
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image("logo.png", width=120)

    st.markdown('<div class="main-title">PhishGuard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Interactive Phishing Awareness Training System</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.info("**Purpose:** To improve phishing awareness through interactive scenario-based learning. The system evaluates user knowledge before and after training to measure improvement.")
    st.markdown("---")

    # Feature cards with icons and buttons
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.image("about.png", width=50)
        st.markdown('<div class="feature-card"><h4>Theory</h4><p>Learn about phishing types</p></div>', unsafe_allow_html=True)
        if st.button("Learn More", key="home_about", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
    with c2:
        st.image("pretest.png", width=50)
        st.markdown('<div class="feature-card"><h4>Pre-Test</h4><p>Measure your starting level</p></div>', unsafe_allow_html=True)
        if st.session_state.name:
            if st.button("Start Pre-Test", key="home_pretest", use_container_width=True):
                st.session_state.page = "pretest"
                st.rerun()
        else:
            st.caption("Enter your name first")
    with c3:
        st.image("training.png", width=50)
        st.markdown('<div class="feature-card"><h4>Training</h4><p>15 real-world scenarios</p></div>', unsafe_allow_html=True)
        if st.session_state.name:
            if st.button("Go to Training", key="home_trainer", use_container_width=True):
                st.session_state.page = "trainer"
                st.rerun()
        else:
            st.caption("Enter your name first")
    with c4:
        st.image("results.png", width=50)
        st.markdown('<div class="feature-card"><h4>Results</h4><p>Track your improvement</p></div>', unsafe_allow_html=True)
        if st.session_state.name:
            if st.button("View Results", key="home_results", use_container_width=True):
                st.session_state.page = "results"
                st.rerun()
        else:
            st.caption("Enter your name first")

    st.markdown("---")
    st.subheader("Enter your name")
    name = st.text_input("", st.session_state.name, placeholder="e.g. Aizat Bekova", label_visibility="collapsed")
    st.subheader("Choose difficulty level")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🟢 Easy — Obvious signs", use_container_width=True):
            st.session_state.difficulty = "Easy"; st.rerun()
    with c2:
        if st.button("🟡 Medium — Less obvious", use_container_width=True):
            st.session_state.difficulty = "Medium"; st.rerun()
    with c3:
        if st.button("🔴 Hard — Realistic", use_container_width=True):
            st.session_state.difficulty = "Hard"; st.rerun()
    st.markdown(f"**Selected:** {st.session_state.difficulty}")

    if st.button("Start Training", type="primary", use_container_width=True):
        if name.strip():
            clear_radio_keys()
            st.session_state.name = name.strip()
            filtered = [s for s in SCENARIOS if s['difficulty'] == st.session_state.difficulty]
            random.shuffle(filtered)
            st.session_state.filtered_scenarios = filtered
            st.session_state.current = 0
            st.session_state.answers = []
            st.session_state.training_score = 0
            st.session_state.show_feedback = False
            st.session_state.time_taken = []
            st.session_state.show_pre_results = False
            st.session_state.show_post_results = False
            st.session_state.pre_answers = []
            st.session_state.post_answers = []
            st.session_state.pre_score = 0
            st.session_state.post_score = 0
            st.session_state.timer_start = None
            st.session_state.page = "pretest"
            st.rerun()
        else:
            st.error("Please enter your name to continue.")

# ===== ABOUT =====
elif page == "about":
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("about.png", width=45)
    with col2:
        st.title("About Phishing")
    st.markdown("---")
    st.markdown("## What is Phishing?\nPhishing is a cyberattack where attackers **disguise themselves as trusted entities** to steal sensitive information. It targets the **human factor** — using psychology to manipulate people.")
    st.markdown("---")
    st.subheader("Types of Phishing Attacks")
    c1, c2 = st.columns(2)
    with c1:
        st.error("**Email Phishing** — Mass emails pretending to be banks or companies.")
        st.error("**Spear Phishing** — Targeted attack using personal information.")
        st.error("**Smishing** — Phishing via SMS messages.")
    with c2:
        st.error("**Vishing** — Fake phone calls pretending to be support teams.")
        st.error("**Quishing** — Phishing via QR codes.")
        st.error("**CEO Fraud** — Impersonating executives for money transfers.")
    st.markdown("---")
    st.subheader("Why Do People Fall for Phishing?")
    st.info("**Urgency** — 'Your account will be deleted!'\n\n**Authority** — Pretending to be a bank or government\n\n**Fear** — Threatening consequences\n\n**Trust** — Using familiar logos\n\n**Curiosity** — 'You have a package waiting'")
    st.markdown("---")
    st.subheader("How to Spot Phishing")
    st.success("Check the sender's email domain carefully\nHover over links to see the real URL\nBe suspicious of urgent language\nNever share passwords via email or phone\nContact organizations through official channels")
    if not st.session_state.name:
        st.warning("Please enter your name on the Home page before starting the test.")
        if st.button("Go to Home", type="primary", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    else:
        if st.button("Go to Pre-Test", type="primary", use_container_width=True):
            st.session_state.page = "pretest"
            st.rerun()

# ===== PRE-TEST =====
elif page == "pretest":
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("pretest.png", width=45)
    with col2:
        st.title("Pre-Test")

    if st.session_state.show_pre_results:
        st.success(f"Pre-Test Complete! Score: **{st.session_state.pre_score}/{len(PRE_QUESTIONS)}**")
        st.markdown("### Answer Review")
        for i, q in enumerate(PRE_QUESTIONS):
            user_ans = st.session_state.pre_answers[i]
            correct_ans = q['a']
            if user_ans == correct_ans:
                st.markdown(f'<div class="answer-correct">Correct — Q{i+1}: {q["q"]}<br><strong>Your answer:</strong> {user_ans}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="answer-wrong">Incorrect — Q{i+1}: {q["q"]}<br><strong>Your answer:</strong> {user_ans}<br><strong>Correct answer:</strong> {correct_ans}</div>', unsafe_allow_html=True)
        st.markdown("---")
        if st.button("Start Training", type="primary", use_container_width=True):
            clear_radio_keys()
            st.session_state.show_pre_results = False
            st.session_state.timer_start = None
            st.session_state.page = "trainer"
            st.rerun()
    else:
        st.markdown("Answer these questions **before** training.")
        st.markdown("---")
        answers = []
        for i, q in enumerate(PRE_QUESTIONS):
            st.markdown(f"**Question {i+1}:** {q['q']}")
            ans = st.radio("", q["options"], key=f"pre_{i}", index=None)
            answers.append(ans)
            st.markdown("")
        if st.button("Submit Pre-Test", type="primary", use_container_width=True):
            if None in answers:
                st.error("Please answer all questions.")
            elif not st.session_state.get('pre_submitted'):
                st.session_state.pre_submitted = True
                st.session_state.pre_score = sum(1 for i, q in enumerate(PRE_QUESTIONS) if answers[i] == q["a"])
                st.session_state.pre_answers = list(answers)
                st.session_state.show_pre_results = True
                st.rerun()

# ===== TRAINER =====
elif page == "trainer":
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("training.png", width=45)
    with col2:
        st.title("Phishing Training Simulator")

    scenarios = st.session_state.filtered_scenarios
    if not scenarios:
        scenarios = [s for s in SCENARIOS if s['difficulty'] == st.session_state.difficulty]
        random.shuffle(scenarios)
        st.session_state.filtered_scenarios = scenarios

    if st.session_state.current >= len(scenarios):
        st.session_state.page = "posttest"
        st.rerun()
        st.stop()

    if st.session_state.show_feedback:
        if st.session_state.last_correct:
            st.markdown(f'<div class="feedback-correct">Correct! {st.session_state.last_explanation}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feedback-wrong">Incorrect. {st.session_state.last_explanation}</div>', unsafe_allow_html=True)
        if st.button("Next Scenario", type="primary", use_container_width=True):
            st.session_state.show_feedback = False
            st.session_state.timer_start = None
            st.rerun()
        st.stop()

    sc = scenarios[st.session_state.current]
    st.markdown(f'<div class="progress-label">Scenario {st.session_state.current + 1} of {len(scenarios)}</div>', unsafe_allow_html=True)
    st.progress(st.session_state.current / len(scenarios))

    diff_class = f"diff-{sc['difficulty'].lower()}"
    st.markdown(f"**Type:** `{sc['type']}` &nbsp;<span class='{diff_class}'>{sc['difficulty']}</span>", unsafe_allow_html=True)
    st.markdown(f'<div class="scenario-box">{sc["message"]}</div>', unsafe_allow_html=True)

    with st.expander("Show hint"):
        st.info(sc['hint'])

    st.markdown("**Is this message phishing or legitimate?**")
    c1, c2 = st.columns(2)
    scenario_key = f"sc_{st.session_state.current}"
    with c1:
        if st.button("PHISHING", type="primary", use_container_width=True, key=f"phishing_{scenario_key}"):
            correct = sc['is_phishing']
            st.session_state.training_score += 1 if correct else 0
            st.session_state.answers.append({"type": sc['type'], "difficulty": sc['difficulty'], "correct": correct, "explanation": sc['explanation']})
            st.session_state.time_taken.append(0)
            st.session_state.show_feedback = True
            st.session_state.last_correct = correct
            st.session_state.last_explanation = sc['explanation']
            st.session_state.current += 1
            st.rerun()
    with c2:
        if st.button("LEGITIMATE", use_container_width=True, key=f"legit_{scenario_key}"):
            correct = not sc['is_phishing']
            st.session_state.training_score += 1 if correct else 0
            st.session_state.answers.append({"type": sc['type'], "difficulty": sc['difficulty'], "correct": correct, "explanation": sc['explanation']})
            st.session_state.time_taken.append(0)
            st.session_state.show_feedback = True
            st.session_state.last_correct = correct
            st.session_state.last_explanation = sc['explanation']
            st.session_state.current += 1
            st.rerun()
    st.stop()

# ===== POST-TEST =====
elif page == "posttest":
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("posttest.png", width=45)
    with col2:
        st.title("Post-Test")

    ts = len(st.session_state.filtered_scenarios) if st.session_state.filtered_scenarios else 5
    st.success(f"Training complete! Score: {st.session_state.training_score}/{ts}")

    if st.session_state.show_post_results:
        st.markdown(f"### Your score: **{st.session_state.post_score}/{len(POST_QUESTIONS)}**")
        st.markdown("### Answer Review")
        for i, q in enumerate(POST_QUESTIONS):
            user_ans = st.session_state.post_answers[i]
            correct_ans = q['a']
            if user_ans == correct_ans:
                st.markdown(f'<div class="answer-correct">Correct — Q{i+1}: {q["q"]}<br><strong>Your answer:</strong> {user_ans}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="answer-wrong">Incorrect — Q{i+1}: {q["q"]}<br><strong>Your answer:</strong> {user_ans}<br><strong>Correct answer:</strong> {correct_ans}</div>', unsafe_allow_html=True)
        st.markdown("---")
        if st.button("View Full Results", type="primary", use_container_width=True):
            clear_radio_keys()
            st.session_state.show_post_results = False
            st.session_state.page = "results"
            st.rerun()
    else:
        st.markdown("Answer similar questions **after** training.")
        st.markdown("---")
        answers = []
        for i, q in enumerate(POST_QUESTIONS):
            st.markdown(f"**Question {i+1}:** {q['q']}")
            ans = st.radio("", q["options"], key=f"post_{i}", index=None)
            answers.append(ans)
            st.markdown("")
        if st.button("Submit Post-Test", type="primary", use_container_width=True):
            if None in answers:
                st.error("Please answer all questions.")
            elif not st.session_state.get('post_submitted'):
                st.session_state.post_submitted = True
                st.session_state.post_score = sum(1 for i, q in enumerate(POST_QUESTIONS) if answers[i] == q["a"])
                st.session_state.post_answers = list(answers)
                st.session_state.show_post_results = True
                result = {
                    "name": st.session_state.name,
                    "difficulty": st.session_state.difficulty,
                    "pre_score": st.session_state.pre_score,
                    "training_score": st.session_state.training_score,
                    "post_score": st.session_state.post_score,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                df = pd.DataFrame([result])
                df.to_csv("results.csv", mode='a', header=not pd.io.common.file_exists("results.csv"), index=False)
                st.rerun()

# ===== RESULTS =====
elif page == "results":
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("results.png", width=45)
    with col2:
        st.title("Your Results")

    st.markdown(f"### User: {st.session_state.name} | Difficulty: {st.session_state.difficulty}")
    st.markdown("---")
    pre = st.session_state.pre_score
    training = st.session_state.training_score
    post = st.session_state.post_score
    tq = len(PRE_QUESTIONS)
    ts = len(st.session_state.filtered_scenarios) if st.session_state.filtered_scenarios else 5
    c1, c2, c3 = st.columns(3)
    c1.metric("Pre-Test", f"{pre}/{tq}", f"{round(pre/tq*100)}%")
    c2.metric("Training", f"{training}/{ts}", f"{round(training/ts*100)}%")
    c3.metric("Post-Test", f"{post}/{tq}", f"{round(post/tq*100)}%")
    st.markdown("---")
    st.subheader("Your Progress")
    chart_data = pd.DataFrame({"Score (%)": [round(pre/tq*100), round(training/ts*100), round(post/tq*100)]}, index=["Pre-Test", "Training", "Post-Test"])
    st.bar_chart(chart_data)
    st.markdown("---")
    st.subheader("Awareness Level")
    avg = (pre/tq + post/tq) / 2 * 100
    if avg >= 80:
        st.markdown('<div class="badge badge-advanced">Advanced — Excellent awareness!</div>', unsafe_allow_html=True)
    elif avg >= 50:
        st.markdown('<div class="badge badge-intermediate">Intermediate — Good, keep learning!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge badge-beginner">Beginner — More training recommended</div>', unsafe_allow_html=True)
    improvement = post - pre
    if improvement > 0:
        st.success(f"You improved by {improvement} point(s) after training!")
    elif improvement == 0:
        st.info("Your score stayed the same. Review the explanations below.")
    else:
        st.warning("Post-test score was lower. Try a different difficulty level.")
    st.markdown("---")
    st.subheader("Training Review")
    correct_count = sum(1 for a in st.session_state.answers if a['correct'])
    wrong_count = sum(1 for a in st.session_state.answers if not a['correct'])
    c1, c2 = st.columns(2)
    c1.metric("Correct", correct_count)
    c2.metric("Incorrect", wrong_count)
    for ans in st.session_state.answers:
        if ans['correct']:
            with st.expander(f"✅ Correct — {ans['type']} ({ans['difficulty']})"):
                st.success(ans['explanation'])
        else: 
             with st.expander(f"❌ Incorrect — {ans['type']} ({ans['difficulty']})"):
                 st.error(ans['explanation'])

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        result_df = pd.DataFrame([{
            "Name": st.session_state.name,
            "Difficulty": st.session_state.difficulty,
            "Pre-Test": f"{pre}/{tq}",
            "Training": f"{training}/{ts}",
            "Post-Test": f"{post}/{tq}",
            "Awareness Level": "Advanced" if avg >= 80 else "Intermediate" if avg >= 50 else "Beginner",
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }])
        st.download_button("Download My Results", result_df.to_csv(index=False), "my_phishing_results.csv", use_container_width=True)
    with c2:
        if st.button("Try Again", use_container_width=True):
            clear_radio_keys()
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
