import zipfile
from pathlib import Path
from contextlib import suppress

from .mysql_db_quick import MysqlConn
from .configs import DB_CONFIG
from .tools import wild_matching


def ibd_restore(
    dbname: str,
    target_tables: str,
    filename: str,
    datadir: str,
) -> None:
    db = MysqlConn(dbname, DB_CONFIG)

    assert zipfile.is_zipfile(filename)

    if not datadir:
        datadir = db.query('show variables like \'datadir\';').fetchone()[1]
    db_path = Path(datadir) / dbname
    assert db_path.is_dir()


    with zipfile.ZipFile(filename, 'r', zipfile.ZIP_DEFLATED) as zip_file:
        _target_files = wild_matching(f'{target_tables}.ibd', zip_file.namelist())
        ibd_files = map(
            lambda x: x.endswith('.ibd') and x,
            _target_files
        )
        for ibd_file in ibd_files:
            table = ibd_file.split('.')[0]
            print(table)

            with suppress(Exception):
                _sql_create = zip_file.read(f'{table}.sql')
                db.query(_sql_create)

            try:
                db.query(f'alter table `{table}` discard tablespace')

                zip_file.extract(f'{table}.ibd', db_path)
                with suppress(Exception):
                    zip_file.extract(f'{table}.cfg', db_path)

                db.query(f'alter table `{table}` import tablespace')

            except Exception as e:
                with suppress(Exception):
                    (db_path / f'{table}.ibd').unlink()
                with suppress(Exception):
                    (db_path / f'{table}.cfg').unlink(missing_ok=True)
                db.query(f'drop table if exists `{table}`;')

                raise Exception('failed when importing tablespace:\n' + str(e))
