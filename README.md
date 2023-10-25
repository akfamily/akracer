## AKRacer

AKRacer 主要是解决 py_mini_racer 在 64 位 ARM 操作系统中的动态链接库调用问题，主要
方案就是通过 `pip install akracer` 使得在对应 `py_mini_racer` 目录中下载相应的已经
编译好的动态链接库，目前主要包括 `armlibmini_racer.dylib` 和 `armlibmini_racer.glibc.so` 这
两个动态链接库，分别对应 Apple M 系列芯片和 Ubuntu 18.04，20.04 和 22.04 及树莓派 64 位操作系统。

### 安装

```bash
pip install akracer
```

### 环境变量设置

需要在本地设置 PyPI 的环境变量

1. `HATCH_INDEX_USER` 为 `__token__`
2. `HATCH_INDEX_AUTH` 为 `pypi-xxxx`
3. 如果使用 PyCharm 则可以在 `Settings -> Tools -> Terminal -> Environment variables` 中设置
4. 具体的值在 `.pypirc` 文件中，其中 `pypi-xxxx` 为对应的 token 是从 pypi 项目的设置中生成的

### 定制化

主要修改 `akracer/py_mini_racer/py_mini_racer.py` 中的 `_get_lib_path` 函数，使得其可以
正常调用到对应的动态链接库。

### 对应操作

1. 修改版本：`akracer/py_mini_racer/__init__.py` 中的 `__version__` 更新到新版本
2. 删除版本：`akracer/dist` 删除该文件夹，以删除老版本
3. 构建版本：`hatch build`
4. 发布版本：`hatch publish`

注意：第一次上传需要在 `hatch publish -u __token__ -a pypi-xxxx` 中配置好 token，参考
https://hatch.pypa.io/latest/publish/#authentication 其中的 pypi-xxxx 为对应的 token 是从
pypi 项目的设置中生成的。

### 动态链接库

本项目目标是解决 py_mini_racer 在 64 位操作系统中的动态链接库调用问题；

1. py_mini_racer 在 x86 架构的操作系统中，可以直接使用 pip 安装，不需要额外的动态链接库；
2. 其在 ARM 架构的操作系统中，需要额外的动态链接库
3. 本次主要提供其在 Apple M 系列芯片中的动态链接库
4. 还提供 ARM 在 Ubuntu 18.04，20.04 和 22.04 中的动态链接库
5. 还提供其在树莓派 64 位操作系统中的动态链接库

对应一览表

1. armlibmini_racer.dylib 对应 Apple M 系列芯片
2. armlibmini_racer.glibc.so 对应 Ubuntu 18.04，20.04 和 22.04 及树莓派 64 位操作系统
3. 其余则由 py_mini_racer 编译安装

### 项目管理

1. [Hatch](https://github.com/pypa/hatch)
2. [Hatch 文档](https://hatch.pypa.io/)