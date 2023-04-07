import zipfile
from typing import List


def zipfile_ls(zipfile_name: str):
    if not zipfile.is_zipfile(zipfile_name):
        raise Exception('zipfile_name is not a zip file')

    zip_file = zipfile.ZipFile(zipfile_name, 'r', zipfile.ZIP_DEFLATED)

    return zip_file.namelist()


def wild_matching(str_: str, list_: List[str]) -> List:
    tables = []
    tables_wild_matching = str_.split('*')
    if len(tables_wild_matching) > 1:
        # multiple tables
        tables = [t for t in list_ if t.startswith(tables_wild_matching[0])]
    else:
        # just one table
        if str_ in list_:
            tables = [ str_ ]
        else:
            tables = []

    return tables
