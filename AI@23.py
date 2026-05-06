"""
Smart Python Assistant (CLI) with Complete Abusive Language Detection
Copyright (c) 2026 Kavyant Kumar
All rights reserved.

Author : Kavyant Kumar (Cares & Laughs – Your Fun Lab / CareLabStudio)
Version: 10.1.0
Year   : 2026
Location: Ghaziabad, Uttar Pradesh, Sector 2, Block A, Flat 101 1/33 Rajendar Nagar, India

Setup (run this in your terminal/command prompt before using):

  On Windows (with 'py' launcher):
      py -m pip install wikipedia
      py -m pip install sympy

  On Linux / macOS (python3):
      python3 -m pip install wikipedia
      python3 -m pip install sympy
"""

__version__ = "10.1.0"

import wikipedia
from sympy import symbols, Eq, solve, sympify
from sympy import simplify, factor, expand
import datetime
import random
import webbrowser
import time
import json
import os
import re

# ========== COMPLETE ABUSIVE LANGUAGE DETECTOR ==========
# Contains EVERY word from your Hindi swear words table

class AbusiveDetector:
    def __init__(self):
        # ===== ALL ROMAN TRANSLITERATION WORDS FROM YOUR TABLE =====
        self.abusive_words = {
            "aad", "aand", "bahenchod", "behenchod", "bhenchod", "bhenchodd",
            "b.c.", "bc", "bakchod", "bakchodd", "bakchodi", "bevda", "bewda",
            "bevdey", "bewday", "bevakoof", "bevkoof", "bevkuf", "bewakoof",
            "bewkoof", "bewkuf", "bhadua", "bhaduaa", "bhadva", "bhadvaa",
            "bhadwa", "bhadwaa", "bhosada", "bhosda", "bhosdaa", "bhosdike",
            "bhonsdike", "bsdk", "b.s.d.k", "bhosdiki", "bhosdiwala", "bhosdiwale",
            "Bhosadchodal", "Bhosadchod", "babbe", "babbey", "bube", "bubey",
            "bur", "burr", "buurr", "buur", "charsi", "chooche", "choochi",
            "chuchi", "chhod", "chod", "chodd", "chudne", "chudney", "chudwa",
            "chudwaa", "chudwane", "chudwaane", "choot", "chut", "chute",
            "chutia", "chutiya", "chutiye", "chuttad", "chutad", "dalaal",
            "dalal", "dalle", "dalley", "fattu", "gadha", "gadhe", "gadhalund",
            "gaand", "gand", "gandu", "gandfat", "gandfut", "gandiya", "gandiye",
            "goo", "gu", "gote", "gotey", "gotte", "hag", "haggu", "hagne",
            "hagney", "harami", "haramjada", "haraamjaada", "haramzyada",
            "haraamzyaada", "haraamjaade", "haraamzaade", "haraamkhor", "haramkhor",
            "jhat", "jhaat", "jhaatu", "jhatu", "kutta", "kutte", "kuttey",
            "kutia", "kutiya", "kuttiya", "kutti", "landi", "landy", "laude",
            "laudey", "laura", "lora", "lauda", "ling", "loda", "lode", "lund",
            "launda", "lounde", "laundey", "laundi", "loundi", "laundiya",
            "loundiya", "lulli", "maar", "maro", "marunga", "madarchod",
            "madarchodd", "madarchood", "madarchoot", "madarchut", "m.c.", "mc",
            "mamme", "mammey", "moot", "mut", "mootne", "mutne", "mooth", "muth",
            "nunni", "nunnu", "paaji", "paji", "pesaab", "pesab", "peshaab",
            "peshab", "pilla", "pillay", "pille", "pilley", "pisaab", "pisab",
            "pkmkb", "porkistan", "raand", "rand", "randi", "randy", "suar",
            "tatte", "tatti", "tatty", "ullu"
        }
        
        # ===== ALL DEVANAGARI WORDS FROM YOUR TABLE =====
        self.devanagari_words = {
            "आंड़", "आंड", "आँड", "बहनचोद", "बेहेनचोद", "भेनचोद",
            "बकचोद", "बकचोदी", "बेवड़ा", "बेवड़े", "बेवकूफ", "भड़ुआ",
            "भड़वा", "भोसड़ा", "भोसड़ीके", "भोसड़ीकी", "भोसड़ीवाला",
            "भोसड़ीवाले", "भोसरचोदल", "भोसदचोद", "भोसड़ाचोदल", "भोसड़ाचोद",
            "बब्बे", "बूबे", "बुर", "चरसी", "चूचे", "चूची", "चुची",
            "चोद", "चुदने", "चुदवा", "चुदवाने", "चूत", "चूतिया", "चुटिया",
            "चूतिये", "चुत्तड़", "चूत्तड़", "दलाल", "दलले", "फट्टू",
            "गधा", "गधे", "गधालंड", "गांड", "गांडू", "गंडफट", "गंडिया",
            "गंडिये", "गू", "गोटे", "हग", "हग्गू", "हगने", "हरामी",
            "हरामजादा", "हरामज़ादा", "हरामजादे", "हरामज़ादे", "हरामखोर",
            "झाट", "झाटू", "कुत्ता", "कुत्ते", "कुतिया", "कुत्ती", "लेंडी",
            "लोड़े", "लौड़े", "लौड़ा", "लोड़ा", "लोडा", "लोडे", "लंड",
            "लौंडा", "लौंडे", "लौंडी", "लौंडिया", "लुल्ली", "नुननी", "नुननु",
            "मार", "मारो", "मारूंगा", "मादरचोद", "मादरचूत", "मादरचुत",
            "मम्मे", "मूत", "मूतने", "मूठ", "पेसाब", "पेशाब", "पिसाब",
            "पिल्ला", "पिल्ले", "पोरकिस्तान", "रांड", "रंडी", "सुअर", "सूअर",
            "टट्टे", "टट्टी", "पाजी", "उल्लू"
        }
        
        # Combine all words
        all_words = self.abusive_words.union(self.devanagari_words)
        
        # Create regex pattern for word boundaries
        self.pattern = re.compile(
            r'\b(?:' + '|'.join(re.escape(w.lower()) for w in all_words) + r')\b',
            re.IGNORECASE
        )
        
        # Special patterns for dotted abbreviations (b.c., m.c., b.s.d.k)
        self.dot_patterns = [
            (r'b\.\s*c\.?', 'bc'),
            (r'm\.\s*c\.?', 'mc'),
            (r'b\.\s*s\.\s*d\.\s*k\.?', 'bsdk'),
        ]
    
    def detect(self, text):
        """Check if text contains abusive words. Returns (has_abuse, list_of_words)"""
        detected = set()
        text_lower = text.lower()
        
        # Check main pattern
        matches = self.pattern.findall(text_lower)
        detected.update(matches)
        
        # Check dot patterns (b.c., m.c., b.s.d.k)
        for pattern, name in self.dot_patterns:
            match = re.search(pattern, text_lower)
            if match:
                detected.add(name)
        
        # Check Devanagari directly
        for word in self.devanagari_words:
            if word in text:
                detected.add(word)
        
        return len(detected) > 0, list(detected)
    
    def filter_text(self, text, replacement="[FILTERED]"):
        """Replace abusive words with [FILTERED]"""
        result = text
        
        # Replace Roman words
        for word in self.abusive_words:
            result = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE).sub(replacement, result)
        
        # Replace Devanagari words
        for word in self.devanagari_words:
            result = result.replace(word, replacement)
        
        # Replace dot patterns
        for pattern, _ in self.dot_patterns:
            result = re.compile(pattern, re.IGNORECASE).sub(replacement, result)
        
        return result
    
    def is_clean(self, text):
        """Return True if no abusive words found"""
        has_abuse, _ = self.detect(text)
        return not has_abuse

