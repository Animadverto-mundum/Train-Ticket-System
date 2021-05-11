# Train-Ticket-System
### 1. 蓝图

对于每一个文件夹，蓝图统一定义在`__init__.py`中

例如对于Manager模块，将蓝图定义在`Manager/__init__.py`中

### 2. 导入

在同一个包内只能采用相对导入，例如蓝图`manager_bp`定义在`Manager/__init__.py`，要在`Manager/manager_auth.py`中导入该蓝图变量，就只能写作`from . import manager_bp`：

```python
# 从当前文件夹导入db变量
from . db
# 从上一级文件夹中model文件导入
from ..model import UserStaff
```

### 3. 运行

可以直接运行app.py文件
也可以在终端中运行
```shell
# powershell
cd Project
$env:FLASK_ENV=development
flask run
```
