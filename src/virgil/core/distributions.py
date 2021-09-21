from importlib.metadata import MetadataPathFinder

IGNORE = ["wheel", "setuptools", "pip"]


class Distribution:
    def __init__(self, d):
        self.name = d.metadata.get("Name")
        self.version = d.metadata.get("Version")
        self.metadata = d.metadata
        self.requires = d.requires


def get_distributions():
    distributions = [Distribution(d) for d in MetadataPathFinder.find_distributions()]
    result = []
    for distribution in distributions:
        if distribution.name not in IGNORE:
            result.append(f"{distribution.name}=={distribution.version} ({distribution.requires})")
    return result