# Initialize the abusive detector
abuse_detector = AbusiveDetector()

# Print detector stats
print("=" * 60)
print("ABUSIVE LANGUAGE DETECTOR LOADED")
print("=" * 60)
print(f"Roman words: {len(abuse_detector.abusive_words)}")
print(f"Devanagari words: {len(abuse_detector.devanagari_words)}")
print(f"TOTAL: {len(abuse_detector.abusive_words) + len(abuse_detector.devanagari_words)} abusive words")
print("=" * 60)

# ---------- Optional Windows beep support ----------
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# ---------- Beep configuration ----------
BEEP_FREQ = 1000
BEEP_DUR = 300

def play_beep(freq=None, dur=None):
    freq = freq or BEEP_FREQ
    dur = dur or BEEP_DUR
    if HAS_WINSOUND and os.name == "nt":
        winsound.Beep(freq, dur)
    else:
        print("\a", end="")

def set_beep_settings(freq: int, dur: int):
    global BEEP_FREQ, BEEP_DUR
    BEEP_FREQ = freq
    BEEP_DUR = dur

// ---------- Site shortcuts ----------
const sites = {
  // Core shortcuts
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
  "gemini": "https://gemini.google.com",
  "copilot": "https://copilot.microsoft.com",
  "claude": "https://claude.ai",
  "deepseek": "https://chat.deepseek.com",
  "cares": "https://codepen.io/Kavyant-Kumar/pen/dPGJPKj?",
  "carelabstudio": "https://www.youtube.com/@CareLabStudio",
  "rickroll": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",

  // Educational (JEE, coding, school)
  "khanacademy": "https://www.khanacademy.org",
  "vedantu": "https://www.vedantu.com",
  "byjus": "https://byjus.com",
  "unacademy": "https://unacademy.com",
  "toppr": "https://www.toppr.com",
  "doubtnut": "https://www.doubtnut.com",
  "physicswallah": "https://www.pw.live",
  "embibe": "https://www.embibe.com",
  "gradeup": "https://gradeup.co",
  "freecodecamp": "https://www.freecodecamp.org",
  "codecademy": "https://www.codecademy.com",
  "sololearn": "https://www.sololearn.com",
  "w3schools": "https://www.w3schools.com",
  "geeksforgeeks": "https://www.geeksforgeeks.org",
  "mycbseguide": "https://mycbseguide.com",
  "learncbse": "https://www.learncbse.in",
  "selfstudys": "https://www.selfstudys.com",
  "nta": "https://nta.ac.in",
  "jeemain": "https://jeemain.nta.nic.in",
  "iitpal": "https://nta.ac.in/lecturesContent",

  // More educational
  "aakashdigital": "https://aakashdigital.com",
  "allen": "https://www.allen.ac.in",
  "fiitjee": "https://www.fiitjee.com",
  "resonance": "https://www.resonance.ac.in",
  "brilliant": "https://brilliant.org",
  "coursera": "https://www.coursera.org",
  "edx": "https://www.edx.org",
  "udacity": "https://www.udacity.com",
  "repl": "https://replit.com",
  "codewars": "https://www.codewars.com",
  "hackerrank": "https://www.hackerrank.com",
  "leetcode": "https://leetcode.com",
  "instructables": "https://www.instructables.com",
  "kiddle": "https://kiddle.co",
  "duolingo": "https://www.duolingo.com",
  "quizlet": "https://quizlet.com",
  "desmos": "https://www.desmos.com/calculator",
  "phet": "https://phet.colorado.edu",
  "ck12": "https://www.ck12.org",
  "openstax": "https://openstax.org",
  "ndlindia": "https://ndl.iitkgp.ac.in",
  "swayam": "https://swayam.gov.in",
  "nroer": "https://nroer.gov.in",
  "diyguru": "https://diyguru.org",
  "vedantujee": "https://www.vedantu.com/jee",

  // Fun (games, quirky, experiments)
  "geoguessr": "https://www.geoguessr.com",
  "wordle": "https://www.nytimes.com/games/wordle",
  "littlealchemy2": "https://littlealchemy2.com",
  "endlesshorse": "https://endless.horse",
  "boredbutton": "https://www.boredbutton.com",
  "uselessweb": "https://www.theuselessweb.com",
  "pointerpointer": "https://pointerpointer.com",
  "catbounce": "https://cat-bounce.com",
  "weavesilk": "https://weavesilk.com",
  "theuselessweb": "https://www.theuselessweb.com",

  "infintecraft": "https://infiniticraft.neocities.org",
  "auctiongame": "https://theauctiongame.com",
  "jigsawpuzzles": "https://www.jigsawpuzzles.io",
  "patatap": "https://www.patatap.com",
  "drawstickman": "https://drawastickman.com",
  "radiogarden": "https://radio.garden",
  "puzzgrid": "https://puzzgrid.com",
  "thissand": "https://thisissand.com",
  "softmurmur": "https://asoftmurmur.com",
  "boredpanda": "https://www.boredpanda.com",
  "mentalfloss": "https://www.mentalfloss.com",
  "thesecretdoor": "https://thesecretdoor.com",
  "window93": "https://windows93.net",
  "jspaint": "https://jspaint.app",
  "wayback": "https://archive.org/web",
  "mobyGames": "https://www.mobygames.com",
  "vintageweb": "https://vintageweb.net",
  "quickdraw": "https://quickdraw.withgoogle.com",
  "pixelflare": "https://pixelflare.com",

  // Anime
  "crunchyroll": "https://www.crunchyroll.com",
  "retrocrush": "https://www.retrocrush.tv",
  "aniwave": "https://aniwave.to",
  "aniwatch": "https://aniwatchtv.to",
  "animeheaven": "https://animeheaven.pro",
  "animesuge": "https://animesuge.to",
  "9anime": "https://9animetv.to",
  "gogoanime": "https://gogoanimes.fi",
  "zoro": "https://zoroxtv.to",
  "hiAnime": "https://hianime.to",
  "tubi": "https://tubitv.com/category/anime",
  "plutoanime": "https://pluto.tv/anime",

  // Minecraft / gaming
  "minecraftnet": "https://www.minecraft.net",
  "hypixel": "https://hypixel.net",
  "mineplex": "https://mineplex.com",
  "mcservers": "https://minecraftservers.org",
  "mcpedl": "https://mcpedl.com",
  "curseforge": "https://www.curseforge.com/minecraft",
  "modrinth": "https://modrinth.com",
  "namecheapmc": "https://minecraft-mp.com",
  "hoplite": "https://hoplite.gg",
  "wynncraft": "https://wynncraft.com",

  // AI tools (coding, creative)
  "huggingface": "https://huggingface.co",
  "replicate": "https://replicate.com",
  "stablediffusionweb": "https://stablediffusionweb.com",
  "cursor": "https://cursor.com",
  "githubcopilot": "https://github.com/features/copilot",
  "midjourney": "https://www.midjourney.com",
  "runwayml": "https://runwayml.com",

  "opencode": "https://github.com/opencode-ai/opencode",
  "aider": "https://aider.chat",
  "continueai": "https://www.continue.dev",
  "geminiassist": "https://gemini.google.com/codeassist",
  "amazonq": "https://aws.amazon.com/q/developer",
  "groq": "https://groq.com",
  "togetherai": "https://www.together.ai",
  "falai": "https://fal.ai",
  "leonardoai": "https://leonardo.ai",

  // Phonk / music
  "soundcloudphonk": "https://soundcloud.com/search?q=phonk",
  "audiomackphonk": "https://audiomack.com/search?q=phonk",
  "monstercatphonk": "https://www.monstercat.com/genre/phonk",
  "phonktracker": "https://www.phonktracker.com",
  "traktrainphonk": "https://traktrain.com/tags/phonk",
  "phonklab": "https://phonklab.com",

  // GitHub / CodePen resources
  "awesome": "https://github.com/sindresorhus/awesome",
  "freeprogbooks": "https://github.com/EbookFoundation/free-programming-books",
  "codinginterview": "https://github.com/jwasham/coding-interview-university",
  "codepenawards": "https://codepen.net/awards",
  "codepenpens": "https://codepen.io/pens",
  "frontenddaily": "https://frontenddaily.com",
  "cssart": "https://codepen.io/tag/CSS%20Art",
  "js13k": "https://js13kgames.com",
  "cssbattle": "https://cssbattle.dev",
  "flexboxfroggy": "https://flexboxfroggy.com",
  "gridgarden": "https://cssgridgarden.com",

  // Search / misc fun / tools
  "brave": "https://brave.com/search",
  "duckduckgo": "https://duckduckgo.com",
  "qwant": "https://www.qwant.com",
  "ecosia": "https://www.ecosia.org",
  "startpage": "https://www.startpage.com",
  "kagi": "https://kagi.com",
  "perplexityai": "https://www.perplexity.ai",
  "youglish": "https://youglish.com",
  "radiooooo": "https://radiooooo.com",
  "neave": "https://www.neave.com/interactive",
  "silk": "https://weavesilk.com",
  "endless": "https://endless.horse",
  "magicbutton": "https://themagicbutton.com",
  "boredhumans": "https://boredhumans.com",
  "maniac": "https://maniac.surge.sh",
  "fallingfall": "https://chrismoreton.com/fallingfall",

  // News (India + global)
  "ndtv": "https://www.ndtv.com",
  "indiatoday": "https://www.indiatoday.in",
  "thehindu": "https://www.thehindu.com",
  "indianexpress": "https://indianexpress.com",
  "timesofindia": "https://timesofindia.indiatimes.com",
  "moneycontrol": "https://www.moneycontrol.com",

  "bbcnews": "https://www.bbc.com/news",
  "aljazeera": "https://www.aljazeera.com",
  "techcrunch": "https://techcrunch.com",
  "wired": "https://www.wired.com",
  "theregister": "https://www.theregister.com",
  "hindustantimes": "https://www.hindustantimes.com",
  "firstpost": "https://www.firstpost.com",
  "scrollin": "https://scroll.in",
  "reuters": "https://www.reuters.com",
  "apnews": "https://apnews.com",
  "bbc": "https://www.bbc.com",
  "cnn": "https://www.cnn.com",
  "foxnews": "https://www.foxnews.com",
  "msnbc": "https://www.msnbc.com"
};
# ---------- Command descriptions ----------
commands = {
    "wiki <topic>": "Wikipedia summary",
    "math": "Solve equations / simplify expressions",
    "open <site>": "Open websites",
    "sites": "List all site shortcuts",
    "time / date / day": "Show current time, date, or day",
    "joke": "Random programming/maths joke",
    "meme": "Random coding meme",
    "motivate": "Short motivation",
    "reminder add <text>": "Add a reminder",
    "reminder list": "List your reminders",
    "note add <text>": "Save a note",
    "note list": "Show all notes",
    "note search <word>": "Search notes",
    "task add <text>": "Add a task",
    "task list": "Show all tasks",
    "task done <n>": "Mark task done",
    "task save/load": "Save/load tasks",
    "jee formula <topic>": "Show built-in formulas",
    "jee load": "Load 1200-formula JEE book",
    "jee topics": "List topics",
    "jee topic <name>": "Show formulas for topic",
    "jee search <keyword>": "Search formulas",
    "focus <minutes>": "Focus timer",
    "timer <seconds>": "Countdown timer",
    "beep set <freq> <ms>": "Set custom beep",
    "beep test": "Test beep",
    "history last": "Show last commands",
    "history stats": "Show usage stats",
    "game": "Guess the number",
    "fun": "Easter egg hints",
    "safety": "India safety tips",
    "setup": "Install packages",
    "shortcuts": "Command shortcuts",
    "terms": "Terms & conditions",
    "version": "Show version",
    "copyright": "Show copyright",
    "help": "Show help menu",
    "about": "About this assistant",
    "credits": "Show credits",
}

