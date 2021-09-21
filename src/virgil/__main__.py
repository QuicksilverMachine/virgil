import click

from virgil.core import distributions


@click.command()
def cli():
    distributions.get_distributions()


if __name__ == "__main__":
    cli()
