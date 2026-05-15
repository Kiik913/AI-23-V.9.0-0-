Imagine an AI that doesn’t just answer questions, but wanders through ideas with you—AI‑23 (v.10.1.0) is built like a playful browser‑lab where chat, search, and tiny interactive experiments all live together in one place. It grows out of the “Cares & Laughs” universe, so every prank, twist, or visual surprise is meant to feel like a gentle nudge and a shared joke, not a jump scare. If you’re curious about what this looks like in action, you can watch the worlds behind it unfold on my YouTube channel, Care Lab Studio (@CareLabStudio), where I mix anime vibes, creative edits, and experiments from the lab into short, snackable videos. On Instagram, over at @kavyanthub, you can peek behind the curtain—small moments, ideas in progress, and the human side of building “loving pranks” and interactive toys for the web. Together, these spaces turn AI‑23 into more than just an app: it becomes a small ecosystem where you can explore, laugh, learn, and maybe even get inspired to build your own strange, kind, and curious creations.

Under the hood, AI‑23 is a Python‑powered lab assistant that can chat, fetch knowledge, solve maths, keep tiny memories, and run small toys like timers or games—all from one file. It uses the wikipedia library to pull summaries and page data directly from Wikipedia, and sympy to work with equations and expressions symbolically, so it can actually “think” with algebra instead of just doing calculator‑style numbers. Even if you are new to Python, the goal is that you can start by just typing messages and simple commands, and slowly slide into editing the code, adding your own tricks, or wiring in new tools as you get more confident.

Installation – Python Dependencies (Step by Step)
To unlock the smarter parts of AI‑23, you install two add‑ons (called packages) using a tool named pip. PyPI (the Python Package Index) is like an official app store for Python code, and pip downloads packages from there for you so your script can import them.

1. Check Python
Make sure Python 3 is installed on your system.

On Windows you usually run py or python; on Linux/macOS you usually run python3.

2. Install required packages
For Windows (with PyLauncher)
Open Command Prompt and run:

bash
py -m pip install wikipedia
py -m pip install sympy
py -m pip tells Windows to use Python’s built‑in package manager so the libraries get installed into the same Python that runs your script. wikipedia lets AI‑23 search and read Wikipedia data from Python, and sympy lets it solve equations or simplify expressions symbolically, not just calculate numbers.

For Linux / macOS (python3)
Open Terminal and run:

bash
python3 -m pip install wikipedia
python3 -m pip install sympy
python3 -m pip does the same job on Linux/macOS—installing packages from PyPI into your current Python 3 environment so import wikipedia and import sympy work without errors.

After this, you can write code like:

python
import wikipedia        # pull summaries, titles, and links from Wikipedia
import sympy as sp      # work with symbols like x, build equations, and solve them
Once these are installed, they’re ready to be imported into AI‑23 and any other Python project you create, so even a new user can gradually move from “click and explore” to “code and create” without needing advanced setup knowledge.

How to Run and Play With AI‑23
Open a terminal or command prompt in the folder where AI@23.py is saved.

Make sure you’ve installed wikipedia and sympy using the commands above.

Start the AI:

Windows:

bash
py AI@23.py
Linux / macOS:

bash
python3 AI@23.py
Wait for the intro banner, then start typing:

Normal messages, for chat and mood/motivation replies.

wiki your topic to fetch a short Wikipedia summary.

Maths like 3*x + 4 = 19 or x^2 + 5x + 6 to let the sympy brain solve or simplify.

Any extra commands you’ve wired in (notes, tasks, timers, games) based on your latest AI‑23 logic.
