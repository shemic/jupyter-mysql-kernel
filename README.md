# jupyter-mysql-kernel

## install:

```
pip install git+https://github.com/shemic/jupyter-mysql-kernel
```

## mysql config:
```
mkdir -p ~/.local/config/
vi ~/.local/config/mysql_config.json

{
    "user"     : "root",
    "port"     : "3306",
    "host"     : "127.0.0.1",
    "charset"  : "utf8"
    "password" : "123456"
}
```