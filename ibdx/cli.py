
import typer

from .ibd_backup import ibd_backup
from .ibd_restore import ibd_restore
from .tools import zipfile_ls


cli = typer.Typer()


@cli.command()
def backup(db_name: str, tar_tables: str):
    try:
        ibd_backup(db_name, tar_tables)
    except Exception as e:
        typer.echo(e)


@cli.command()
def restore(
    db_name: str,
    tar_tables: str = typer.Argument(''),
    need_tables: str = typer.Option('')
):
    try:
        ibd_restore(db_name, tar_tables, need_tables)
    except Exception as e:
        typer.echo(e)


@cli.command()
def ls(zipfile_name: str):
    try:
        for name in zipfile_ls(zipfile_name):
            typer.echo(name)
    except Exception as e:
        typer.echo(e)
