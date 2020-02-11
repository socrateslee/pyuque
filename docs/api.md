# 语雀API的调用

[语雀的官方API文档](https://www.yuque.com/yuque/developer)提供了一些针对语雀的团队，知识库以及文档等进行管理的相关接口，pyuque针对大致按照语雀的分类对这些接口进行了封装。我们可以先看一个例子：

```
from pyuque.client import Yuque

# 声明一个SDK客户端实例
client = Yuque("<YOUR_ACCESS_TOKEN>")

# 发起文档api请求
client.doc.get(...)

# 发起知识库api请求
client.repo.get(...)
```

如上面的代码范例所示，```client```后面跟的```doc```或者```repo```等，是pyuque的client根据语雀的api的分类划分的名字空间。 

## 名字空间
pyuque根据语雀的API的操作对象划分了Yuque这个客户端类的名字空间，这个名字空间的划分和语雀API的网址的前缀也更相似。具体的名字空间和方法如下:

- __user__: 封装用户相关的api
    - __get__ 获取单个用户信息/获取认证的用户的个人信息(无需传参)
    - __list_groups__ 获取某个用户的加入的组织列表
    - __list_repos__ 获取某个用户的知识库列表
    - __create_repo__ 为用户创建知识库
- __group__: 封装组织相关的api
    - __list__ 获取公开组织列表
    - __create__ 创建 Group
    - __get__ 获取单个组织的详细信息
    - __update__ 更新单个组织的详细信息
    - __delete__ 删除组织
    - __users_list__ 获取组织成员信息
    - __users_add__ 增加或更新组织成员
    - __users_delete__ 删除组织成员
    - __list_repos__ 获取某个团队的知识库列表
    - __create_repo__ 为团队创建知识库
- __repo__: 封装和知识库相关的api
    - __get__ 获取知识库详情
    - __update__ 更新知识库信息
    - __delete__ 删除知识库
    - __toc__ 获取一个知识库的目录结构
    - __list_docs__ 获取一个仓库的文档列表
- __doc__: 封装和文档相关的api
    - __get__ 获取单篇文档的详细信息
    - __create__ 创建文档
    - __update__ 更新文档
    - __delete__ 删除文档
- __search__: 封装和搜索相关的api
    - __search__ 搜索

## 一些注意事项

- 一个通过api创建的普通文档，如果被人工编辑过，则不能再通过api进行更新(update)，如果还要进行api的更新，则需要删除在重建。
- 对于知识库的名字空间，比如test/test，在pyuque中会在两端进行trim，比如/test/test/，test/test/，/test/test等，都是一致的。
