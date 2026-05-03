"""
Smart Python Assistant (CLI)
Copyright (c) 2026 Kavyant Kumar
All rights reserved.

Author  : Kavyant Kumar (Cares & Laughs – Your Fun Lab / CareLabStudio)
Version : 10.0.0
Year    : 2026
Location: Ghaziabad, Uttar Pradesh, Sector 2, Block A, Flat 101 1/33 Rajendar Nagar,  India

Setup (run this in your terminal/command prompt before using):

  On Windows (with 'py' launcher):
      py -m pip install wikipedia
      py -m pip install sympy

  On Linux / macOS (python3):
      python3 -m pip install wikipedia
      python3 -m pip install sympy
"""

__version__ = "10.0.0"

import wikipedia
from sympy import symbols, Eq, solve, sympify
from sympy import simplify, factor, expand
import datetime
import random
import webbrowser
import time
import json  # for saving/loading tasks + formulas
import os

# ---------- Optional Windows beep support ----------
try:
    import winsound  # Windows-only
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# ---------- Beep configuration ----------
BEEP_FREQ = 1000  # Hz (37–32767 on Windows)
BEEP_DUR = 300    # milliseconds

def play_beep(freq=None, dur=None):
    freq = freq or BEEP_FREQ
    dur = dur or BEEP_DUR
    if HAS_WINSOUND and os.name == "nt":
        winsound.Beep(freq, dur)
    else:
        # Fallback: terminal bell
        print("\a", end="")

def set_beep_settings(freq: int, dur: int):
    global BEEP_FREQ, BEEP_DUR
    BEEP_FREQ = freq
    BEEP_DUR = dur

