"""Command line client."""

import typer

from shadoof.uploader import write_to_hilltop
from typing import Annotated

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def main(
    input_file: Annotated[str, typer.Argument(help="Path of file to be uploaded")],
    destination: Annotated[
        str, typer.Argument(help="Path of hts file to receive data")
    ],
    raw_xml: Annotated[
        bool,
        typer.Option("--raw_xml", "-r", help="Whether to skip pre-xml parsing"),
    ] = False,
):
    write_to_hilltop(input_file, destination, raw_xml=raw_xml)


if __name__ == "__main__":
    app()