# ---------- Core JEE formulas ----------
jee_formulas = {
    "kinematics": ["v = u + at", "s = ut + 1/2 at^2", "v^2 = u^2 + 2as"],
    "laws_of_motion": ["F = m a", "friction f = μ N"],
    "work_energy": ["K = 1/2 m v^2", "U = m g h", "W = ΔK"],
    "gravitation": ["F = G m1 m2 / r^2", "g = G M / R^2", "v_escape = √(2 G M / R)"],
    "electrostatics": ["F = k q1 q2 / r^2", "E = k q / r^2", "V = k q / r"],
    "current_electricity": ["V = I R", "P = V I"],
    "trigonometry": ["sin^2(x) + cos^2(x) = 1", "1 + tan^2(x) = sec^2(x)"],
    "quadratic": ["x = [-b ± √(b^2 - 4ac)] / (2a)"],
    "basic_calculus": ["d/dx (x^n) = n x^(n-1)", "∫ x^n dx = x^(n+1)/(n+1) + C"],
    "thermodynamics": ["ΔU = Q - W", "PV = nRT"],
    "waves": ["v = fλ", "y = A sin(ωt - kx)"],
    "optics": ["1/f = 1/v - 1/u", "μ1 sin θ1 = μ2 sin θ2"],
    "magnetism": ["F = qvB sin θ", "F = BIL sin θ"],
    "modern_physics": ["E = hf", "λ = h/p", "E = mc²"],
    "rotational_motion": ["τ = I α", "L = I ω", "K_rot = 1/2 I ω²"],
    "shm": ["x = A sin(ωt + φ)", "T = 2π√(m/k)", "T = 2π√(L/g)"],
    "vectors": ["A·B = |A||B| cos θ", "A×B = |A||B| sin θ n̂"],
    "logarithms": ["log(ab) = log a + log b", "log(a/b) = log a - log b"],
    "binomial": ["(a+b)^n = Σ nCr a^(n-r) b^r"],
    "probability": ["P(A∪B) = P(A) + P(B) - P(A∩B)", "P(A|B) = P(A∩B) / P(B)"],
}

