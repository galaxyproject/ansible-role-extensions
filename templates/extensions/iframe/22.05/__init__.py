import random

pages = [
    {
        'src': 'https://galaxyproject.org/bare/eu/news/',
        'height': 1000,
        'title': 'Galactic News',
        'weight': 0.5,
    },
    {
        'src': 'https://docs.google.com/forms/d/e/1FAIpQLScxvybBFjgCqHPbQC8Qrallex4JampXGCVK-UoBqTNx54BfrQ/viewform',
        'height': 1000,
        'title': 'Usegalaxy feedback form',
        'weight': 0.2,
    },
    # {
        # # TODO: need to self-host
        # 'src': 'http://teacheng.illinois.edu/SequenceAlignment/',
        # 'height': 1000,
        # 'title': 'Sequence Alignment: The Game!',
        # 'weight': 0.0,
    # },
    {
        'src': 'https://stats.galaxyproject.eu/d/000000004/galaxy?orgId=1&refresh=1m&viewPanel=38&from=now-3h&to=now',
        'height': 1000,
        'title': 'Galaxy Queue (past 3 hours)',
        'weight': 0.5,
    },
    {
        'src': 'https://galaxyproject.org/bare/eu/events/',
        'height': 1000,
        'title': 'Upcoming Events',
        'weight': 0.5,
    },
    {
        'src': 'https://usegalaxy.eu/gapars-experiment/',
        'height': 1000,
        'title': 'Citizen Science Experiment!',
        'weight': 0.5,
    }
]

weighted_pages = [(page, page['weight']) for page in pages]

def weighted_choice(choices):
    """Weighted random distribution. Given a list like [('a', 1), ('b', 2)]
    will return a 33% of the time and b 66% of the time."""
    # http://stackoverflow.com/a/3679747
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w


def main(trans, webhook, params):
    return weighted_choice(weighted_pages)
