# pyuque

pyuque一个语雀的Python版本的API Client，并且提供了一些命令行工具来辅助进行授权、组织和管理语雀上的文档。

## 安装

通过pip安装和升级pyuque

```
pip install -U pyuque
```

## 调用语雀API

下面是一个简单的范例，通过pyuque调用语雀API来获取一篇语雀官方开发文档的内容

```
from pyuque.client import Yuque

# 建立一个语雀API的client
client = Yuque("<YOUR_ACCESS_TOKEN>")

# 调用API，获取文档内容
client.doc.get("yuque/developer", "api")
```