# ---------- Site shortcuts ----------
sites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "wikipedia": "https://www.wikipedia.org",
    "github": "https://github.com",
    "stackoverflow": "https://stackoverflow.com",
    "gmail": "https://mail.google.com",
    "instagram": "https://www.instagram.com",
    "reddit": "https://www.reddit.com",
    "codepen": "https://codepen.io",
    "perplexity": "https://www.perplexity.ai",
    "chatgpt": "https://chat.openai.com",
    "whatsapp": "https://web.whatsapp.com",
    "discord": "https://discord.com/app",
    "spotify": "https://open.spotify.com",
    "netflix": "https://www.netflix.com",
    "twitter": "https://twitter.com",
    "x": "https://twitter.com",
    "facebook": "https://www.facebook.com",
    "linkedin": "https://www.linkedin.com",
    "drive": "https://drive.google.com",
    "docs": "https://docs.google.com/document/u/0/",
    "sheets": "https://docs.google.com/spreadsheets/u/0/",
    "slides": "https://docs.google.com/presentation/u/0/",
    "classroom": "https://classroom.google.com",
    "meet": "https://meet.google.com",

    # coding / dev
    "geeksforgeeks": "https://www.geeksforgeeks.org",
    "w3schools": "https://www.w3schools.com",
    "leetcode": "https://leetcode.com",
    "hackerrank": "https://www.hackerrank.com",
    "codeforces": "https://codeforces.com",
    "kaggle": "https://www.kaggle.com",
    "github_gist": "https://gist.github.com",
    "mdn": "https://developer.mozilla.org",
    "pypi": "https://pypi.org",

    # design / productivity
    "canva": "https://www.canva.com",
    "figma": "https://www.figma.com",
    "notion": "https://www.notion.so",
    "toggl": "https://track.toggl.com",

    # learning platforms (core)
    "udemy": "https://www.udemy.com",
    "coursera": "https://www.coursera.org",
    "khan": "https://www.khanacademy.org",
    "nptel": "https://nptel.ac.in",
    "byjus": "https://byjus.com",
    "pw": "https://www.pw.live",
    "allen": "https://www.allen.ac.in",
    "unacademy": "https://unacademy.com",
    "cbse": "https://www.cbse.gov.in",
    "nta": "https://www.nta.ac.in",
    "jeemain": "https://jeemain.nta.nic.in",
    "jeeadvanced": "https://jeeadv.ac.in",

    # coding envs / ML
    "replit": "https://replit.com",
    "glitch": "https://glitch.com",
    "colab": "https://colab.research.google.com",
    "huggingface": "https://huggingface.co",

    # your search
    "cares_search": "https://codepen.io/Kavyant-Kumar/pen/vEXPVmb",

    # extra JEE / study
    "nta_lectures": "https://nta.ac.in/lecturesContent",
    "iitpal": "https://nta.ac.in/lecturesContent",
    "quizlet": "https://quizlet.com",

    # extra coding practice
    "gfg_practice": "https://practice.geeksforgeeks.org",
    "codechef": "https://www.codechef.com",
    "freecodecamp": "https://www.freecodecamp.org",

    # your custom links
    "cares": "https://codepen.io/Kavyant-Kumar/pen/dPGJPKj?",
    "kavyanthub": "https://www.instagram.com/kavyanthub/",
    "carelabstudio": "https://www.youtube.com/@CareLabStudio",
    "rickroll": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",

    # browsers / search engines
    "brave": "https://search.brave.com",
    "chrome": "https://www.google.com/chrome",
    "duckduckgo": "https://duckduckgo.com",
    "bing": "https://www.bing.com",

    # extra JEE / NEET / study
    "vedantu": "https://www.vedantu.com",
    "embibe": "https://www.embibe.com",
    "toppr": "https://www.toppr.com",
    "doubtnut": "https://www.doubtnut.com",
    "physics_wallah": "https://www.pw.live",
    "aakash": "https://www.aakash.ac.in",
    "fiitjee": "https://www.fiitjee.com",
    "resonance": "https://www.resonance.ac.in",
    "career360": "https://www.careers360.com",
    "exam_fear": "https://www.examfear.com",

    # official education / gov
    "ncert": "https://ncert.nic.in",
    "diksha": "https://diksha.gov.in",
    "swayam": "https://swayam.gov.in",
    "epathshala": "https://epathshala.nic.in",
    "nios": "https://www.nios.ac.in",

    # math tools
    "brilliant": "https://brilliant.org",
    "wolfram": "https://www.wolframalpha.com",
    "mathway": "https://www.mathway.com",
    "symbolab": "https://www.symbolab.com",
    "desmos": "https://www.desmos.com",
    "geogebra": "https://www.geogebra.org",

    # physics / chemistry resources
    "phet": "https://phet.colorado.edu",
    "hyperphysics": "http://hyperphysics.phy-astr.gsu.edu",
    "chemguide": "https://www.chemguide.co.uk",

    # YouTube education channels
    "khan_academy_yt": "https://www.youtube.com/@khanacademy",
    "physics_wallah_yt": "https://www.youtube.com/@PhysicsWallah",
    "unacademy_yt": "https://www.youtube.com/@UnacademyLive",
    "byju_yt": "https://www.youtube.com/@BYJUS",
    "vedantu_yt": "https://www.youtube.com/@VedantuEnglish",

    # study tools / coding / misc
    "anki": "https://apps.ankiweb.net",
    "quizizz": "https://quizizz.com",
    "photomath": "https://photomath.com",
    "study_tonight": "https://www.studytonight.com",
    "javatpoint": "https://www.javatpoint.com",
    "tutorialspoint": "https://www.tutorialspoint.com",
    "atcoder": "https://atcoder.jp",
    "topcoder": "https://www.topcoder.com",
    "projecteuler": "https://projecteuler.net",
    "codewars": "https://www.codewars.com",
    "exercism": "https://exercism.org",

    # --- general AI chatbots ---
    "gemini": "https://gemini.google.com",
    "copilot": "https://copilot.microsoft.com",
    "claude": "https://claude.ai",
    "sarvam": "https://sarvam.ai",
    "grok": "https://grok.com",
    "deepseek": "https://chat.deepseek.com",
    "pi_ai": "https://pi.ai",
    "reka": "https://chat.reka.ai",
    "poe": "https://poe.com",
    "blackbox_ai": "https://www.blackbox.ai",
    "phind": "https://www.phind.com",

    # --- coding assistants ---
    "github_copilot": "https://github.com/features/copilot",
    "cursor": "https://www.cursor.com",
    "amazon_q": "https://aws.amazon.com/q/developer/",
    "jetbrains_ai": "https://www.jetbrains.com/ai/",
    "tabnine": "https://www.tabnine.com",
    "replit_agent": "https://replit.com/ai",
    "augment_code": "https://www.augmentcode.com",
    "aider": "https://aider.chat",

    # --- image / design / art ---
    "midjourney": "https://www.midjourney.com",
    "leonardo": "https://leonardo.ai",
    "dalle": "https://labs.openai.com",
    "ideogram": "https://ideogram.ai",
    "playgroundai": "https://playground.com",
    "canva_magic": "https://www.canva.com/ai-image-generator",

    # --- video / image-to-video ---
    "runway": "https://runwayml.com",
    "pika": "https://pika.art",
    "imagineart": "https://imagine.art",
    "veo": "https://labs.google/veo",
    "sora": "https://openai.com/sora",
    "kling": "https://klingai.com",

    # --- voice, meetings, notes ---
    "otter": "https://otter.ai",
    "fireflies": "https://fireflies.ai",
    "tldv": "https://tldv.io",
    "scribe": "https://scribehow.com",

    # --- presentation / docs AI ---
    "tome": "https://beta.tome.app",
    "gamma": "https://gamma.app",
    "slidesai": "https://www.slidesai.io",
    "notion_ai": "https://www.notion.so/product/ai",

    # --- official safety links (India) ---
    "india_helplines": "https://www.india.gov.in/directory/helpline",
    "staysafeonline": "https://www.mygov.in/staysafeonline",
    "cyber_safety_tips": "https://cybercrime.gov.in/Webform/Crime_OnlineSafetyTips.aspx",

    # extra global learning / courses
    "edx": "https://www.edx.org",
    "udacity": "https://www.udacity.com",
    "academicearth": "https://academicearth.org",
    "classcentral": "https://www.classcentral.com",
    "skillup": "https://www.simplilearn.com/skillup-free-online-courses",
    "simplilearn": "https://www.simplilearn.com",

    # language learning
    "duolingo": "https://www.duolingo.com",
    "memrise": "https://www.memrise.com",
    "busuu": "https://www.busuu.com",
    "lingq": "https://www.lingq.com",
    "vocabulary": "https://www.vocabulary.com",

    # reading / OER
    "openlibrary": "https://openlibrary.org",
    "gutenberg": "https://www.gutenberg.org",
    "wikibooks": "https://www.wikibooks.org",
    "wikiversity": "https://www.wikiversity.org",
    "oercommons": "https://www.oercommons.org",
    "openlearn": "https://www.open.edu/openlearn/",
    "alison": "https://alison.com",

    # science / space
    "sciencebuddies": "https://www.sciencebuddies.org",
    "exploratorium": "https://www.exploratorium.edu",
    "nasaeducation": "https://science.nasa.gov/learn",
    "earthobservatory": "https://earthobservatory.nasa.gov",
    "smithsonianlearning": "https://learninglab.si.edu",
    "nationalgeographickids": "https://kids.nationalgeographic.com",
    "britannica_online": "https://www.britannica.com",

    # learning videos
    "teded": "https://ed.ted.com",
    "ted": "https://www.ted.com"
}
# ---------- Command descriptions (for help) ----------
commands = {
    "wiki <topic>": "Wikipedia summary",
    "math": "Solve equations / simplify expressions",
    "open <site>": "Open websites like youtube, google, cares, gemini, chatgpt, etc.",
    "sites": "List all site shortcuts you can open",
    "time / date / day": "Show current time, date, or day",
    "joke": "Random programming/maths joke",
    "meme": "Print a random coding / student meme line",
    "motivate": "Short motivation for study/coding",
    "reminder add <text>": "Add a reminder (only in memory)",
    "reminder list": "List your reminders",
    "note add <text>": "Save a note to notes.txt",
    "note list": "Show all notes",
    "note search <word>": "Search word in notes",
    "task add <text>": "Add a task to your to-do list",
    "task list": "Show all tasks",
    "task done <n>": "Mark task number n as done",
    "task save/load": "Save or load tasks to/from tasks.json",
    "jee formula <topic>": "Show built-in formulas (physics + maths)",
    "jee load": "Load 1200-formula JEE book from JSON",
    "jee topics": "List topics in 1200-formula book",
    "jee topic <name>": "Show formulas for one topic (from 1200-formula book)",
    "jee search <keyword>": "Search formulas in the 1200-formula book",
    "focus <minutes>": "Start a focus timer",
    "timer <seconds>": "Countdown timer that beeps when time is up",
    "beep set <freq> <ms>": "Set custom beep frequency (Hz) and duration (ms)",
    "beep test": "Play a test beep with current settings",
    "history last": "Show your last few commands",
    "history stats": "Show simple usage stats",
    "game": "Play guess-the-number",
    "fun": "Hints about secret Easter eggs",
    "safety": "Show India safety tips, helplines & lab rules",
    "setup": "Show how to install wikipedia & sympy",
    "shortcuts": "Show useful command & site shortcuts",
    "terms": "Show terms & conditions of this lab",
    "version": "Show assistant version",
    "copyright": "Show copyright notice",
    "help": "Show this help menu",
    "about": "About this assistant",
    "credits": "Show credits for this project",
}

