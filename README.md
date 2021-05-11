This is a class assignment from SWJTU

### 1. 蓝图

对于每一个文件夹，蓝图统一定义在`__init__.py`中

例如对于Manager模块，将蓝图定义在`Manager/__init__.py`中

### 2. 引用

目前只能采用相对引用，例如：

```python
# 从当前文件夹导入db变量
from . db
# 从上一级文件夹中model文件导入
from ..model import UserStaff
```

### 3. 运行

注意不能直接运行app.py文件

```shell
cd Project
flask run
```

