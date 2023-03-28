import zipfile
from pathlib import Path
from typing import Optional

from . import __version__
from .mysql_db_quick import MysqlConn
from .configs import DB_CONFIG
from .tools import wild_matching


def ibd_backup(
    dbname: str,
    target_tables: str,
    datadir: Optional[str],
    filename: Optional[str],
) -> None:
    db = MysqlConn(dbname, DB_CONFIG)

    if not datadir:
        datadir = db.query('show variables like \'datadir\';').fetchone()[1]
    db_path = Path(datadir) / dbname
    assert db_path.is_dir()

    if not filename:
        filename = dbname + '.' + target_tables.split('*')[0] + '.zip'

    if not Path(filename).exists():
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f'.ibdx.v{__version__}', f'{__version__}')

    tables = wild_matching(target_tables, db.get_tables())

    with zipfile.ZipFile(filename, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for table in tables:
            print(table)
            db.query(f"flush tables `{table}` for export;")

            _sql_create = db.query(f'show create table `{table}`;').fetchall()[0][1]
            zip_file.writestr(f'{table}.sql', _sql_create)
            zip_file.write(db_path / f'{table}.ibd', f'{table}.ibd')
            zip_file.write(db_path / f'{table}.cfg', f'{table}.cfg')

            db.query('unlock tables;')
