import zipfile


def zipfile_ls(zipfile_name: str):
    if not zipfile.is_zipfile(zipfile_name):
        raise Exception('zipfile_name is not a zip file')

    zip_file = zipfile.ZipFile(zipfile_name, 'r', zipfile.ZIP_DEFLATED)

    return zip_file.namelist()


def wild_matching(str_: str, list_: list[str]) -> list:
    tables: list[str]
    tables_wild_matching = str_.split('*')
    if len(tables_wild_matching) > 1:
        # multiple tables
        tables = list(map(lambda x: x.startswith(tables_wild_matching[0]) and x, list_))
    else:
        # just one table
        if str_ in list_:
            tables = [ str_ ]
        else:
            tables = []

    return tables
