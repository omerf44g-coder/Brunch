# Brunch - Advanced Word-Based Passlist Generator

Brunch is a customized, targeted wordlist generator designed for penetration testing and CTF challenges. Unlike traditional character-based generators, Brunch takes specific target keywords and creates highly probable password combinations including leet speak, capitalization variations, and common suffixes.

## Features
- Generates permutations from targeted word lists.
- Interactive CLI menu and one-line command execution.
- Automated Leet Speak variations (e.g., a -> @, e -> 3).
- Common suffix additions (e.g., !, 2026, _).
- Length filtering (Min/Max).
- Reads input words directly from terminal or a `.txt` file.

## Installation
\`\`\`bash
git clone https://github.com/omerf44g-coder/brunch.git
cd brunch
pip install -r requirements.txt
\`\`\`
*(Note: Ensure you have `tqdm` installed for the progress bar).*

## Usage
**Interactive Mode:**
\`\`\`bash
python3 brunch.py
\`\`\`

**CLI Mode:**
\`\`\`bash
python3 brunch.py -w admin,cyber,123 -o custom_list.txt --leet --suffix --min 6 --max 15
\`\`\`