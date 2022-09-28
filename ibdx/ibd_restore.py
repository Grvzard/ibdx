import zipfile
from pathlib import Path
from contextlib import suppress

from .mysql_db_quick import MysqlConn
from .configs import DB_CONFIG


def ibd_restore(
    data_path: str,
    db_name: str,
    tar_tables: str,
    need_tables: str = ''
) -> None:
    db_path = Path(data_path) / db_name
    if not db_path.is_dir():
        raise Exception('db_path is not dir')
    if not need_tables:
        need_tables = tar_tables

    db = MysqlConn(db_name, DB_CONFIG)

    zipfile_name = f'{db_name}_{tar_tables}.zip'
    zip_file = zipfile.ZipFile(zipfile_name, 'r', zipfile.ZIP_DEFLATED)

    file_list = [file for file in zip_file.namelist() if file.endswith('.ibd')]
    for file in file_list:
        table = file.split('.')[0]
        if table.startswith(need_tables):
            print(table)
            with suppress(Exception):
                _sql_create = zip_file.read(f'{table}.sql')
                db.query(_sql_create)
            db.query(f'alter table `{table}` discard tablespace')
            zip_file.extract(f'{table}.ibd', db_path)
            with suppress(Exception):
                zip_file.extract(f'{table}.cfg', db_path)
            db.query(f'alter table `{table}` import tablespace')
