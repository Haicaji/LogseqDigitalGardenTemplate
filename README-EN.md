# LogseqDigitalGardenTemplate

[**中文简体**](./README.md) | [**English**](./README-EN.md)

Make it easier for you to publish your Logseq graph as your own digital garden.

<!-- PROJECT SHIELDS -->

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

## Notice

Due to file size limitations on Github, the following files have not been uploaded, but you can download the complete package in [releases](https://github.com/Haicaji/LogseqDigitalGardenTemplate/releases).

```
/publish-spa/
/OtherDependencies/
/logseq/
/Node/
```

## Table of Contents

* [Brief Introduction](#brief-introduction)
* [Getting Started](#getting-started)
    * [Requirements](#requirements)
    * [Deployment Process](#deployment-process)
        * [Install babashka](#install-babashka)
        * [Install Clojure](#install-clojure)
        * [Generate Static HTML Page Template](#generate-static-html-page-template)
        * [Install publish-spa](#install-publish-spa)
        * [Initialize the /GraphsFile/ Directory](#initialize-the-graphsfile-directory)
        * [Initialize the /PublishWeb/ Directory](#initialize-the-publishweb-directory)
        * [Let's Test with Something](#lets-test-with-something)
* [Change Page Styles](#change-page-styles)
* [File Directory Description](#file-directory-description)
* [Other Projects Used in This Project](#other-projects-used-in-this-project)

### Brief Introduction

1.  Integrate with Logseq's automatic commit function, implementing the Git hook to execute automation processes (the content of the process is as follows):
2.  Convert image formats (except gif) to `avif` to save space, without changing the file name.
3.  Generate a webpage of the Logseq graph using `Logseq-Publish-spa`.
4.  Upload the Logseq graph webpage to Github and publish it.
5.  Automatically delete Github deployments and workflow records.

### Getting Started

#### Requirements

1. Currently, only usable on Windows computers.
2. Ensure that Git is usable on your computer.
3. Logseq has been installed.
4. JDK17 or above has been installed.

#### Deployment Process

##### Install babashka

Download and add `babashka` to your environment variables.

You can find a version of `babashka` in the `OtherDependencies` folder of this project, or download the latest version from [babashka's releases](https://github.com/babashka/babashka/releases).

##### Install Clojure

You can find the Clojure MSI file in the `OtherDependencies` folder of this project for installation, or download the latest version from [Clojure's releases](https://github.com/casselc/clj-msi/releases).

##### Generate Static HTML Page Template

In the project directory, first clone Logseq.

```
git clone https://github.com/logseq/logseq
```

Then enter the `logseq` directory, install dependencies, and generate the template. (Why don't I install and then package? Because this step will increase the entire project volume by nearly 2G, I think it's better to install it yourself. Other dependencies are already installed).

```
cd logseq
$env:Path += ";$((Convert-Path -Path '../Node/'))" # Temporarily add ../Node/ to environment variables
yarn install --frozen-lockfile # Note the network connection here; it might disconnect if the network is not good and need to re-execute
yarn gulp:build
clojure -M:cljs release publishing
```

If the following error occurs, please modify the PowerShell execution script permissions.

```
../Node/yarn : File ......\LogseqDigitalGardenTemplate\Node\yarn.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
Location Line:1 Char: 1
+ ../Node/yarn install --frozen-lockfile
+ ~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) []，PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

Modify permissions command to allow the current user to execute local scripts.

```
Set-ExecutionPolicy Remotesigned -Scope CurrentUser
```

##### Install publish-spa

In `/publish-spa/`, execute:

```
$env:Path += ";$((Convert-Path -Path '../Node/'))" # Temporarily add ../Node/ to environment variables
npm i -g
```

##### Initialize the /GraphsFile/ Directory

Use Logseq to initialize a graph in the `/GraphsFile/` directory. Generally, if there are no images in the graph, there will be no `assets` file in this directory. However, for debugging purposes, you can create one yourself first.

Then, initialize a Git file in this directory.

Execute the following commands:

```
git init
git add -A
git commit -m "Init"
```

Then, put the two scripts in the `/GitHookBak/` directory into the `/GraphsFile/.git/hook/` directory.

##### Initialize the /PublishWeb/ Directory

In this directory, two workflows have been written. `delete-workflow-runs.yml` is used to automatically delete Github deployments and workflow records, while `static.yml` is used to generate a Github Page.

But remember to change the repository name in `/.github/delete-workflow-runs.yml` to your own.

```yaml
jobs:
  del_runs:
    steps:
        with:
          repository: 'Here write your own github.io repository address'
```

Create an initial Git in this directory.

```
git init
git add -A
git commit -m "Init"
```

Add a Github remote repository.

```
git branch -M main
git remote add origin <Your Github repository address>
```

> Also, if you are using Git for the first time, remember to configure your Git username and email.
> `git config --global user.email <Your email>`
> `git config --global user.name <Your Name>`

##### Let's Test with Something

Enable Logseq's automatic commit function (toggling it on/off will execute it once).

> Before generating the Logseq webpage, please set which pages to publish in Logseq, or publish all of them.

### Change Page Styles

You can go to [logseq/publish-spa](https://github.com/logseq/publish-spa) to view detailed commands, and then change the `../Node/logseq-publish-spa ../PublishWeb` command in the `/GraphsFile/.git/hook/post-commit` file.

### File Directory Description

```
filetree
├── /GitHookBak/        # Backup of git hook scripts
│  ├── post-commit
│  └── pre-commit
├── /GraphsFile/        # Stores Logseq graphs
│  ├── /.git/
│  └── ...              # Omitted Logseq graph directory structure
├── /ImageToAVIF/       # Scripts for converting images to avif format
├── /Node/              # Nodejs with pre-installed dependencies
├── /OtherDependencies/ # Some dependencies to be installed, perhaps you can download the latest version
├── /publish-spa/       # publish-spa project folder
├── /PublishWeb/        # Generated Logseq graph webpages
│  ├── /.git/
│  └── ...              # Omitted Logseq graph webpage directory structure
├── creatWeb.bat        # Manually generate webpages, but won't upload
├── ImageToAVIF.bat     # Manually convert all images in the graph to the specified format
├── PublishWeb.bat      # Manually perform a commit operation on /GraphsFile/, in order to automatically execute hook scripts, realizing manual generation of web
├── README.md
├── TestWebByPython.bat # Use Python to start an HTTP service for testing webpages
└── upload.log          # Git hook logs
```

### Other Projects Used in This Project

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