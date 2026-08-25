"""Strip credentials out of archived text before it is written to disk.

This is not optional hygiene. Several routine prompts carry live secrets inline
— an FTP password, a WordPress deploy key, Google Ads client secret and
developer token — because they were pasted into the instruction when the routine
was created. Archiving those verbatim into a git repository would publish them.

Every writer in this archive runs its text through this module first.

Why two passes
--------------
A single regex sweep is not enough. The same WordPress key appears in all of
these shapes inside one prompt (illustrated with a dummy value — never put a
real secret in this file):

    X-Sourov-Key: EXAMPLEKEY123              labelled pair
    'X-Sourov-Key': 'EXAMPLEKEY123'          quoted JSON-ish key
    | **Deploy Secret** | `EXAMPLEKEY123` |  markdown table cell
    ?action=status&key=EXAMPLEKEY123         URL query parameter
    EXAMPLEKEY123                            bare, on its own line

Writing a pattern for every shape is a losing game — the bare occurrence has no
syntactic marker at all. So:

  1. **Harvest** — labelled patterns find the secret *values*.
  2. **Sweep** — every harvested value is then replaced everywhere it occurs,
     literally and case-insensitively, regardless of surrounding syntax.

Harvesting is per-corpus, not per-string: a secret labelled once in one routine
is redacted from every other routine that repeats it bare. Callers therefore
harvest across all texts before redacting any of them.

Design notes:
  * Only the value is replaced. The surrounding key stays, so the page still
    reads correctly and the reader can see a secret was there.
  * The replacement encodes the kind of secret, never a hash or prefix of the
    original — a prefix leaks entropy.
  * Reports are returned rather than logged, so callers can surface how much was
    removed instead of redacting silently.
"""

import re

PLACEHOLDER = "«REDACTED:{label}»"

# Values that look secret-shaped but are not, and would wreck the pages if
# swept. Compared case-insensitively against harvested values.
ALLOWLIST = {
    "password", "secret", "changeme", "your_api_key", "xxxxxxxx",
    "redacted", "none", "null", "true", "false", "example",
}

MIN_SECRET_LEN = 8

# A truncated secret still leaks entropy, and truncated forms show up naturally:
# a grep pattern quoting the first half of a key, a log line cutting a token
# short. Once a secret is known, any prefix of it this long or longer is swept
# too. Kept at 10 rather than 8 so short hex runs and git short-SHAs are not
# caught by accident.
MIN_PREFIX_LEN = 10

