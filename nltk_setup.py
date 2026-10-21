"""Locate NLTK tokenizer and WordNet data, downloading them when missing.

The 2017 tree committed a full ``nltk_data`` checkout (many languages, about
94MB). That corpus is not source. This module downloads only the English
packages the sentence engine uses.
"""

import os

PACKAGES = (
    ("punkt_tab", "tokenizers/punkt_tab"),
    ("wordnet", "corpora/wordnet"),
    ("omw-1.4", "corpora/omw-1.4"),
)

DOWNLOAD_HINT = "python -m nltk.downloader punkt_tab wordnet omw-1.4"


def _can_write(path):
    try:
        os.makedirs(path, exist_ok=True)
        probe = os.path.join(path, ".write-test")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("")
        os.remove(probe)
        return True
    except OSError:
        return False


def data_directory():
    configured = os.environ.get("NLTK_DATA")
    if configured:
        return configured
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nltk_data")
    if _can_write(os.path.dirname(local) or "."):
        return local
    return "/tmp/nltk_data"


def ensure_nltk_data():
    """Make punkt and WordNet importable. Raise LookupError with a hint on failure."""
    import nltk

    target = data_directory()
    os.makedirs(target, exist_ok=True)
    if target not in nltk.data.path:
        nltk.data.path.insert(0, target)
    # The old checkout lived in ./nltk_data. Keep that path on the search list
    # for anyone who still has a local copy.
    legacy = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nltk_data")
    if legacy not in nltk.data.path:
        nltk.data.path.append(legacy)

    missing = []
    for package, resource in PACKAGES:
        try:
            nltk.data.find(resource)
        except LookupError:
            missing.append(package)
    if not missing:
        return target
    for package in missing:
        downloaded = nltk.download(package, download_dir=target, quiet=True)
        if not downloaded:
            raise LookupError(
                "Could not download NLTK package %s. Run: %s" % (package, DOWNLOAD_HINT)
            )
    return target