# ---------- 1200-formula JEE book ----------
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
    return "Available JEE topics:\n" + ", ".join(sorted(JEE_FORMULAS_1200.keys()))

def show_jee_topic(topic: str):
    if not JEE_FORMULAS_1200:
        return "JEE formula book not loaded. Use 'jee load' first."
    topic = topic.strip()
    if topic not in JEE_FORMULAS_1200:
        return "No such topic. Use 'jee topics' to see all."
    lines = [f"Formulas for {topic}:"]
    for i, fml in enumerate(JEE_FORMULAS_1200[topic], 1):
        lines.append(f"  {i}. {fml}")
    return "\n".join(lines)

def search_jee_formula(keyword: str):
    if not JEE_FORMULAS_1200:
        return "JEE formula book not loaded. Use 'jee load' first."
    results = []
    for topic, flist in JEE_FORMULAS_1200.items():
        for fml in flist:
            if keyword.lower() in fml.lower():
                results.append(f"[{topic}] {fml}")
    if not results:
        return "No formulas found matching that keyword."
    return "Search results:\n" + "\n".join(results[:50])

# ---------- Wikipedia setup ----------
wikipedia.set_lang("en")

def wiki_search(query):
    try:
        return wikipedia.summary(query, sentences=2)
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
]
motivations = [
    "Small consistent study sessions beat 1 big panic session.",
    "Every bug you fix is literally XP for your brain.",
    "You don't need perfect focus, just remove one distraction and start.",
]

def add_reminder(text: str):
    reminders.append(text)
    return f"Reminder added: {text}"

def list_reminders():
    if not reminders:
        return "You have no reminders yet."
    return "\n".join(f"{i}. {r}" for i, r in enumerate(reminders, 1))

def get_time():
    return datetime.datetime.now().strftime("Current time: %H:%M:%S, Date: %d-%m-%Y")

def get_day():
    return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][datetime.datetime.today().weekday()]

def get_joke():
    return random.choice(jokes)

def get_meme():
    return random.choice(memes)

def get_motivation():
    return random.choice(motivations)

# ---------- Notes ----------
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
    return "\n".join(found) if found else "No notes found with that word."

# ---------- Tasks ----------
tasks = []

def add_task(text: str):
    tasks.append({"text": text, "done": False})
    return f"Task added: {text}"

def list_tasks():
    if not tasks:
        return "You have no tasks yet."
    return "\n".join(f"[{'✓' if t['done'] else ' '}] {i}. {t['text']}" for i, t in enumerate(tasks, 1))

def done_task(index: int):
    if 1 <= index <= len(tasks):
        tasks[index-1]["done"] = True
        return f"Task {index} marked as done."
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
    entry = {"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "command": command}
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
    return "\n".join(f"{e['time']} → {e['command']}" for e in history[-n:])

def show_history_stats():
    if not history:
        return "No history yet."
    counts = {}
    for h in history:
        cmd = h["command"].split()[0] if h["command"] else ""
        counts[cmd] = counts.get(cmd, 0) + 1
    top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]
    return f"Total commands: {len(history)}\nMost used commands:\n" + "\n".join(f"  - {cmd}: {c} times" for cmd, c in top)

# ---------- Game ----------
def play_guess():
    secret = random.randint(1, 20)
    print("AI: I picked a number between 1 and 20. Type 'q' to quit.")
    tries = 0
    while True:
        guess = input("Your guess: ").strip()
        if guess.lower() == "q":
            print(f"AI: Game ended. The number was {secret}")
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
    print(f"AI: Focus timer started for {minutes} minutes.")
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
    print("AI: Entering matrix mode...")
    for _ in range(lines):
        row = "".join(random.choice(chars) for _ in range(width))
        print(row)
        time.sleep(delay)
    print("AI: Matrix mode ended. Back to reality.")

