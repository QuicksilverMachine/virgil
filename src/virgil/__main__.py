import click

from virgil.core import distributions


@click.command()
def cli():
    distribution_list = distributions.get_distributions()
    for distribution in distribution_list:
        print(distribution)


if __name__ == "__main__":
    cli()
