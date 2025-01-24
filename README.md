# LogseqDigitalGardenTemplate

使你更轻松的发布Logseq图谱, 作为自己的数字花园

<!-- PROJECT SHIELDS -->

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
 
## 目录



### 功能简述

1. 与 Logseq 的自动 Commit 联动, 实现调用git hook, 执行自动化流程(流程内容为以下几点)
2. 将图片格式(除gif)转为 `avif` 以节省空间, 但命名并未改变
3. 通过 `Logseq-Publish-spa` 生成 Logseq 图谱的网页
4. 将 Logseq 图谱网页上传 Github, 并通过发布

### 上手指南

#### 使用要求

1. 目前仅能Windows电脑上使用
2. 确保你的电脑可以使用 Git
3. 已经安装好了 Logseq
4. 已经安装JDK17或以上版本

#### 部署流程

##### babashka安装

下载并把 `babashka` 添加进环境变量

你可以在该项目的`OtherDependencies`文件夹中, 找到某个版本的`babashka`, 或者去 [babashka 的 releases](https://github.com/babashka/babashka/releases) 下载最新版本

##### Clojure安装

你可以在该项目的`OtherDependencies`文件夹中, 找到 Clojure 的 msi 文件进行安装, 或者去 [Clojure 的 releases](https://github.com/casselc/clj-msi/releases) 下载最新版本

##### 生成静态html页面模板

在项目目录下, 先克隆 Logseq

```
git clone https://github.com/logseq/logseq
```

然后进入 logseq 目录, 安装依赖并生成模板(为什么我不安装好后再打包? 因为这一步会使整个项目体积增加快 2G, 我想还是自己安装比较好, 其他的依赖都安装好了)

```
$env:Path += ";$((Convert-Path -Path '../Node/'))" # 将 ../Node/ 临时添加进环境变量
cd logseq
yarn install --frozen-lockfile # 这里注意网络连接, 网络不好的情况下, 会断连, 需要重新执行
yarn gulp:build
clojure -M:cljs release publishing
```

如果出现以下报错, 请修改 PowerShell 执行脚本的权限

```
../Node/yarn : 无法加载文件 ......\LogseqDigitalGardenTemplate\Node\yarn.ps1，因为在此系统上禁止运行脚
本。有关详细信息，请参阅 https:/go.microsoft.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。
所在位置 行:1 字符: 1
+ ../Node/yarn install --frozen-lockfile
+ ~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) []，PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

修改权限命令, 使当前用户可以执行本地脚本

```
Set-ExecutionPolicy Remotesigned -Scope CurrentUser
```

##### 初始化 /GraphsFile/ 目录

使用Logseq在 /GraphsFile/ 目录初始化一个图谱, 一般情况下, 如果图谱内没有图片, 是该目录下是不会有 `assets` 文件的, 但是为了后续调试, 你可以先自己创建一个

然后在该目录在初始化 git 文件

执行如下命令

```
git init
git add -A
git commit -m "Init"
```

然后把 /GitHookBak/ 目录下的两个脚本, 放到 /GraphsFile/.git/hook/ 目录下

##### 初始化 /PublishWeb/ 目录

> 在生成 Logseq 网页前, 请先在 Logseq 中设置要发布哪些页面, 或者全部发布

在这个目录下, 已经写入了两个工作流, 用于自动删除 Github 的 deployments 和 workflow 记录

但是记得把 /.github/delete-workflow-runs.yml 中的仓库名称写为你自己的
```
jobs:
  del_runs:
    steps:
        with:
          repository: '这里写为你自己的github.io仓库地址'
```

在这个目录在创建初始化 git

```
git init
git add -A
git commit -m "Init"
```

添加 Github 远程仓库

```
git branch -M main
git remote add origin <你的Github仓库的地址>
```

> 对了, 如果你第一次使用 git, 记得在配置 git 的用户名和邮箱
> git config --global user.email <Your email>
> git config --global user.name <Your Name>

##### 随便写点东西测试一下吧

开启 Logseq 的自动 Commit 功能(开关一下, 就会执行一次)

### 文件目录说明

```
filetree 
├── /GitHookBak/        # git hook 脚本的备份
│  ├── post-commit
│  └── pre-commit
├── /GraphsFile/        # 存放 Logseq 图谱
│  ├── /.git/
│  └── ...              # 省略 Logseq 图谱的目录结构
├── /ImageToAVIF/       # 图片转 avif 格式的脚本
├── /Node/              # 已经安装好依赖的 Nodejs
├── /OtherDependencies/ # 一些代安装的依赖, 或许你可以去下载最新版
├── /publish-spa/       # publish-spa 的项目文件夹
├── /PublishWeb/        # 生成的 Logseq 图谱网页
│  ├── /.git/
│  └── ...              # 省略 Logseq 图谱网页的目录结构
├── creatWeb.bat        # 手动生成网页, 但是不会上传
├── ImageToAVIF.bat     # 手动将图谱所有图片进行格式转换
├── PublishWeb.bat      # 手动对 /GraphsFile/ 执行 Commit 操作, 以达到自动执行 hook 脚本, 实现手动生成网
├── README.md
├── TestWebByPython.bat # 使用 Python 启动 Http 服务, 用于测试网页
└── upload.log          # git hook 的日志
```

### 该项目使用到的其他项目

- [logseq/logseq](https://github.com/logseq/logseq)
- [logseq/publish-spa](https://github.com/logseq/publish-spa)
- [babashka/babashka](https://github.com/babashka/babashka)
- [casselc/clj-msi](https://github.com/casselc/clj-msi)
- [shaojintian/Best_README_template](https://github.com/shaojintian/Best_README_template)

<!-- links -->
[forks-shield]: https://img.shields.io/github/forks/Haicaji/LogseqDigitalGardenTemplate.svg?style=flat-square
[forks-url]: https://github.com/Haicaji/LogseqDigitalGardenTemplate/network/members
[stars-shield]: https://img.shields.io/github/stars/Haicaji/LogseqDigitalGardenTemplate.svg?style=flat-square
[stars-url]: https://github.com/Haicaji/LogseqDigitalGardenTemplate/stargazers
[issues-shield]: https://img.shields.io/github/issues/Haicaji/LogseqDigitalGardenTemplate.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/Haicaji/LogseqDigitalGardenTemplate.svg
