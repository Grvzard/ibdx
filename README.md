# ibdx


## Use case

- another way to backup/restore InnoDB tables besides mysqldump


## Setup

```
git clone https://github.com/Grvzard/ibdx.git [-b docker]
cd ibdx

pip3 install -r requirements.txt

cp demo.env .env
vim .env
```


## Usage

main version:
```
python3 -m ibdx backup --db test1 --tables tbl_users* [--datadir /mysql-data]
python3 -m ibdx restore -f test1.tbl_users.zip --db test1 --tables tbl_users* [--datadir /mysql-data]
```
if the mysql server is running in docker, the _--datadir_ option is needed.

more tips can be found by: ```python3 -m ibdx --help```

**Importantly:**
There is no guarantee that it will work between mysql and mariadb.
Ensure that the backup and restore sides are the same db system.


## Script Workflow

backup:
1. mysql> ``` FLUSH TABLES test1 FOR EXPORT; ``` (tables are read locked)
2. backup the .ibd (and .cfg) files.
3. mysql> ``` UNLOCK TABLES; ```

restore:
1. (optional) mysql> ``` CREATE TABLE test1; ```
2. mysql> ``` ALTER TABLE test1 DISCARD TABLESPACE; ```
3. copy the .ibd (and .cfg) files to the mysql-server's datadir
4. mysql> ``` ALTER TABLE test1 IMPORT TABLESPACE; ```


## Reference

[MariaDB Knowledge Base > InnoDB File-Per-Table Tablespaces](https://mariadb.com/kb/en/innodb-file-per-table-tablespaces/#copying-transportable-tablespaces)
