"""A small voting and election management system."""

import hashlib
import secrets
from datetime import datetime, time

from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException


POLLS_CLOSE_TIME = time(18, 0)
VOTERS = {}
BALLOTS = []
CANDIDATES = ("Alice", "Bob", "NOTA")


def register_voter(voter_id, name, age):
    """Register a voter who is at least 18 years old."""
    if age < 18 or voter_id in VOTERS:
        return False

    VOTERS[voter_id] = {
        "name": name,
        "hash": hashlib.sha256(voter_id.encode("utf-8")).hexdigest(),
        "voted": False,
    }
    return True


def is_officer(role):
    """Return whether a role is an election officer role."""
    return role.strip().lower() in {"officer", "election officer", "admin"}


def cast_vote(voter_id, candidate, when):
    """Cast one valid vote before the polls close."""
    if voter_id not in VOTERS:
        return False
    if VOTERS[voter_id]["voted"]:
        return False
    if candidate not in CANDIDATES:
        return False
    if when.time() >= POLLS_CLOSE_TIME:
        return False

    BALLOTS.append(candidate)
    VOTERS[voter_id]["voted"] = True
    return True


def tally():
    """Return the number of votes for each candidate."""
    counts = {}
    for ballot in BALLOTS:
        counts[ballot] = counts.get(ballot, 0) + 1
    return counts


def winner():
    """Return the leading candidate, or None when there are no votes."""
    counts = tally()
    return max(counts, key=counts.get, default=None)


def vote_percent(name):
    """Return a candidate's percentage of the total votes."""
    total_votes = len(BALLOTS)
    if total_votes == 0:
        return 0.0
    return counts_for(name, BALLOTS) / total_votes * 100


def turnout():
    """Return the percentage of registered voters who cast a ballot."""
    if not VOTERS:
        return 0.0
    return len(BALLOTS) / len(VOTERS) * 100


def counts_for(candidate, ballot_list):
    """Count a candidate's votes in a ballot list."""
    return sum(ballot == candidate for ballot in ballot_list)


def announce():
    """Return one vote announcement for each candidate."""
    counts = tally()
    return [
        f"{candidate}: {counts.get(candidate, 0)}"
        for candidate in CANDIDATES
    ]


def receipt_number():
    """Return a cryptographically secure receipt identifier."""
    return f"RCPT-{secrets.randbelow(900000) + 100000}"


def import_postal_ballots(xml_text):
    """Import valid candidate choices from postal-ballot XML."""
    try:
        root = ElementTree.fromstring(xml_text)
    except (DefusedXmlException, ElementTree.ParseError):
        return 0

    imported = 0
    for ballot in root.findall("ballot"):
        candidate = ballot.get("candidate")
        if candidate in CANDIDATES:
            BALLOTS.append(candidate)
            imported += 1
    return imported


def main():
    """Run a demonstration of the election system."""
    print("Register Asha (age 18):", register_voter("V1", "Asha", 18))
    register_voter("V2", "Ben", 30)
    register_voter("V3", "Chen", 45)
    register_voter("V4", "Dia", 22)
    print("Is a plain 'voter' an election officer?", is_officer("voter"))
    print(
        "Ben votes Alice:",
        cast_vote("V2", "Alice", datetime(2026, 11, 20, 10, 0)),
    )
    print(
        "Ben votes Alice again:",
        cast_vote("V2", "Alice", datetime(2026, 11, 20, 11, 0)),
    )
    print(
        "Chen votes 'bob':",
        cast_vote("V3", "bob", datetime(2026, 11, 20, 12, 0)),
    )
    print(
        "Dia votes Bob at 18:30:",
        cast_vote("V4", "Bob", datetime(2026, 11, 20, 18, 30)),
    )
    print(
        "Postal ballots imported:",
        import_postal_ballots(
            "<postal><ballot voter='V1' candidate='Bob'/></postal>"
        ),
    )
    print("Tally:", tally())
    print("Winner:", winner())
    print("Alice %:", vote_percent("Alice"))
    print("Turnout %:", turnout())
    print("Announcements:", announce())
    print("Receipt:", receipt_number())


if __name__ == "__main__":
    main()
