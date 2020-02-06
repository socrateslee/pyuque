# pyuque

pyuque一个[蚂蚁金服的语雀](https://www.yuque.com/)的Python版本的API Client，并且提供了一些命令行工具来辅助进行授权、组织和管理语雀上的文档。

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

## 在cli中进行OAuth认证

在下面的范例中，可以通过pyuque的cli在命令行中进行OAuth授权，获取access token:

```
python -m pyuque.cli --client_id <YOUR_CLIENT_ID>\
                     --client_secret <YOUR_CLIENT_SECRET>\
                     oauth-nonweb
```

在上面的命令中的oauth-nonweb代码非web流程，将运行命令后的网址粘贴到浏览器进行授权后，直接进入下一步就可以获得access token。