# ---------- Core JEE formulas ----------
jee_formulas = {
    "kinematics": [
        "v = u + at",
        "s = ut + 1/2 at^2",
        "v^2 = u^2 + 2as",
        "average speed = total distance / total time",
        "a = (v - u) / t",
    ],
    "laws_of_motion": [
        "F = m a",
        "ΣF = 0 for equilibrium",
        "friction f = μ N",
    ],
    "work_energy": [
        "W = F · s · cos(θ)",
        "K = 1/2 m v^2",
        "U = m g h",
        "E (mechanical) = K + U",
        "W(net) = ΔK (work–energy theorem)",
    ],
    "gravitation": [
        "F = G m1 m2 / r^2",
        "g = G M / R^2",
        "U = -G M m / r",
        "v_escape = √(2 G M / R)",
    ],
    "electrostatics": [
        "F = k q1 q2 / r^2",
        "E (point charge) = k q / r^2",
        "V (point charge) = k q / r",
        "C (parallel plate) = ε A / d",
    ],
    "current_electricity": [
        "I = Q / t",
        "V = I R (Ohm's law)",
        "R(series) = R1 + R2 + ...",
        "1/R(parallel) = 1/R1 + 1/R2 + ...",
        "P = V I = I^2 R = V^2 / R",
    ],
    "trigonometry": [
        "sin^2(x) + cos^2(x) = 1",
        "1 + tan^2(x) = sec^2(x)",
        "1 + cot^2(x) = cosec^2(x)",
        "sin(−x) = −sin(x), cos(−x) = cos(x)",
        "sin(π/2 − x) = cos(x), cos(π/2 − x) = sin(x)",
    ],
    "quadratic": [
        "General form: ax^2 + bx + c = 0",
        "D (discriminant) = b^2 − 4ac",
        "Roots: x = [−b ± √D] / (2a)",
        "Sum of roots = −b/a, product = c/a",
    ],
    "basic_calculus": [
        "d/dx (x^n) = n x^(n−1)",
        "d/dx (sin x) = cos x",
        "d/dx (cos x) = −sin x",
        "∫ x^n dx = x^(n+1)/(n+1) + C (n ≠ −1)",
        "∫ 1/x dx = ln|x| + C",
    ],
    "thermodynamics": [
        "ΔU = Q - W (First law)",
        "PV = nRT (Ideal gas equation)",
        "W = P ΔV (work in isobaric process)",
        "γ = Cp/Cv (heat capacity ratio)",
        "Efficiency η = 1 - T2/T1 (Carnot engine)",
        "ΔS = Q/T (entropy change)",
    ],
    "waves": [
        "v = fλ (wave equation)",
        "y = A sin(ωt - kx) (progressive wave)",
        "f_beat = |f1 - f2| (beats)",
        "v = √(T/μ) (wave speed on string)",
        "I ∝ A² (intensity and amplitude)",
    ],
    "optics": [
        "1/f = 1/v - 1/u (mirror formula)",
        "m = -v/u (magnification)",
        "μ = c/v (refractive index)",
        "μ1 sin θ1 = μ2 sin θ2 (Snell's law)",
        "1/f = (μ-1)(1/R1 - 1/R2) (lens maker)",
        "Path diff = nλ (constructive interference)",
        "Path diff = (n+1/2)λ (destructive)",
    ],
    "magnetism": [
        "F = qvB sin θ (magnetic force)",
        "F = BIL sin θ (force on current)",
        "B = μ0 I / (2πr) (straight wire)",
        "B = μ0 NI / L (solenoid)",
        "τ = NIAB sin θ (torque on coil)",
        "Φ = B·A (magnetic flux)",
    ],
    "modern_physics": [
        "E = hf = hc/λ (photon energy)",
        "KE_max = hf - φ (photoelectric)",
        "λ = h/p (de Broglie wavelength)",
        "E = mc² (mass-energy)",
        "1/λ = R(1/n1² - 1/n2²) (Rydberg)",
        "E_n = -13.6/n² eV (H-atom energy)",
    ],
    "rotational_motion": [
        "τ = I α (torque = moment × angular acc)",
        "L = I ω (angular momentum)",
        "K_rot = 1/2 I ω²",
        "I = Σ m r² (moment of inertia)",
        "v = r ω (linear and angular velocity)",
        "a_c = v²/r = ω²r (centripetal)",
    ],
    "shm": [
        "x = A sin(ωt + φ) (displacement)",
        "v = ω√(A² - x²) (velocity)",
        "a = -ω²x (acceleration)",
        "T = 2π√(m/k) (spring)",
        "T = 2π√(L/g) (simple pendulum)",
        "E = 1/2 k A² (total energy)",
    ],
    "vectors": [
        "A·B = |A||B| cos θ (dot product)",
        "A×B = |A||B| sin θ n̂ (cross product)",
        "R = √(A² + B² + 2AB cos θ) (resultant)",
        "tan α = (B sin θ)/(A + B cos θ)",
    ],
    "logarithms": [
        "log(ab) = log a + log b",
        "log(a/b) = log a - log b",
        "log(a^n) = n log a",
        "log_a(b) = log b / log a (base change)",
        "e^(ln x) = x, ln(e^x) = x",
    ],
    "binomial": [
        "(a+b)^n = Σ nCr a^(n-r) b^r",
        "nCr = n! / (r!(n-r)!)",
        "nCr = nC(n-r)",
        "General term T_(r+1) = nCr a^(n-r) b^r",
    ],
    "matrices": [
        "det(AB) = det(A) × det(B)",
        "A⁻¹ = adj(A) / det(A)",
        "(AB)⁻¹ = B⁻¹A⁻¹",
        "det(A') = det(A)",
        "For 2×2: det = ad - bc",
    ],
    "straight_lines": [
        "Slope m = (y2-y1)/(x2-x1)",
        "y - y1 = m(x - x1) (point-slope)",
        "y = mx + c (slope-intercept)",
        "Distance = |ax1+by1+c|/√(a²+b²)",
        "Angle = tan⁻¹|(m1-m2)/(1+m1m2)|",
    ],
    "circles": [
        "(x-h)² + (y-k)² = r² (standard form)",
        "x² + y² + 2gx + 2fy + c = 0 (general)",
        "Center = (-g, -f), r = √(g²+f²-c)",
        "Tangent length = √(x1²+y1²+2gx1+2fy1+c)",
    ],
    "complex_numbers": [
        "z = a + ib = r(cos θ + i sin θ)",
        "r = |z| = √(a² + b²)",
        "θ = tan⁻¹(b/a) (argument)",
        "z1·z2 = r1r2[cos(θ1+θ2) + i sin(θ1+θ2)]",
        "z^n = r^n(cos nθ + i sin nθ) (De Moivre)",
    ],
    "limits": [
        "lim(x→0) sin x/x = 1",
        "lim(x→0) (1−cos x)/x² = 1/2",
        "lim(x→0) tan x/x = 1",
        "lim(x→∞) (1 + 1/x)^x = e",
        "lim(x→0) (a^x - 1)/x = ln a",
        "lim(x→0) (e^x - 1)/x = 1",
    ],
    "probability": [
        "P(A∪B) = P(A) + P(B) - P(A∩B)",
        "P(A|B) = P(A∩B) / P(B)",
        "P(A∩B) = P(A) × P(B|A)",
        "Total probability: P(E) = Σ P(Ai)P(E|Ai)",
        "Bayes: P(Ai|E) = P(Ai)P(E|Ai) / P(E)",
    ],
}

# ---------- 1200-formula JEE book (JSON) ----------
JEE_FORMULAS_1200 = {}

def load_jee_formula_book(path="jee_1200_formulas.json"):
    global JEE_FORMULAS_1200
    try:
        with open(path, "r", encoding="utf-8") as f:
            JEE_FORMULAS_1200 = json.load(f)
        total = sum(len(v) for v in JEE_FORMULAS_1200.values())
        return f"Loaded {total} formulas from {path}."
    except FileNotFoundError:
        return "JEE formula book file not found. Make sure 'jee_1200_formulas.json' is in this folder."
    except Exception as e:
        return f"Error loading JEE formula book: {e}"

