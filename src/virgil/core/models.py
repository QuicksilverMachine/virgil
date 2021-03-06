import subprocess

from importlib.metadata import (
    Distribution,
    MetadataPathFinder,
    PackageNotFoundError,
)
from typing import List, Optional

from virgil.config import Config


class Package:
    def __init__(self, distribution: Distribution) -> None:
        self.name: str = distribution.metadata.get("Name")
        self.version: str = distribution.metadata.get("Version")
        self.metadata = distribution.metadata
        self._requires = distribution.requires

    def __repr__(self) -> str:
        return f"Package: ({self.name}, {self.version})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Package) and self.id == other.id

    @property
    def id(self) -> str:
        return f"{self.name}=={self.version}"

    @property
    def requirements(self) -> List["Requirement"]:
        return [Requirement.from_string(r) for r in self._requires or []]


class Requirement:
    def __init__(self, name: str, version: str) -> None:
        self.name: str = name
        self.version: str = version

    def __repr__(self) -> str:
        return f"Requirement: ({self.name}, {self.version})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Requirement) and self.id == other.id

    @property
    def id(self) -> str:
        return f"{self.name}{self.version}" if self.version != Config.any_version else self.name

    @property
    def package(self) -> Optional[Package]:
        try:
            distribution = Distribution.from_name(name=self.name)
            return Package(distribution=distribution)
        except PackageNotFoundError:
            return None

    @staticmethod
    def from_string(requirement_string: str) -> "Requirement":
        requirements = [r.strip() for r in requirement_string.split(";")]
        name_and_version = requirements[0].split()
        name = name_and_version[0]
        version = (
            name_and_version[1].strip("(").strip(")")
            if len(name_and_version) > 1
            else Config.any_version
        )
        return Requirement(name=name, version=version)


def get_packages() -> List[Package]:
    site_packages_paths = get_site_packages_path()

    packages = [
        Package(distribution=distribution)
        for distribution in MetadataPathFinder.find_distributions(
            context=(
                MetadataPathFinder.Context(path=site_packages_paths)
                if site_packages_paths
                else MetadataPathFinder.Context()
            )
        )
    ]
    return sorted([package for package in packages if package.name], key=lambda p: p.id.lower())


def get_flat_requirements(packages: List[Package]) -> List[Requirement]:
    result: List[Requirement] = []
    for package in packages:
        for requirement in package.requirements:
            # Ignore already added requirements
            if requirement.id not in [r.id for r in result]:
                result.append(requirement)
    return sorted(result, key=lambda r: r.id.lower())


def get_site_packages_path() -> list[str]:
    """Get site packages path by using user's python binary,
    this will allow virgil to check dependencies of user's
    environment when it's installed globally
    """
    return [
        subprocess.check_output(["python3", "-c", "import site;print(site.getsitepackages()[0])"])
        .decode()
        .strip()
    ]
