from virgil.config import Config
from virgil.core.models import get_flat_requirements, get_packages
from virgil.core.printer import Printer


def list_command(_):
    printer = Printer()

    printer.info("Installed packages\n")
    package_list = get_packages()
    for package in package_list:
        if package.name not in Config.ignore_list:
            printer.package(package.id)

    printer.info("\nRequirements\n")
    for requirement in get_flat_requirements(packages=package_list):
        if requirement.name not in Config.ignore_list:
            printer.requirement(requirement.id)