def list_jee_topics():
    if not JEE_FORMULAS_1200:
        return "JEE formula book not loaded. Use 'jee load' first."
    topics = sorted(JEE_FORMULAS_1200.keys())
    return "Available JEE topics:\n" + ", ".join(topics)

def show_jee_topic(topic: str):
    if not JEE_FORMULAS_1200:
        return "JEE formula book not loaded. Use 'jee load' first."
    topic = topic.strip()
    if topic not in JEE_FORMULAS_1200:
        return "No such topic in 1200-formula book. Use 'jee topics' to see all."
    lines = [f"Formulas for {topic}:"]
    for i, fml in enumerate(JEE_FORMULAS_1200[topic], start=1):
        lines.append(f"  {i}. {fml}")
    return "\n".join(lines)

def search_jee_formula(keyword: str):
    if not JEE_FORMULAS_1200:
        return "JEE formula book not loaded. Use 'jee load' first."
    key = keyword.lower().strip()
    results = []
    for topic, flist in JEE_FORMULAS_1200.items():
        for fml in flist:
            if key in fml.lower():
                results.append(f"[{topic}] {fml}")
    if not results:
        return "No formulas found matching that keyword."
    return "Search results:\n" + "\n".join(results[:50])

# ---------- Wikipedia setup ----------
wikipedia.set_lang("en")

def wiki_search(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.DisambiguationError:
        return f"Too many results for '{query}'. Try being more specific."
    except wikipedia.PageError:
        return f"No page found for '{query}'."
    except Exception as e:
        return f"Error: {e}"

# ---------- Math setup ----------
x, y = symbols("x y")

def is_math(text: str) -> bool:
    math_chars = "0123456789x=+-*/^()"
    return any(ch in text for ch in math_chars)

def handle_math(expr: str):
    if "=" in expr:
        try:
            left_str, right_str = expr.split("=")
            left = sympify(left_str)
            right = sympify(right_str)
            equation = Eq(left, right)
            print("\nMath-AI: Equation is:", equation)
            sol = solve(equation, x)
            if sol:
                print("Math-AI: Solution(s) for x:", sol)
            else:
                print("Math-AI: No solution or infinite solutions.")
            print()
        except Exception as e:
            print("Math-AI: Sorry, I couldn't understand that equation.", e, "\n")
    else:
        try:
            expr_sym = sympify(expr)
            print("\nMath-AI: Expression is:", expr_sym)
            print("Math-AI: Simplified:", simplify(expr_sym))
            print("Math-AI: Expanded:", expand(expr_sym))
            print("Math-AI: Factored:", factor(expr_sym), "\n")
        except Exception as e:
            print("Math-AI: Sorry, I couldn't understand that expression.", e, "\n")

# ---------- Reminders, jokes, time ----------
reminders = []
jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "There are only 10 kinds of people: those who understand binary and those who don't.",
    "Why was the math book sad? It had too many problems."
]

memes = [
    "Me: I will study. Also me: *opens VS Code and Minecraft together*",
    "When code works on the first try: 'Did I just become a senior dev?'",
    "JEE + coding: two boss fights, one player.",
    "Python: indentationError. Me: my life is also not properly indented.",
]

motivations = [
    "Small consistent study sessions beat 1 big panic session. 30–60 minutes today is enough.",
    "Every bug you fix is literally XP for your brain. Keep farming.",
    "You don’t need perfect focus, just remove one distraction and start.",
    "Your future self will thank you for 1 hour of JEE + 1 hour of code today.",
]

def add_reminder(text: str):
    reminders.append(text)
    return f"Reminder added: {text}"

def list_reminders():
    if not reminders:
        return "You have no reminders yet."
    msg = "Your reminders:\n"
    for i, r in enumerate(reminders, start=1):
        msg += f"{i}. {r}\n"
    return msg.strip()

def get_time():
    now = datetime.datetime.now()
    return now.strftime("Current time: %H:%M:%S, Date: %d-%m-%Y")

def get_day():
    day = datetime.datetime.today().weekday()
    names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return names[day]

def get_joke():
    return random.choice(jokes)

def get_meme():
    return random.choice(memes)

def get_motivation():
    return random.choice(motivations)

# ---------- Notes (file) ----------
def add_note(text: str):
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return "Note saved."

def show_notes():
    try:
        with open("notes.txt", "r", encoding="utf-8") as f:
            data = f.read().strip()
        return data if data else "No notes yet."
    except FileNotFoundError:
        return "No notes file yet."

def search_notes(word: str):
    try:
        with open("notes.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return "No notes yet."
    found = [ln.strip() for ln in lines if word.lower() in ln.lower()]
    if not found:
        return "No notes found with that word."
    return "\n".join(found)

# ---------- Tasks / to-do list ----------
tasks = []

def add_task(text: str):
    tasks.append({"text": text, "done": False})
    return f"Task added: {text}"

def list_tasks():
    if not tasks:
        return "You have no tasks yet."
    lines = []
    for i, t in enumerate(tasks, start=1):
        status = "✓" if t["done"] else " "
        lines.append(f"[{status}] {i}. {t['text']}")
    return "\n".join(lines)

def done_task(index: int):
    if 1 <= index <= len(tasks):
        tasks[index-1]["done"] = True
        return f"Task {index} marked as done."
    else:
        return "No task with that number."

def save_tasks():
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    return "Tasks saved to tasks.json."

def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r", encoding="utf-8") as f:
            tasks = json.load(f)
        return "Tasks loaded from tasks.json."
    except FileNotFoundError:
        return "No saved tasks found."

# ---------- History ----------
history = []

def add_history_entry(command: str):
    entry = {
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "command": command,
    }
    history.append(entry)
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(entry)
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def show_last_history(n=10):
    if not history:
        return "No history yet."
    lines = []
    for entry in history[-n:]:
        lines.append(f"{entry['time']} → {entry['command']}")
    return "\n".join(lines)

def show_history_stats():
    if not history:
        return "No history yet."
    total = len(history)
    counts = {}
    for h in history:
        cmd = h["command"].split()[0] if h["command"] else ""
        counts[cmd] = counts.get(cmd, 0) + 1
    top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]
    lines = [f"Total commands: {total}", "Most used commands:"]
    for cmd, c in top:
        lines.append(f"  - {cmd}: {c} times")
    return "\n".join(lines)

# ---------- Game ----------
def play_guess():
    secret = random.randint(1, 20)
    print("AI: I picked a number between 1 and 20. Try to guess! Type 'q' to quit this game.")
    tries = 0
    while True:
        guess = input("Your guess: ").strip()
        if guess.lower() == "q":
            print("AI: Game ended. The number was", secret)
            break
        try:
            g = int(guess)
        except ValueError:
            print("AI: Please enter a number.")
            continue
        tries += 1
        if g < secret:
            print("AI: Too low!")
        elif g > secret:
            print("AI: Too high!")
        else:
            print(f"AI: Correct! You took {tries} tries.")
            break

# ---------- Focus timer ----------
def focus_timer(minutes: int):
    total = minutes * 60
    print(f"AI: Focus timer started for {minutes} minutes. I’ll remind you when it’s over.")
    while total > 0:
        if total % 60 == 0:
            print(f"AI: {total // 60} minutes left...")
        time.sleep(1)
        total -= 1
    print("AI: Time's up! Great job. Take a 5 minute break.")
    play_beep()

