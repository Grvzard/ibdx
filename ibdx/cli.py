from typing import Optional

import typer

from .ibd_backup import ibd_backup
from .ibd_restore import ibd_restore
from .tools import zipfile_ls
from .deps import complete_filename


cli = typer.Typer()


@cli.command()
def backup(
    dbname: str = typer.Option(
        ..., '--db', '-d'),
    target_tables: Optional[str] = typer.Option(
        '*', '--tables', '-t'),
    datadir: Optional[str] = typer.Option(''),
    filename: Optional[str] = typer.Option(
        '', '--file', '-f', autocompletion=complete_filename),
):
    try:
        ibd_backup(dbname, target_tables, datadir, filename)
    except Exception as e:
        typer.echo(f'ibdx error: {e}')


@cli.command()
def restore(
    dbname: str = typer.Option(
        ..., '--db', '-d'),
    target_tables: Optional[str] = typer.Option(
        '*', '--tables', '-t'),
    filename: str = typer.Option(
        ..., '--file', '-f', autocompletion=complete_filename),
    datadir: Optional[str] = typer.Option(''),
):
    try:
        ibd_restore(dbname, target_tables, filename, datadir)
    except Exception as e:
        typer.echo(f'ibdx error: {e}')


@cli.command()
def ls(
    zipfile_name: str = typer.Argument('', autocompletion=complete_filename)
):
    try:
        for name in zipfile_ls(zipfile_name):
            typer.echo(name)
    except Exception as e:
        typer.echo(f'ibdx error: {e}')