# (label, pattern). Each pattern captures the value in group "secret";
# group 1 is the prefix to preserve.
HARVEST_RULES: list[tuple[str, str]] = [
    # Labelled key/value: colon or equals, optionally quoted either side.
    ("wordpress-api-key",
     r"(?i)(['\"`]?X-Sourov-Key['\"`]?\s*[:=]\s*['\"`]?)"
     r"(?P<secret>[^\s'\"`\\|]{6,})"),
    ("password",
     r"(?i)(['\"`]?\b(?:ftp[ _-]?)?pass(?:word|wd)?['\"`]?\s*[:=]\s*['\"`]?)"
     r"(?P<secret>[^\s'\"`\\|]{6,})"),
    # Account identifiers for hosting/db/ssh. The `_plausible` digit rule keeps
    # this off ordinary prose like "User: Sourov" while catching "u839…".
    ("account-username",
     r"(?i)(['\"`]?\b(?:ftp|sftp|ssh|db|database|mysql|cpanel|host)?[ _-]?"
     r"user(?:name)?['\"`]?\s*[:=]\s*['\"`]?)"
     r"(?P<secret>[^\s'\"`\\|]{8,})"),
    ("client-secret",
     r"(?i)(['\"`]?\bclient[_ -]?secret['\"`]?\s*[:=]\s*['\"`]?)"
     r"(?P<secret>[^\s'\"`\\|]{8,})"),
    ("developer-token",
     r"(?i)(['\"`]?\bdeveloper[_ -]?token['\"`]?\s*[:=]\s*['\"`]?)"
     r"(?P<secret>[^\s'\"`\\|]{8,})"),
    ("access-token",
     r"(?i)(['\"`]?\b(?:access|refresh|auth|api)[_ -]?token['\"`]?\s*[:=]\s*['\"`]?)"
     r"(?P<secret>[^\s'\"`\\|]{8,})"),
    ("api-key",
     r"(?i)(['\"`]?\bapi[_ -]?key['\"`]?\s*[:=]\s*['\"`]?)"
     r"(?P<secret>[^\s'\"`\\|]{8,})"),
    ("deploy-key",
     r"(?i)(['\"`]?\b(?:deploy[_ -]?)?(?:secret|key)['\"`]?\s*[:=]\s*['\"`]?)"
     r"(?P<secret>[^\s'\"`\\|]{8,})"),
    # URL query parameter: ?key=… or &key=…
    ("url-key-param",
     r"(?i)([?&](?:key|token|secret|api_?key|password)=)"
     r"(?P<secret>[^\s&'\"`<>|]{8,})"),
    # Markdown table cell whose row label names a credential:
    #   | **FTP Password** | `EXAMPLEKEY123` |
    ("table-cell-secret",
     r"(?i)(\|[^|\n]*\b(?:secret|key|password|token|passwd)\b[^|\n]*\|\s*`?)"
     r"(?P<secret>[^\s`|]{8,})"),
    ("bearer-token",
     r"(?i)(\bBearer\s+)(?P<secret>[A-Za-z0-9._\-]{16,})"),
    # Provider-shaped tokens, recognisable without any label.
    ("github-token", r"()(?P<secret>gh[pousr]_[A-Za-z0-9]{16,})"),
    ("openai-key", r"()(?P<secret>sk-[A-Za-z0-9_\-]{16,})"),
    ("slack-token", r"()(?P<secret>xox[abprs]-[A-Za-z0-9\-]{10,})"),
    ("aws-access-key", r"()(?P<secret>AKIA[0-9A-Z]{16})"),
    ("private-key-block",
     r"()(?P<secret>-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
    # Long bare hex — 48+ chars is a key, not prose or a git SHA (40).
    ("hex-secret",
     r"(?<![0-9a-fA-F])()(?P<secret>[0-9a-fA-F]{48,})(?![0-9a-fA-F])"),
]

COMPILED = [(label, re.compile(pat)) for label, pat in HARVEST_RULES]


def _plausible(value: str) -> bool:
    if len(value) < MIN_SECRET_LEN:
        return False
    if value.lower() in ALLOWLIST:
        return False
    if value.startswith("«REDACTED"):
        return False
    # A value that is only punctuation or only letters with no digits is more
    # likely prose than a credential — except for provider-prefixed tokens,
    # which are caught by their own patterns before reaching here.
    return any(c.isdigit() for c in value) or len(value) >= 20


def harvest(text: str) -> dict[str, str]:
    """Find credential values in one text. Returns {value: label}."""
    found: dict[str, str] = {}
    if not text:
        return found
    for label, pattern in COMPILED:
        for match in pattern.finditer(text):
            value = match.group("secret")
            if _plausible(value):
                found.setdefault(value, label)
    return found


def harvest_all(texts) -> dict[str, str]:
    """Harvest across a whole corpus so bare repeats are covered too."""
    known: dict[str, str] = {}
    for text in texts:
        for value, label in harvest(text).items():
            known.setdefault(value, label)
    return known


def redact(text: str, known: dict[str, str] | None = None):
    """Return (redacted_text, {label: count}).

    Pass `known` from `harvest_all` to also sweep bare occurrences. Without it
    this still applies the labelled patterns to the single text.
    """
    if not text:
        return text, {}
    report: dict[str, int] = {}
    known = dict(known or {})
    for value, label in harvest(text).items():
        known.setdefault(value, label)

    # Longest first, so a secret containing another as a substring is replaced
    # whole rather than leaving a mangled tail.
    for value in sorted(known, key=len, reverse=True):
        label = known[value]
        pattern = _prefix_pattern(value)
        text, count = pattern.subn(PLACEHOLDER.format(label=label), text)
        if count:
            report[label] = report.get(label, 0) + count
    return text, report


def _prefix_pattern(value: str) -> "re.Pattern[str]":
    """Match `value`, or any prefix of it at least MIN_PREFIX_LEN long.

    Built as a nest of optional single characters after the mandatory head, so
    the regex engine's greediness takes the longest prefix present:

        "abcdefghijkl" -> abcdefghij(?:k(?:l)?)?
    """
    if len(value) <= MIN_PREFIX_LEN:
        return re.compile(re.escape(value), re.IGNORECASE)
    head = re.escape(value[:MIN_PREFIX_LEN])
    tail = ""
    for char in reversed(value[MIN_PREFIX_LEN:]):
        tail = f"(?:{re.escape(char)}{tail})?"
    return re.compile(head + tail, re.IGNORECASE)


def merge(into: dict[str, int], other: dict[str, int]) -> dict[str, int]:
    for key, count in other.items():
        into[key] = into.get(key, 0) + count
    return into


def summarise(report: dict[str, int]) -> str:
    if not report:
        return "no credentials found"
    total = sum(report.values())
    detail = ", ".join(f"{k}×{v}" for k, v in sorted(report.items()))
    return f"redacted {total} credential(s): {detail}"