# ---------- Countdown timer ----------
def countdown_timer(seconds: int):
    print(f"AI: Countdown started for {seconds} seconds.")
    remaining = seconds
    while remaining > 0:
        mins, secs = divmod(remaining, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        print("AI Timer:", time_str, end="\r")
        time.sleep(1)
        remaining -= 1
    print("\nAI: Time's up!")
    play_beep()

# ---------- Matrix rain ----------
def matrix_rain(lines=10, width=30, delay=0.05):
    chars = "01"
    print("AI: Entering matrix mode (fake)…")
    for _ in range(lines):
        row = "".join(random.choice(chars) for _ in range(width))
        print(row)
        time.sleep(delay)
    print("AI: Matrix mode ended. Back to reality.")

# ---------- Main loop ----------
print("AI: Hi! I am your smart Python AI.")
print("AI: What I can do:")
print("  - wiki <topic>        → Wikipedia summary")
print("  - math                → equations & expressions")
print("  - open <site>         → youtube, google, gemini, chatgpt, perplexity, sarvam, etc.")
print("  - time / date / day   → show current time, date, or day")
print("  - joke / meme         → random joke or coding/student meme")
print("  - motivate            → small motivation for study/coding")
print("  - reminder add/list   → simple reminders")
print("  - note add/list/search→ notes in notes.txt")
print("  - task add/list/done  → to-do list (with save/load)")
print("  - jee formula         → built-in key formulas")
print("  - jee load/topics/topic/search → 1200-formula JEE book (JSON)")
print("  - focus <minutes>     → focus timer for study")
print("  - timer <seconds>     → short countdown with beep")
print("  - beep set/test       → customize and test beep sound")
print("  - history last/stats  → see your usage history")
print("  - game                → guess-the-number")
print("  - safety              → India safety tips, helplines & lab rules")
print("  - setup               → how to install required Python packages")
print("  - shortcuts           → quick reminder of useful commands & sites")
print("  - terms               → terms & conditions of this fun lab")
print("  - help / sites / about→ discover features")
print("  - version / credits   → version & project credits")
print("  - fun                 → hint about secret Easter eggs")
print("Type 'bye' to exit.\n")

current_hour = datetime.datetime.now().hour
if current_hour < 12:
    greet = "Good morning"
elif current_hour < 18:
    greet = "Good afternoon"
else:
    greet = "Good evening"
print(f"AI: {greet}, Kavyant! (v{__version__})")

while True:
    user_input = input("You: ").strip()
    lower = user_input.lower()

    # record every action
    add_history_entry(lower)

    if lower in ("bye", "exit", "quit"):
        print("AI: Goodbye! Keep coding and studying!")
        break

    if lower.startswith("wiki "):
        topic = user_input[5:].strip()
        if topic:
            print("AI: Searching Wikipedia...")
            answer = wiki_search(topic)
            print("AI:", answer)
        else:
            print("AI: Please type something after 'wiki'.")

    elif lower.startswith("open "):
        key = lower[5:].strip()
        if key in sites:
            print("AI: Opening", key, "...")
            webbrowser.open(sites[key])
        else:
            print("AI: I don't know that site yet.")
            some_keys = ", ".join(sorted(list(sites.keys()))[:20])
            print("AI: Some options are:", some_keys, "...")

    elif lower == "help":
        print("AI: Here are my commands:")
        for cmd, desc in commands.items():
            print(f"  - {cmd:20} → {desc}")

    elif lower in ("sites", "open list"):
        print("AI: You can 'open' these sites:")
        print(", ".join(sorted(sites.keys())))

    elif lower == "about":
        print(f"AI: I am a Python assistant (v{__version__}) made by Kavyant Kumar (Cares & Laughs – Your Fun Lab).")
        print("AI: I help with web, wiki, math, notes, reminders, tasks, JEE formulas, focus timers and fun Easter eggs.")

    elif lower == "credits":
        print("AI: Project: Smart Python Assistant (CLI)")
        print("AI: Creator: Kavyant Kumar (Cares & Laughs – Your Fun Lab / CareLabStudio)")
        print("AI: Built with: Python, wikipedia, sympy, webbrowser, and pure curiosity.")
        print("AI: Year: 2026 | Location: Ghaziabad, India")
        print("AI: If you’re seeing this on YouTube, like & subscribe to support future projects!")

    elif lower == "version":
        print(f"AI: Current version: v{__version__}")

    elif lower == "copyright":
        print("AI: © 2026 Kavyant Kumar. All rights reserved.")
        print("AI: No part of this code may be reproduced, distributed, or modified")
        print("AI: without the prior written permission of the copyright owner.")

    elif lower == "fun":
        print("AI: Try typing things like:")
        print("  - 'import this', 'antigravity'")
        print("  - 'kavyant secret', 'hack system'")
        print("  - 'cowsay', 'matrix', 'hello world'")
        print("  - 'from future import braces'")
        print("  - 'rick roll'")
        print("  - 'open gemini', 'open chatgpt', 'open claude', 'open copilot', 'open perplexity', 'open sarvam'")
        print("  - 'safety' to see India safety tips & helplines")

    elif lower == "setup":
        print("AI: To install required Python packages, run these in your terminal:")
        print()
        print("  On Windows (with 'py' launcher):")
        print("    py -m pip install wikipedia")
        print("    py -m pip install sympy")
        print()
        print("  On Linux / macOS (python3):")
        print("    python3 -m pip install wikipedia")
        print("    python3 -m pip install sympy")

    elif lower == "shortcuts":
        print("AI: Quick shortcuts you can use:")
        print()
        print("  General:")
        print("    - 'help'              → list all commands")
        print("    - 'shortcuts'         → this quick overview")
        print("    - 'sites'             → list all site shortcuts")
        print("    - 'about', 'credits'  → info about this project")
        print("    - 'version'           → show current version")
        print()
        print("  Web & AI:")
        print("    - 'open youtube', 'open google', 'open gmail'")
        print("    - 'open gemini', 'open chatgpt', 'open claude', 'open copilot'")
        print("    - 'open perplexity', 'open sarvam', 'open deepseek', 'open grok'")
        print("    - 'open cares'        → open your Cares & Laughs Fun Lab pen")
        print("    - 'open carelabstudio'→ open your YouTube channel")
        print()
        print("  Study & JEE:")
        print("    - 'jee formula kinematics'    → key formulas built-in")
        print("    - 'jee load'                  → load 1200-formula JEE JSON")
        print("    - 'jee topics'                → see all topics in JEE book")
        print("    - 'jee topic <name>'          → formulas for a topic")
        print("    - 'jee search <keyword>'      → search formulas in JEE book")
        print("    - 'focus 25'                  → 25-min focus timer")
        print("    - 'timer 120'                 → 2-minute countdown timer")
        print()
        print("  Notes & Tasks:")
        print("    - 'note add <text>'           → add a note to notes.txt")
        print("    - 'note list'                 → show all notes")
        print("    - 'note search <word>'        → search notes")
        print("    - 'task add <text>'           → add to-do")
        print("    - 'task list'                 → show to-dos")
        print("    - 'task done 1'               → mark task 1 done")
        print("    - 'task save' / 'task load'   → save/load tasks.json")
        print()
        print("  Fun & Easter Eggs:")
        print("    - 'fun'                       → list Easter egg hints")
        print("    - 'matrix'                    → fake matrix rain")
        print("    - 'game'                      → guess-the-number game")
        print("    - 'cowsay' or 'sl'            → fun ASCII art")
        print("    - 'rick roll'                 → you know what happens")
        print("    - 'import this', 'antigravity', 'from future import braces'")
        print()
        print("  Safety & Setup:")
        print("    - 'safety'                    → India safety tips & helplines")
        print("    - 'setup'                     → how to install wikipedia & sympy")
        print("    - 'history last' / 'history stats' → see your usage history")

    elif lower == "terms":
        print("AI: Terms & Conditions of this Fun Lab")
        print()
        print("1) Educational & Entertainment Purpose Only:")
        print("   This assistant is made for learning, study support, and positive fun.")
        print("   It is not a professional tool for medical, legal, financial or emergency advice.")
        print()
        print("2) You Are Responsible for Your Actions:")
        print("   You are responsible for how you use the information and ideas from this lab.")
        print("   Use them only for legal and ethical purposes (no hacking, scams, bullying or abuse).")
        print()
        print("3) No Guarantee of Accuracy:")
        print("   The assistant may sometimes be wrong or outdated, especially for helplines or laws.")
        print("   Always double-check important information on official websites or with trusted adults/teachers.")
        print()
        print("4) Privacy & Sensitive Data:")
        print("   Do NOT enter passwords, OTPs, bank details, very private secrets or full addresses into this lab.")
        print("   Notes and history are stored locally on your device, but still keep them safe and non-sensitive.")
        print()
        print("5) No NSFW / 18+ Use for Minors:")
        print("   If you are under 18, do NOT use this lab to access adult content, gambling, drugs or illegal stuff.")
        print("   Two external NSFW areas mentioned in your projects are strictly 18+ only.")
        print()
        print("6) No Harassment or Hate:")
        print("   Do not use this lab to plan, support or spread harassment, bullying, discrimination or hate speech.")
        print("   Be kind in your code, your chats, and your projects.")
        print()
        print("7) Changes & Updates:")
        print("   The developer (Kavyant Kumar) can change features, text, or rules anytime to improve safety and quality.")
        print("   Updated versions may have new commands, safety tips, or removed/changed features.")
        print()
        print("8) No Liability:")
        print("   The creator is not liable for any damage, loss or trouble caused by misuse of this lab or wrong information.")
        print("   By using this assistant, you accept that you must act carefully and double-check important things.")
        print()
        print("9) Respect Licenses & Credits:")
        print("   Do not remove original credits or claim this full project as only your own if you share or fork it.")
        print("   When you share modified versions, give clear credit to the original creator and follow license terms if added.")
        print()
        print("10) Golden Rule:")
        print("   Anything you build or do after using this lab must be Kind, Legal and Respectful.")
        print("   If an idea breaks any of these three, it is NOT allowed here – don’t do it, don’t share it.")
        print()
        print("AI: By continuing to use this assistant, you agree to these terms in spirit.")

    elif lower == "safety":
        print("AI: Safety, Helplines & Lab Rules (India)")
        print()
        print("Safety First:")
        print("  - Never share your real name, address, school, phone number, passwords or bank details in random apps or sites.")
        print("  - Never share OTPs (one-time passwords) with anyone – not friends, 'support' staff, or strangers.")
        print("  - Do not enter your details on random forms/pop-ups that promise money, gifts or free diamonds/coins.")
        print("  - Don’t click unknown links or download files from strangers. Avoid 'free UC/Robux' hacks on Discord/Telegram.")
        print("  - Be kind in jokes and pranks: no bullying or hate. In multiplayer games, report toxic chat.")
        print("  - If something online makes you feel scared or uncomfortable, stop and tell a trusted adult; use cybercrime.gov.in for serious issues.")
        print("  - Take regular breaks from screens (20-20-20 rule) and move your body.")
        print()
        print("India SMS Codes (P / S / T / G):")
        print("  Many sender IDs in India use a letter so you can see what type of SMS it is.")
        print("  - P (Promotional): Marketing, offers, ads. Example: 'WINBIG-P: Claim prize!' – usually ignore.")
        print("  - S (Service): Service / account updates, reminders, customer info.")
        print("  - T (Transactional): OTPs, banking alerts, order confirmations.")
        print("  - G (Government): Official government messages, advisories, emergency alerts.")
        print("  If an SMS looks random or has strange links, treat it as suspicious. Do NOT click links or share data/OTPs.")
        print()
        print("Values, Rights & Zero Corruption:")
        print("  - Practice honesty – no cheating, no fake promises, no bribes.")
        print("  - Respect everyone – no hate speech in gaming chats or code forums.")
        print("  - Say NO to corruption – don’t support shortcuts that break rules.")
        print("  - Remember your basic rights in India (equality, free speech, protection from exploitation, right to education, etc.).")
        print("  - Real 'pro gamer' and 'pro coder' behaviour = fair play, giving credit, not stealing work, and reporting abuse instead of using it.")
        print()
        print("Emergency Contacts (India) (always verify latest on india.gov.in/directory/helpline):")
        print("  - 112: All emergencies (police / fire / medical).")
        print("  - 100: Police.")
        print("  - 101: Fire.")
        print("  - 102: Ambulance (basic medical).")
        print("  - 108: Ambulance & disaster response (many states).")
        print("  - 1070: Relief Commissioner for natural calamities (state level).")
        print("  - 1073: Road accident emergency service (many states).")
        print("  - 1033: Road accidents (national highways).")
        print("  - 1906: LPG leak helpline.")
        print("  - 1930: Cybercrime / online financial fraud helpline (call ASAP).")
        print("  - 1915: National Consumer Helpline.")
        print("  - 1098: Childline (kids / students in trouble).")
        print("  - 1091 / 181: Women’s helplines (domestic abuse & safety).")
        print("  - 1097: AIDS / HIV helpline.")
        print("  - 1064: Anti-corruption helpline (many states).")
        print("  - 1066 / 011-1066: Anti-poison (AIIMS New Delhi).")
        print("  - 1800-599-0019: Mental health (KIRAN 24x7).")
        print()
        print("Cybercrime, Digital Safety & Online Fraud:")
        print("  - 1930: National cyber fraud helpline (immediate reporting).")
        print("  - 155260 / 155299: Cyber/banking fraud lines (varies by bank/state).")
        print("  - 14440: Digital payments / UPI (NPCI help).")
        print("  - 1945: Banking fraud escalation (some regions).")
        print("  - 1800-11-1100: IT / digital complaints (government grievance).")
        print("  - 1963: Telecom complaints (spam/fraud calls – varies).")
        print("  - 198 / 199: Telecom complaints (billing, network, spam calls).")
        print("  - Cybercrime portal: cybercrime.gov.in (official FIR/reporting).")
        print("  - RBI complaint portal: cms.rbi.org.in (bank escalation).")
        print("  - National Consumer Portal: consumerhelpline.gov.in.")
        print("  - Suspected fraud calls/SMS: sancharsaathi.gov.in (Sanchar Saathi).")
        print()
        print("CBSE, Students & Education Support (check cbse.gov.in for latest):")
        print("  - 1800-11-8002: CBSE helpline (general queries).")
        print("  - 011-22509256: CBSE HQ support.")
        print("  - 1800-11-6888: Exam stress / counseling (seasonal).")
        print("  - 14416: Student mental health support.")
        print("  - 1098: Child helpline (students in distress).")
        print("  - 14567: Senior citizen helpline (for guardians).")
        print("  - 104: Student health advice (many states).")
        print("  - 1800-599-0019: KIRAN mental health (students too).")
        print("  - CBSE Official: cbse.gov.in | Results: results.cbse.nic.in | DigiLocker: digilocker.gov.in.")
        print("  - CBSE vigilance: vigilance@cbse.gov.in (exam/board malpractice, corruption-related complaints).")
        print()
        print("Other education systems & support:")
        print("  - UGC Helpline: 1800-111-656 (higher education issues).")
        print("  - AICTE Support: 1800-425-1111 (technical education).")
        print("  - National Scholarship Portal: scholarships.gov.in.")
        print("  - Anti-Ragging Helpline: 1800-180-5522.")
        print()
        print("Different abilities, same safety:")
        print("  If you or a family member has any disability and faces online/offline abuse, you can still use these helplines; some states have special support lines.")
        print()
        print("Think Before You Click:")
        print("  - Don’t tap links from unknown numbers, random DMs, or 'you won a prize' messages.")
        print("  - Check the full URL: small spelling changes (g00gle, instagrarn) are a red flag.")
        print("  - Never enter passwords, PIN, card or OTP on pages opened from random links.")
        print("  - When in doubt, open the official website/app yourself instead of using the link.")
        print()
        print("Extra Care for Younger Users & Girls:")
        print("  - Never send photos, videos or live location to strangers or 'online friends' you’ve never met with family around.")
        print("  - If someone flirts, blackmails, asks for 'secret pics' or threatens to leak chats, stop replying and tell a trusted adult immediately.")
        print("  - You can call 1098 (Childline) or use cybercrime.gov.in for serious cases – don’t stay silent.")
        print()
        print("Pro Mode: Clean Installs Only:")
        print("  - Before installing any app, check ratings, reviews and number of downloads; fake apps often have weird names and few reviews.")
        print("  - Check permissions: a torch/wallpaper app should not need mic, SMS, contacts or full location access.")
        print("  - Avoid browser pop-ups saying 'Your phone is infected' or 'Update required, click here' – close the tab instead.")
        print("  - For school/work files, prefer official links (school portal, Google Drive, OneDrive) instead of random file-sharing sites.")
        print("  - Backup important data (photos, notes, code) regularly so you don’t lose everything if something goes wrong.")
        print()
        print("Stealth Mode: Privacy & Tracking:")
        print("  - Keep profiles private wherever possible; only accept people you actually know.")
        print("  - Check privacy settings on your main apps (who can see posts, status, stories).")
        print("  - Turn off location sharing for social media and random apps that don’t need it.")
        print("  - Don’t post your routine (school time, tuition location, solo travel plans) in real time.")
        print("  - If someone keeps asking for photos, video calls or personal details, stop responding and tell a trusted adult.")
        print()
        print("Report, Don’t Just Rage Quit:")
        print("  - If you get abusive/creepy/blackmail messages, do NOT reply or fight back.")
        print("  - Take screenshots (chat, profile, phone number, payment IDs) and save them safely.")
        print("  - Block the account and use the platform’s report button.")
        print("  - For serious stuff (money fraud, threats, nudes, blackmail), tell a trusted adult and use cybercrime.gov.in or the 1930 helpline.")
        print()
        print("Smoking & Tobacco: Why to Quit:")
        print("  - Damages lungs, heart and brain; increases risk of cancer, stroke, TB and early death.")
        print("  - Wastes money that could go to games, education, travel or family.")
        print("  - Makes fitness, focus and exam performance worse over time.")
        print("  - National Tobacco Quitline: 1800-112-356.")
        print("  - mCessation SMS: missed call to 011-22901701 for free SMS tips.")
        print("  - KIRAN Mental Health Helpline: 1800-599-0019 (24x7).")
        print()
        print("Simple Ways to Start Quitting:")
        print("  - Pick a quit date in the next 7 days and mark it in your calendar/notes.")
        print("  - Throw away all cigarettes/bidis/vapes/gutkha from your room, bag and desk.")
        print("  - Avoid smoking spots and late-night 'smoke breaks' with friends for a while.")
        print("  - When cravings hit, use gum/water/deep breathing/short walks; cravings usually peak 5–10 minutes.")
        print("  - Treat it like a streak: if you slip, don’t quit quitting – restart your streak next day.")
        print()
        print("Four Monkeys of Digital Wisdom:")
        print("  🙈 See No Toxic  – avoid hateful, violent or disturbing content; mute/block pages that stress you out.")
        print("  🙉 Hear No Fake  – don’t believe every forward, reel or rumour (exam leaks, free money, free UC); cross-check big news on trusted sites.")
        print("  🙊 Speak No Hate – no bullying, slurs or harassment in chats/comments/voice, even as 'jokes'.")
        print("  🐒 Do No Wrong   – don’t hack, leak, dox, cheat or share private photos/data; use your skills for good and report abuse.")
        print()
        print("Golden Rule of This Lab:")
        print("  Anything you do after using this lab must be Kind (no bullying), Legal (no hacking/drugs/gambling/revenge stuff), and Respectful (no corruption, no cheating, no hate).")
        print("  If an idea breaks any of these, it is NOT allowed here – don’t do it, don’t share it, don’t encourage it.")
        print()
        print("5-Second Check Before Any Action:")
        print("  1) Would I be okay if my parents/teacher saw this?")
        print("  2) Would I be okay if this was done to me?")
        print("  3) Could this break a law, hurt someone’s mind/body, or leak private info?")
        print("  If the answer is 'no' or 'I’m not sure' to any, don’t do it. Change the plan.")
        print()
        print("Good Deeds & Nation-Building Mode:")
        print("  - Help a classmate with notes/homework/doubts instead of trolling them.")
        print("  - Join or start clean-up, tree-planting or blood-donation awareness (with adults).")
        print("  - Volunteer in school/college events, NSS-type activities or local community drives.")
        print("  - Give credit when you use someone’s code, art or idea; no plagiarism, only respect.")
        print()
        print("Daily Kindness Missions:")
        print("  - Send one honest compliment to a friend or family member today.")
        print("  - Help at home (dishes, room, siblings’ homework) without being asked.")
        print("  - Share notes/explanations with someone who missed a class.")
        print("  - Make one person laugh today with a harmless joke or meme.")
        print()
        print("About the Developer:")
        print("  This lab is developed by Kavyant Kumar, a student web developer who loves mixing code, games and mental-health-friendly ideas.")
        print("  It started as a forked Pen and was rebuilt into this fuller Cares & Laughs Lab while keeping the original MIT license and proper credit.")
        print("  Featured projects are on your CodePen profile (Cares & Laughs – Fun Lab, Windows 11 Clone, Greener World, Pixel Shooter, etc.).")
        print()
        print("Important:")
        print("  - Helpline numbers, laws and websites can change over time.")
        print("  - For the latest official details, always double-check:")
        print("      * india.gov.in/directory/helpline")
        print("      * cybercrime.gov.in")
        print("      * mygov.in/staysafeonline")
        print("  - If you ever notice a wrong/outdated number or broken link, update your code and pages.")
        print()
        print("For full rules about how to use this lab, type 'terms'.")
        print()
        print("AI: Safety mode off. Use this info kindly and legally.")

    elif lower.startswith("reminder add "):
        text = user_input[len("reminder add "):].strip()
        if text:
            print("AI:", add_reminder(text))
        else:
            print("AI: Please write what to remember after 'reminder add'.")
    elif lower == "reminder list":
        print("AI:", list_reminders())

    elif lower.startswith("note add "):
        text = user_input[len("note add "):].strip()
        if text:
            print("AI:", add_note(text))
        else:
            print("AI: Please write something after 'note add'.")
    elif lower == "note list":
        print("AI:", show_notes())
    elif lower.startswith("note search "):
        word = user_input[len("note search "):].strip()
        if word:
            print("AI:", search_notes(word))
        else:
            print("AI: Please provide a word after 'note search'.")

    elif lower.startswith("task add "):
        text = user_input[len("task add "):].strip()
        if text:
            print("AI:", add_task(text))
        else:
            print("AI: Please write something after 'task add'.")

    elif lower == "task list":
        print("AI:\n" + list_tasks())

    elif lower.startswith("task done "):
        num_str = user_input[len("task done "):].strip()
        try:
            n = int(num_str)
            print("AI:", done_task(n))
        except ValueError:
            print("AI: Please give a valid task number after 'task done'.")

    elif lower == "task save":
        print("AI:", save_tasks())

    elif lower == "task load":
        print("AI:", load_tasks())

    elif lower == "history last":
        print("AI:", show_last_history())
    elif lower == "history stats":
        print("AI:", show_history_stats())

    elif lower == "jee load":
        print("AI:", load_jee_formula_book())

    elif lower == "jee topics":
        print("AI:", list_jee_topics())

    elif lower.startswith("jee topic "):
        tname = user_input[len("jee topic "):].strip()
        if tname:
            print("AI:", show_jee_topic(tname))
        else:
            print("AI: Please provide a topic name after 'jee topic'.")

    elif lower.startswith("jee search "):
        key = user_input[len("jee search "):].strip()
        if key:
            print("AI:", search_jee_formula(key))
        else:
            print("AI: Please provide a keyword after 'jee search'.")

    elif lower.startswith("jee formula "):
        topic = lower[len("jee formula "):].strip()
        if topic in jee_formulas:
            print(f"AI: Formulas for {topic}:")
            for f in jee_formulas[topic]:
                print("  -", f)
        else:
            print("AI: I don't have formulas for that topic yet.")
            print("AI: Try topics like:")
            print("AI:  kinematics, laws_of_motion, work_energy, gravitation")
            print("AI:  electrostatics, current_electricity, trigonometry, quadratic, basic_calculus")
            print("AI:  thermodynamics, waves, optics, magnetism, modern_physics, rotational_motion, shm")
            print("AI:  vectors, logarithms, binomial, matrices, straight_lines, circles, complex_numbers")
            print("AI:  limits, probability")

    elif lower.startswith("focus "):
        num_str = lower[len("focus "):].strip()
        try:
            mins = int(num_str)
            focus_timer(mins)
        except ValueError:
            print("AI: Please give minutes like 'focus 25'.")

    elif lower.startswith("timer "):
        num_str = lower[len("timer "):].strip()
        try:
            secs = int(num_str)
            if secs <= 0:
                print("AI: Please give a positive number of seconds.")
            else:
                countdown_timer(secs)
        except ValueError:
            print("AI: Please give seconds like 'timer 30' or 'timer 120'.")

    elif lower.startswith("beep set "):
        parts = lower.split()
        if len(parts) == 4:
            try:
                freq = int(parts[2])
                dur = int(parts[3])
                if freq < 37 or freq > 32767:
                    print("AI: Frequency must be between 37 and 32767 Hz.")
                else:
                    set_beep_settings(freq, dur)
                    print(f"AI: Beep settings updated to {freq} Hz, {dur} ms.")
                    play_beep()
            except ValueError:
                print("AI: Use numbers like 'beep set 1000 300'.")
        else:
            print("AI: Use: beep set <freq> <ms>  e.g. 'beep set 800 200'.")

    elif lower == "beep test":
        print("AI: Playing test beep with current settings.")
        play_beep()

    elif lower == "matrix":
        matrix_rain()

    elif "time" in lower or "date" in lower:
        print("AI:", get_time())
    elif "day" in lower:
        print("AI: Today is", get_day())

    elif lower == "joke":
        print("AI:", get_joke())
    elif lower == "meme":
        print("AI:", get_meme())
    elif lower == "motivate":
        print("AI:", get_motivation())

    elif lower == "game":
        play_guess()

    elif is_math(lower):
        handle_math(user_input)

    else:
        if "import this" in lower:
            print("AI: Nice, you know the Zen of Python. Readability counts. [Easter egg]")
        elif "antigravity" in lower:
            print("AI: Opening a secret Python comic for you...")
            webbrowser.open("https://xkcd.com/353/")
        elif "hello world" in lower:
            print("AI: Hello World! (classic Python vibe).")
        elif "from future import braces" in lower:
            print("AI: SyntaxError: not a chance (Python is loyal to indentation).")
        elif "kavyant secret" in lower:
            print("AI: Welcome to the Fun Lab secret room 🧪 (keep building cool stuff).")
        elif lower == "hack system":
            print("AI: Initializing hack protocol...")
            print("AI: 0%... 25%... 50%... 75%... 100%")
            print("AI: Just kidding. Stay ethical, hacker.")
        elif lower == "cowsay":
            print(r"  ^__^")
            print(r"  (oo)\_______")
            print(r"  (__)\       )\/\ ")
            print(r"      ||----w |")
            print(r"      ||     ||")
        elif lower == "sl":
            print("AI:      ====        ________")
            print("AI:  _D _|  |_______/        \\__I_I_____===__|")
            print("AI:   |(_)---  |   H\\________/ |   |        |")
            print("AI:   /     |  |   H  |  |     |   |        |")
            print("AI:  ===============( )==============( )=====")
        elif "rick roll" in lower or "rickroll" in lower:
            print("AI: Never gonna give you up...")
            webbrowser.open(sites["rickroll"])
        elif "good night" in lower or "gn" in lower:
            print("AI: Good night! Sleep well and crush it tomorrow.")
        elif "hello" in lower or "hi" in lower:
            print("AI: Hello! How are you feeling today?")
        elif "sad" in lower:
            print("AI: I'm sorry you feel sad. Want to tell me more or take a small break?")
        elif "study" in lower or "jee" in lower:
            print("AI: Remember: small steps daily for JEE, Class 11, and boards. What topic are you on?")
        elif "code" in lower or "coding" in lower:
            print("AI: Coding + JEE together is powerful. What project are you working on?")
        else:
            print("AI: I don't fully understand, but I'm learning. Try saying it in a simpler way.")
