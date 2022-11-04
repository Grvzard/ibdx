import zipfile
from pathlib import Path

from .mysql_db_quick import MysqlConn
from .configs import DB_CONFIG


def ibd_backup(
    db_name: str,
    tar_tables: str = '',
) -> None:
    db = MysqlConn(db_name, DB_CONFIG)

    datadir = db.query('show variables like \'datadir\';').fetchone()[1]
    db_path = Path(datadir) / db_name
    assert db_path.is_dir()

    zipfile_name = f'{db_name}_{tar_tables}.zip'
    zip_file = zipfile.ZipFile(zipfile_name, 'w', zipfile.ZIP_DEFLATED)

    for table in db.get_tables():
        if table.startswith(tar_tables):
            print(table)
            db.query(f"flush tables `{table}` for export;")

            _sql_create = db.query(f'show create table `{table}`;').fetchall()[0][1]
            zip_file.writestr(f'{table}.sql', _sql_create)
            zip_file.write(db_path / f'{table}.ibd', f'{table}.ibd')
            zip_file.write(db_path / f'{table}.cfg', f'{table}.cfg')

            db.query('unlock tables;')
