# ibdx


## Use case

- another way to backup/restore InnoDB tables besides mysqldump


## Workflow

backup in 3 steps:
1. mysql> ``` FLUSH TABLES test1 FOR EXPORT; (tables are read locked) ```
2. backup the .ibd (and .cfg) files.
3. mysql> ``` UNLOCK TABLES; ```

restore in 4 steps:
1. mysql> ``` CREATE TABLE test1 (...); ```
2. mysql> ``` ALTER TABLE test1 DISCARD TABLESPACE; ```
3. copy the .ibd (and .cfg) files to the mysql-server's datadir
4. mysql> ``` ALTER TABLE test1 IMPORT TABLESPACE; ```


## Reference

[MariaDB Knowledge Base > InnoDB File-Per-Table Tablespaces](https://mariadb.com/kb/en/innodb-file-per-table-tablespaces/#copying-transportable-tablespaces)
