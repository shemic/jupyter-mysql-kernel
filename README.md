# MySQL kernel for Jupyter/IPython

![jupyter-mysql-kernel](https://github.com/shemic/jupyter-mysql-kernel/blob/master/res/jupyter.png)


## install:

```
pip install git+https://github.com/bertrandpsi/jupyter-mysql-kernel
```

## mysql config:
```
mkdir -p ~/.local/config/
vi ~/.local/config/mysql_config.json

{
    "user"     : "root",
    "port"     : "3306",
    "host"     : "127.0.0.1",
    "charset"  : "utf8",
    "password" : "",
    "display"  : "prettytable"
}
```