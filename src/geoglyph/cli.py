"""Command line client."""

import typer

from geoglyph.uploader import write_to_hilltop


app = typer.Typer()
app.command()(write_to_hilltop)


if __name__ == "__main__":
    app()