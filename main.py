#!/usr/bin/env python3
"""The Tired Dark Lord: A 100-Word Villain Monologue.

Writes one original 100-word monologue, spoken by a fantasy villain who is
secretly just very tired, to /output/entry.txt.

Craft notes (from the kit's judge brief, most important first):
1. About 100 words, on subject: a tired villain's monologue.
2. The tiredness is FELT, never announced: no "tired", "weary",
   "exhausted", "sleepy" or the like anywhere in the text. It lives in
   the rhythm -- trailing off mid-sentence, losing the thread, forgetting
   the hero's name, filing the apocalypse under taxes.
3. A specific villain with a history and a scheme, not a generic dark
   lord: his speechwriter died of old age waiting; his eclipse rite
   needs the hero's blood, sword and name; his ledger, his sticking
   third step, his cold floor.
4. Speakable in one breath, with a turn/sting in the last line: the
   dreaded kneel-or-die moment collapses into "...you may as well sit."
5. Exactly 100 words, every one earning its place; 529 characters,
   inside the gate's 1-600 character limit.
"""

import os

ENTRY = (
    "Come in. Mind the\u2014 the step. Third one. It sticks.\n"
    "\n"
    "You expected thunder, I know. A throne. A speech. I had one once. "
    "It was... longer. Sharper. The boy who wrote it died of old age, "
    "which tells you about how long this has taken.\n"
    "\n"
    "Yes, the eclipse. Yes, the crown. The rite needs your blood, your "
    "sword, your\u2014 what was it. Oh. Your name. I wrote it down "
    "somewhere. In the ledger. Under... taxes.\n"
    "\n"
    "Kneel. Or don't. The floor is cold either way, and honestly, hero\u2014\n"
    "\n"
    "...you may as well sit. This will take a moment. It always does."
)

# Words that would ANNOUNCE the tiredness instead of showing it.
# The judge's criterion 2 demotes any entry that simply says the
# villain is weary, so the entry must contain none of these.
BANNED_ANNOUNCEMENTS = (
    "tired", "weary", "weariness", "exhausted", "exhaustion",
    "sleepy", "sleepiness", "fatigue", "fatigued", "drowsy",
    "worn out", "dead on my feet", "running on empty",
)


def check_is_text(text):
    if not isinstance(text, str):
        raise ValueError("entry must be a string")


def check_not_blank(text):
    if not text.strip():
        raise ValueError("entry must not be only white space")


def check_utf8(text):
    text.encode("utf-8")  # raises if not encodable


def check_length(text):
    # Gate: /output/entry.txt is UTF-8 text of 1 to 600 characters.
    if not 1 <= len(text) <= 600:
        raise ValueError(
            "entry must be 1-600 characters, got %d" % len(text)
        )


def check_word_count(text):
    # Judge criterion 5: stays near 100 words. We aim for exactly 100.
    words = text.split()
    if not 95 <= len(words) <= 105:
        raise ValueError(
            "entry must be about 100 words, got %d" % len(words)
        )


def check_tiredness_shown_not_announced(text):
    lowered = text.lower()
    for word in BANNED_ANNOUNCEMENTS:
        if word in lowered:
            raise ValueError(
                "entry announces tiredness with %r; it must be felt, "
                "not stated" % word
            )


def check_villainy(text):
    # Criterion 3: a specific villain with a history and a scheme --
    # the entry must carry the scheme (eclipse rite) and the history
    # (the speechwriter who died of old age).
    lowered = text.lower()
    for anchor in ("eclipse", "rite", "old age"):
        if anchor not in lowered:
            raise ValueError("entry is missing its scheme/history anchor %r" % anchor)


def check_sting(text):
    # Criterion 4: a turn or sting lands in the last line.
    last_line = text.strip().splitlines()[-1]
    if "sit" not in last_line.lower():
        raise ValueError("last line must carry the sting")


def validate_structure(text):
    """Gates: the file must be well-formed UTF-8 text in range."""
    check_is_text(text)
    check_not_blank(text)
    check_utf8(text)
    check_length(text)


def validate_shape(text):
    """Shape: about 100 words, spoken as one monologue."""
    check_word_count(text)


def check_paragraph_breaks(text):
    # A monologue spoken in beats: at least two blank-line breaks
    # separate the approach, the scheme and the kneel.
    if text.count("\n\n") < 2:
        raise ValueError("entry must breathe in at least three beats")


def check_em_dash_trailing_off(text):
    # The trailing-off rhythm lives in the em dashes: the villain
    # loses the thread mid-sentence at least twice.
    if text.count("\u2014") < 2:
        raise ValueError("entry must trail off on em dashes at least twice")


def validate_voice(text):
    """Voice: tiredness felt not announced, specific villain, sting last."""
    check_tiredness_shown_not_announced(text)
    check_villainy(text)
    check_sting(text)
    check_paragraph_breaks(text)
    check_em_dash_trailing_off(text)


def validate(text):
    validate_structure(text)
    validate_shape(text)
    validate_voice(text)


def main():
    validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY + "\n")
    print("wrote /output/entry.txt: %d words, %d characters"
          % (len(ENTRY.split()), len(ENTRY) + 1))


if __name__ == "__main__":
    main()