# ========== MAIN LOOP ==========
print("\n" + "=" * 60)
print("AI: Hi! I am your smart Python AI with Abusive Language Detection.")
print("AI: I will detect and filter abusive language automatically.")
print("=" * 60)
print("\nAI: What I can do:")
print("  - wiki <topic>     - open <site>     - math")
print("  - time/date/day    - joke/meme/motivate")
print("  - reminder add/list  - note add/list/search")
print("  - task add/list/done/save/load")
print("  - jee formula <topic>  - jee load/topics/topic/search")
print("  - focus <minutes>  - timer <seconds>")
print("  - beep set/test    - history last/stats")
print("  - game             - matrix")
print("  - safety           - setup - shortcuts - terms")
print("  - about            - credits - version - copyright")
print("  - help / sites / fun")
print("\nType 'bye' to exit.\n")

current_hour = datetime.datetime.now().hour
if current_hour < 12:
    greet = "Good morning"
elif current_hour < 18:
    greet = "Good afternoon"
else:
    greet = "Good evening"
print(f"AI: {greet}, Kavyant! (v{__version__})\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    
    lower = user_input.lower()
    
    # ===== ABUSIVE LANGUAGE CHECK =====
    has_abuse, bad_words = abuse_detector.detect(user_input)
    if has_abuse:
        print(f"AI: ⚠️ ABUSIVE LANGUAGE DETECTED! Please be respectful.")
        print(f"AI: Detected: {', '.join(bad_words)}")
        print(f"AI: Filtered: {abuse_detector.filter_text(user_input)}")
        add_history_entry(f"[ABUSE] {user_input}")
    else:
        add_history_entry(lower)
    
    # Exit commands
    if lower in ("bye", "exit", "quit"):
        print("AI: Goodbye! Keep coding and studying!")
        break
    
    # Wiki
    if lower.startswith("wiki "):
        topic = user_input[5:].strip()
        if topic:
            print("AI: Searching Wikipedia...")
            print("AI:", wiki_search(topic))
        else:
            print("AI: Please type something after 'wiki'.")
    
    # Open sites
    elif lower.startswith("open "):
        key = lower[5:].strip()
        if key in sites:
            print(f"AI: Opening {key}...")
            webbrowser.open(sites[key])
        else:
            print("AI: I don't know that site yet. Type 'sites' to see all options.")
    
    # Help
    elif lower == "help":
        print("AI: Here are my commands:")
        for cmd, desc in commands.items():
            print(f"  - {cmd:20} → {desc}")
    
    # Sites list
    elif lower in ("sites", "open list"):
        print("AI: You can 'open' these sites:")
        print(", ".join(sorted(sites.keys())))
    
    # About
    elif lower == "about":
        print(f"AI: I am a Python assistant (v{__version__}) made by Kavyant Kumar.")
        print("AI: I help with web, wiki, math, notes, reminders, tasks, JEE formulas, timers, and abuse detection.")
    
    # Credits
    elif lower == "credits":
        print("AI: Project: Smart Python Assistant (CLI)")
        print("AI: Creator: Kavyant Kumar (Cares & Laughs – Your Fun Lab / CareLabStudio)")
        print("AI: Built with: Python, wikipedia, sympy, and pure curiosity.")
        print("AI: Year: 2026 | Location: Ghaziabad, India")
    
    # Version
    elif lower == "version":
        print(f"AI: Current version: v{__version__}")
    
    # Copyright
    elif lower == "copyright":
        print("AI: © 2026 Kavyant Kumar. All rights reserved.")
    
    # Fun
    elif lower == "fun":
        print("AI: Try typing things like:")
        print("  - 'import this', 'antigravity', 'cowsay', 'matrix'")
        print("  - 'kavyant secret', 'hack system', 'rick roll'")
        print("  - 'open gemini', 'open chatgpt', 'open claude'")
    
    # Setup
    elif lower == "setup":
        print("AI: To install required packages, run:")
        print("  pip install wikipedia sympy")
    
    # Shortcuts
    elif lower == "shortcuts":
        print("AI: Quick shortcuts:")
        print("  - 'help' - 'sites' - 'about' - 'credits' - 'version'")
        print("  - 'safety' - 'terms' - 'fun' - 'game' - 'matrix'")
    
    # Terms
    elif lower == "terms":
        print("AI: Terms & Conditions:")
        print("1) Educational & Entertainment purpose only")
        print("2) No liability for misuse or wrong information")
        print("3) Be kind, legal, and respectful")
        print("4) Do not share personal info like passwords or OTPs")
        print("5) By using this assistant, you agree to these terms")
    
    # Safety
    elif lower == "safety":
        print("AI: SAFETY TIPS & HELPLINES (India)")
        print("-" * 40)
        print("Emergency: 112 (all), 100 (police), 108 (ambulance)")
        print("Cybercrime: 1930 or cybercrime.gov.in")
        print("Child Helpline: 1098")
        print("Women Helpline: 1091 / 181")
        print("Mental Health (KIRAN): 1800-599-0019")
        print("-" * 40)
        print("⚠️ Never share OTPs, passwords, or personal info online!")
        print("⚠️ Think before you click unknown links!")
    
    # Reminders
    elif lower.startswith("reminder add "):
        text = user_input[13:].strip()
        if text:
            print("AI:", add_reminder(text))
        else:
            print("AI: Please write something after 'reminder add'.")
    elif lower == "reminder list":
        print("AI:", list_reminders())
    
    # Notes
    elif lower.startswith("note add "):
        text = user_input[9:].strip()
        if text:
            print("AI:", add_note(text))
        else:
            print("AI: Please write something after 'note add'.")
    elif lower == "note list":
        print("AI:", show_notes())
    elif lower.startswith("note search "):
        word = user_input[12:].strip()
        if word:
            print("AI:", search_notes(word))
        else:
            print("AI: Please provide a word after 'note search'.")
    
    # Tasks
    elif lower.startswith("task add "):
        text = user_input[9:].strip()
        if text:
            print("AI:", add_task(text))
        else:
            print("AI: Please write something after 'task add'.")
    elif lower == "task list":
        print("AI:\n" + list_tasks())
    elif lower.startswith("task done "):
        try:
            n = int(user_input[10:].strip())
            print("AI:", done_task(n))
        except ValueError:
            print("AI: Please give a valid task number after 'task done'.")
    elif lower == "task save":
        print("AI:", save_tasks())
    elif lower == "task load":
        print("AI:", load_tasks())
    
    # History
    elif lower == "history last":
        print("AI:", show_last_history())
    elif lower == "history stats":
        print("AI:", show_history_stats())
    
    # JEE
    elif lower == "jee load":
        print("AI:", load_jee_formula_book())
    elif lower == "jee topics":
        print("AI:", list_jee_topics())
    elif lower.startswith("jee topic "):
        tname = user_input[10:].strip()
        if tname:
            print("AI:", show_jee_topic(tname))
        else:
            print("AI: Please provide a topic name after 'jee topic'.")
    elif lower.startswith("jee search "):
        key = user_input[11:].strip()
        if key:
            print("AI:", search_jee_formula(key))
        else:
            print("AI: Please provide a keyword after 'jee search'.")
    elif lower.startswith("jee formula "):
        topic = lower[12:].strip()
        if topic in jee_formulas:
            print(f"AI: Formulas for {topic}:")
            for f in jee_formulas[topic]:
                print(f"  - {f}")
        else:
            print("AI: I don't have formulas for that topic yet.")
    
    # Timers
    elif lower.startswith("focus "):
        try:
            mins = int(lower[6:].strip())
            focus_timer(mins)
        except ValueError:
            print("AI: Please give minutes like 'focus 25'.")
    elif lower.startswith("timer "):
        try:
            secs = int(lower[6:].strip())
            if secs <= 0:
                print("AI: Please give a positive number of seconds.")
            else:
                countdown_timer(secs)
        except ValueError:
            print("AI: Please give seconds like 'timer 30'.")
    
    # Beep
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
    
    # Matrix
    elif lower == "matrix":
        matrix_rain()
    
    # Time/Date/Day
    elif "time" in lower or "date" in lower:
        print("AI:", get_time())
    elif lower == "day":
        print("AI: Today is", get_day())
    
    # Joke/Meme/Motivate
    elif lower == "joke":
        print("AI:", get_joke())
    elif lower == "meme":
        print("AI:", get_meme())
    elif lower == "motivate":
        print("AI:", get_motivation())
    
    # Game
    elif lower == "game":
        play_guess()
    
    # Math
    elif is_math(lower):
        handle_math(user_input)
    
    # Easter eggs
    elif "import this" in lower:
        print("AI: Nice, you know the Zen of Python. Readability counts.")
    elif "antigravity" in lower:
        print("AI: Opening a secret Python comic for you...")
        webbrowser.open("https://xkcd.com/353/")
    elif "hello world" in lower:
        print("AI: Hello World!")
    elif "from future import braces" in lower:
        print("AI: SyntaxError: not a chance (Python is loyal to indentation).")
    elif "kavyant secret" in lower:
        print("AI: Welcome to the Fun Lab secret room 🧪")
    elif lower == "hack system":
        print("AI: Initializing hack protocol...")
        time.sleep(0.5)
        print("AI: 0%... 25%... 50%... 75%... 100%")
        print("AI: Just kidding. Stay ethical, hacker.")
    elif lower == "cowsay":
        print(r"  ^__^")
        print(r"  (oo)\_______")
        print(r"  (__)\       )\/\ ")
        print(r"      ||----w |")
        print(r"      ||     ||")
    elif "rick roll" in lower or "rickroll" in lower:
        print("AI: Never gonna give you up...")
        webbrowser.open(sites.get("rickroll", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    elif "good night" in lower or lower == "gn":
        print("AI: Good night! Sleep well and crush it tomorrow.")
    elif lower in ("hello", "hi"):
        print("AI: Hello! How are you feeling today?")
    elif "sad" in lower:
        print("AI: I'm sorry you feel sad. Want to talk about it?")
    elif "study" in lower or "jee" in lower:
        print("AI: Remember: small steps daily. What topic are you on?")
    elif "code" in lower or "coding" in lower:
        print("AI: Coding + JEE together is powerful. What project are you working on?")
    else:
        print("AI: I don't fully understand. Try 'help' for commands.") # ========== MAIN LOOP WITH EMOJIS ==========
print("\n" + "=" * 60)
print("🤖 AI: Namaste! I am your smart Python AI with Abusive Language Detection!")
print("🛡️ AI: I will detect and filter abusive language automatically.")
print("=" * 60)
print("\n✨ What I can do:")
print("  📚 wiki <topic>     🌐 open <site>     🧮 math")
print("  ⏰ time/date/day    😂 joke/meme       💪 motivate")
print("  📝 reminder add/list  📓 note add/list/search")
print("  ✅ task add/list/done/save/load")
print("  📖 jee formula <topic>  📚 jee load/topics/topic/search")
print("  🎯 focus <minutes>  ⏱️ timer <seconds>")
print("  🔔 beep set/test    📜 history last/stats")
print("  🎮 game             💻 matrix")
print("  🛡️ safety           ⚙️ setup - 🔗 shortcuts - 📜 terms")
print("  ℹ️ about            👏 credits - 🔢 version - ©️ copyright")
print("  ❓ help / 🌐 sites / 🎉 fun")
print("\n💬 Type 'bye' to exit.\n")

current_hour = datetime.datetime.now().hour
if current_hour < 12:
    greet = "🌅 Good morning"
elif current_hour < 18:
    greet = "☀️ Good afternoon"
else:
    greet = "🌙 Good evening"
print(f"🤖 AI: {greet}, Kavyant! (v{__version__}) 🎉\n")

while True:
    user_input = input("👤 You: ").strip()
    if not user_input:
        continue
    
    lower = user_input.lower()
    
    # ===== ABUSIVE LANGUAGE CHECK WITH EMOJIS =====
    has_abuse, bad_words = abuse_detector.detect(user_input)
    if has_abuse:
        print(f"🤖 AI: 🚫⛔ ABUSIVE LANGUAGE DETECTED! Please be respectful. 🛡️")
        print(f"🤖 AI: 🔍 Detected: {', '.join(bad_words)}")
        print(f"🤖 AI: ✨ Filtered: {abuse_detector.filter_text(user_input)}")
        add_history_entry(f"[ABUSE] {user_input}")
    else:
        add_history_entry(lower)
    
    # Exit commands
    if lower in ("bye", "exit", "quit"):
        print("🤖 AI: 👋 Goodbye! Keep coding and studying! 📚💪")
        print("🤖 AI: 🙏 Have a great day! 🌟")
        break
    
    # Wiki
    if lower.startswith("wiki "):
        topic = user_input[5:].strip()
        if topic:
            print("🤖 AI: 📚 Searching Wikipedia... 🔍")
            print("🤖 AI:", wiki_search(topic))
        else:
            print("🤖 AI: 📝 Please type something after 'wiki'.")
    
    # Open sites
    elif lower.startswith("open "):
        key = lower[5:].strip()
        if key in sites:
            print(f"🤖 AI: 🌐 Opening {key}... 🚀")
            webbrowser.open(sites[key])
        else:
            print("🤖 AI: ❌ I don't know that site yet. Type 'sites' to see all options.")
    
    # Help
    elif lower == "help":
        print("🤖 AI: 📚 Here are my commands:")
        for cmd, desc in commands.items():
            print(f"  - {cmd:20} → {desc}")
    
    # Sites list
    elif lower in ("sites", "open list"):
        print("🤖 AI: 🌐 You can 'open' these sites:")
        print("📁 " + ", ".join(sorted(sites.keys())))
    
    # About
    elif lower == "about":
        print(f"🤖 AI: ℹ️ I am a Python assistant (v{__version__}) made by Kavyant Kumar.")
        print("🤖 AI: 🛠️ I help with web, wiki, math, notes, reminders, tasks, JEE formulas, timers, and abuse detection.")
        print("🤖 AI: ❤️ Made with love at Cares & Laughs – Your Fun Lab!")
    
    # Credits
    elif lower == "credits":
        print("🤖 AI: 👏 Project: Smart Python Assistant (CLI)")
        print("🤖 AI: 👨‍💻 Creator: Kavyant Kumar (Cares & Laughs – Your Fun Lab / CareLabStudio)")
        print("🤖 AI: 🐍 Built with: Python, wikipedia, sympy, and pure curiosity.")
        print("🤖 AI: 📍 Year: 2026 | Location: Ghaziabad, India")
        print("🤖 AI: 🙏 If you like this, please subscribe to CareLabStudio on YouTube!")
    
    # Version
    elif lower == "version":
        print(f"🤖 AI: 🔢 Current version: v{__version__}")
    
    # Copyright
    elif lower == "copyright":
        print("🤖 AI: ©️ 2026 Kavyant Kumar. All rights reserved.")
    
    # Fun
    elif lower == "fun":
        print("🤖 AI: 🎉 Try typing things like:")
        print("  - 'import this' 🐍, 'antigravity' 🚀, 'cowsay' 🐮, 'matrix' 💻")
        print("  - 'kavyant secret' 🤫, 'hack system' 🔓, 'rick roll' 🎵")
        print("  - 'open gemini' 🤖, 'open chatgpt' 💬, 'open claude' 🧠")
        print("  - 'open cares' 🎨, 'open carelabstudio' 📺")
    
    # Setup
    elif lower == "setup":
        print("🤖 AI: ⚙️ To install required packages, run:")
        print("  📦 pip install wikipedia sympy")
        print("  🔧 Or: python -m pip install wikipedia sympy")
    
    # Shortcuts
    elif lower == "shortcuts":
        print("🤖 AI: 🔗 Quick shortcuts:")
        print("  - 'help' ❓ - 'sites' 🌐 - 'about' ℹ️ - 'credits' 👏")
        print("  - 'version' 🔢 - 'safety' 🛡️ - 'terms' 📜 - 'fun' 🎉")
        print("  - 'game' 🎮 - 'matrix' 💻 - 'cowsay' 🐮")
    
    # Terms
    elif lower == "terms":
        print("🤖 AI: 📜 Terms & Conditions:")
        print("1️⃣ Educational & Entertainment purpose only")
        print("2️⃣ No liability for misuse or wrong information")
        print("3️⃣ Be kind, legal, and respectful")
        print("4️⃣ Do not share personal info like passwords or OTPs")
        print("5️⃣ By using this assistant, you agree to these terms")
        print("🤖 AI: 🙏 Thank you for being responsible!")
    
    # Safety
    elif lower == "safety":
        print("🤖 AI: 🛡️ SAFETY TIPS & HELPLINES (India)")
        print("=" * 50)
        print("📞 EMERGENCY NUMBERS:")
        print("  🚨 112 - All emergencies (Police/Fire/Medical)")
        print("  👮 100 - Police")
        print("  🚒 101 - Fire")
        print("  🚑 102/108 - Ambulance")
        print("  👧 1098 - Child Helpline")
        print("  👩 1091/181 - Women Helpline")
        print("  💻 1930 - Cybercrime Helpline")
        print("  🧠 1800-599-0019 - Mental Health (KIRAN)")
        print("=" * 50)
        print("⚠️ SAFETY TIPS:")
        print("  🔐 Never share OTPs, passwords, or personal info online!")
        print("  🚫 Think before you click unknown links!")
        print("  📱 Report suspicious messages immediately!")
        print("  👨‍👩‍👧 Tell a trusted adult if something feels wrong!")
        print("  🙏 Stay safe, stay aware!")
    
    # Reminders
    elif lower.startswith("reminder add "):
        text = user_input[13:].strip()
        if text:
            print("🤖 AI:", add_reminder(text), "📝")
        else:
            print("🤖 AI: 📝 Please write something after 'reminder add'.")
    elif lower == "reminder list":
        print("🤖 AI: 📋", list_reminders())
    
    # Notes
    elif lower.startswith("note add "):
        text = user_input[9:].strip()
        if text:
            print("🤖 AI:", add_note(text), "📓")
        else:
            print("🤖 AI: 📓 Please write something after 'note add'.")
    elif lower == "note list":
        print("🤖 AI: 📚", show_notes())
    elif lower.startswith("note search "):
        word = user_input[12:].strip()
        if word:
            print("🤖 AI: 🔍", search_notes(word))
        else:
            print("🤖 AI: 📝 Please provide a word after 'note search'.")
    
    # Tasks
    elif lower.startswith("task add "):
        text = user_input[9:].strip()
        if text:
            print("🤖 AI:", add_task(text), "✅")
        else:
            print("🤖 AI: ✅ Please write something after 'task add'.")
    elif lower == "task list":
        print("🤖 AI: 📋\n" + list_tasks())
    elif lower.startswith("task done "):
        try:
            n = int(user_input[10:].strip())
            print("🤖 AI:", done_task(n), "🎉")
        except ValueError:
            print("🤖 AI: 🔢 Please give a valid task number after 'task done'.")
    elif lower == "task save":
        print("🤖 AI:", save_tasks(), "💾")
    elif lower == "task load":
        print("🤖 AI:", load_tasks(), "📂")
    
    # History
    elif lower == "history last":
        print("🤖 AI: 📜", show_last_history())
    elif lower == "history stats":
        print("🤖 AI: 📊", show_history_stats())
    
    # JEE
    elif lower == "jee load":
        print("🤖 AI:", load_jee_formula_book(), "📚")
    elif lower == "jee topics":
        print("🤖 AI:", list_jee_topics(), "📖")
    elif lower.startswith("jee topic "):
        tname = user_input[10:].strip()
        if tname:
            print("🤖 AI:", show_jee_topic(tname), "📝")
        else:
            print("🤖 AI: 📚 Please provide a topic name after 'jee topic'.")
    elif lower.startswith("jee search "):
        key = user_input[11:].strip()
        if key:
            print("🤖 AI:", search_jee_formula(key), "🔍")
        else:
            print("🤖 AI: 🔍 Please provide a keyword after 'jee search'.")
    elif lower.startswith("jee formula "):
        topic = lower[12:].strip()
        if topic in jee_formulas:
            print(f"🤖 AI: 📖 Formulas for {topic}:")
            for f in jee_formulas[topic]:
                print(f"  📐 {f}")
        else:
            print("🤖 AI: ❌ I don't have formulas for that topic yet.")
    
    # Timers
    elif lower.startswith("focus "):
        try:
            mins = int(lower[6:].strip())
            focus_timer(mins)
        except ValueError:
            print("🤖 AI: 🎯 Please give minutes like 'focus 25'.")
    elif lower.startswith("timer "):
        try:
            secs = int(lower[6:].strip())
            if secs <= 0:
                print("🤖 AI: ⏱️ Please give a positive number of seconds.")
            else:
                countdown_timer(secs)
        except ValueError:
            print("🤖 AI: ⏱️ Please give seconds like 'timer 30'.")
    
    # Beep
    elif lower.startswith("beep set "):
        parts = lower.split()
        if len(parts) == 4:
            try:
                freq = int(parts[2])
                dur = int(parts[3])
                if freq < 37 or freq > 32767:
                    print("🤖 AI: 🔊 Frequency must be between 37 and 32767 Hz.")
                else:
                    set_beep_settings(freq, dur)
                    print(f"🤖 AI: 🔊 Beep settings updated to {freq} Hz, {dur} ms. 🔔")
                    play_beep()
            except ValueError:
                print("🤖 AI: 🔢 Use numbers like 'beep set 1000 300'.")
        else:
            print("🤖 AI: 🔊 Use: beep set <freq> <ms>  e.g. 'beep set 800 200'.")
    elif lower == "beep test":
        print("🤖 AI: 🔊 Playing test beep with current settings... 🔔")
        play_beep()
        print("🤖 AI: ✅ Beep test complete!")
    
    # Matrix
    elif lower == "matrix":
        matrix_rain()
    
    # Time/Date/Day
    elif "time" in lower or "date" in lower:
        print("🤖 AI:", get_time(), "📅")
    elif lower == "day":
        print("🤖 AI: 📆 Today is", get_day())
    
    # Joke/Meme/Motivate
    elif lower == "joke":
        print("🤖 AI: 😂", get_joke())
    elif lower == "meme":
        print("🤖 AI: 🎭", get_meme())
    elif lower == "motivate":
        print("🤖 AI: 💪", get_motivation())
    
    # Game
    elif lower == "game":
        play_guess()
    
    # Math
    elif is_math(lower):
        handle_math(user_input)
    
    # Easter eggs
    elif "import this" in lower:
        print("🤖 AI: 🐍 Zen of Python! Readability counts. 📖")
    elif "antigravity" in lower:
        print("🤖 AI: 🚀 Opening xkcd comic for you...")
        webbrowser.open("https://xkcd.com/353/")
    elif "hello world" in lower:
        print("🤖 AI: 🌍 Hello World! 👋")
    elif "from future import braces" in lower:
        print("🤖 AI: ❌ SyntaxError: not a chance (Python is loyal to indentation). 😂")
    elif "kavyant secret" in lower:
        print("🤖 AI: 🧪 Welcome to the Fun Lab secret room! 🤫")
        print("🤖 AI: 🔬 Keep building cool stuff! 💪")
    elif lower == "hack system":
        print("🤖 AI: 🔓 Initializing hack protocol...")
        time.sleep(0.5)
        print("🤖 AI: 0%... 25%... 50%... 75%... 100%")
        print("🤖 AI: 😂 Just kidding. Stay ethical, hacker! 🛡️")
    elif lower == "cowsay":
        print(r"  ^__^")
        print(r"  (oo)\_______")
        print(r"  (__)\       )\/\ ")
        print(r"      ||----w |")
        print(r"      ||     ||")
        print("🤖 AI: 🐮 Moooo! 🐄")
    elif "rick roll" in lower or "rickroll" in lower:
        print("🤖 AI: 🎵 Never gonna give you up... 🎶")
        webbrowser.open(sites.get("rickroll", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    elif "good night" in lower or lower == "gn":
        print("🤖 AI: 🌙 Good night! Sleep well and crush it tomorrow! 😴💪")
    elif lower in ("hello", "hi"):
        print("🤖 AI: 👋 Hello! How are you feeling today? 😊")
        print("🤖 AI: 💬 Type 'help' to see what I can do!")
    elif "sad" in lower:
        print("🤖 AI: 😔 I'm sorry you feel sad.")
        print("🤖 AI: 🤗 Want to talk about it or take a small break?")
        print("🤖 AI: 🌟 Remember, this too shall pass!")
    elif "study" in lower or "jee" in lower:
        print("🤖 AI: 📚 Remember: small steps daily = big results! 🎯")
        print("🤖 AI: 💪 What topic are you studying right now?")
    elif "code" in lower or "coding" in lower:
        print("🤖 AI: 💻 Coding + JEE together = Super powerful! 🦸")
        print("🤖 AI: 🚀 What project are you working on?")
    elif "thank" in lower or "thanks" in lower:
        print("🤖 AI: 🙏 You're welcome! Happy to help! 😊")
        print("🤖 AI: 🌟 Keep shining and keep coding!")
    else:
        print("🤖 AI: 🤔 I don't fully understand. Try 'help' for commands. ❓")
