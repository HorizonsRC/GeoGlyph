"""Command line client."""

import typer


def write_to_hilltop(input_file, output_path):
    print(f"write from {input_file} to {output_path}.")



app = typer.Typer()
app.command()(write_to_hilltop)


if __name__ == "__main__":
    app()