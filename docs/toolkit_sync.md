# 同步本地文件夹到语雀知识库

可以通过pyuque把本地文件夹内的markdown文档同步到一个语雀知识库中，pyuque的文档就是通过这个方式同步到知识库中的。

## 命令行引用

```
pyuque sync-dir <LOCAL_FOLDER> <REPO>
```

上面的命令中，<LOCAL_FOLDER>是本地文件夹的名字，<REPO>是知识库的名字。比如

```
pyuque sync-dir docs socrateslee/pyuque
```

在本地文件夹中，可以添加一个.toc文件，用于组织文档在语雀知识库中展示的结构。.toc就是一个普通的markdown文件，通过unordered list来表示一个树形的结构，其中链接的地址就可以直接指向每个文件（比如xxxx.md，对应的地址就是xxxx）。