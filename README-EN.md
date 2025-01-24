# LogseqDigitalGardenTemplate

[**中文简体**](./README.md) | [**English**](./README-EN.md)

Effortlessly publish your Logseq graph as your own digital garden.

<!-- PROJECT SHIELDS -->

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

## Notice

Due to GitHub file size limitations, the following files are not included in this repository. You can download the complete package from [releases](https://github.com/Haicaji/LogseqDigitalGardenTemplate/releases).

```
/publish-spa/
/OtherDependencies/
/logseq/
/Node/
```

## Table of Contents

*   [Overview](#overview)
*   [Getting Started](#getting-started)
    *   [Requirements](#requirements)
    *   [Deployment Process](#deployment-process)
        *   [Install babashka](#install-babashka)
        *   [Install Clojure](#install-clojure)
        *   [Generate Static HTML Page Template](#generate-static-html-page-template)
        *   [Initialize the /GraphsFile/ Directory](#initialize-the-graphsfile-directory)
        *   [Initialize the /PublishWeb/ Directory](#initialize-the-publishweb-directory)
        *   [Test it out by writing something](#test-it-out-by-writing-something)
*   [File Directory Description](#file-directory-description)
*   [Projects Used by This Project](#projects-used-by-this-project)

### Overview

1.  Integrates with Logseq's automatic commit feature to trigger Git hooks and execute an automated process (detailed below).
2.  Converts image formats (except GIFs) to `avif` to save space, while preserving filenames.
3.  Generates a web page from your Logseq graph using `Logseq-Publish-spa`.
4.  Uploads the generated Logseq graph webpage to GitHub and publishes it.

### Getting Started

#### Requirements

1.  Currently only works on Windows.
2.  Ensure Git is installed and functional on your computer.
3.  Logseq is already installed.
4.  JDK 17 or a later version is installed.

#### Deployment Process

##### Install babashka

Download `babashka` and add it to your system's environment variables.

You can find a version of `babashka` in the `OtherDependencies` folder of this project, or download the latest version from [babashka releases](https://github.com/babashka/babashka/releases).

##### Install Clojure

You can find the Clojure MSI installer in the `OtherDependencies` folder of this project, or download the latest version from [Clojure releases](https://github.com/casselc/clj-msi/releases).

##### Generate Static HTML Page Template

In the project's root directory, first clone Logseq:

```
git clone https://github.com/logseq/logseq
```

Then, navigate into the `logseq` directory, install dependencies, and generate the template (Why not bundle this? Because it increases the project size by about 2GB. I prefer to install it manually. All other dependencies are already installed).

```
$env:Path += ";$((Convert-Path -Path '../Node/'))" # Temporarily add ../Node/ to the environment variable
cd logseq
yarn install --frozen-lockfile # Note the network connection, it might disconnect and you might need to redo this step.
yarn gulp:build
clojure -M:cljs release publishing
```

If you encounter the following error, you may need to adjust the PowerShell execution policy.

```
../Node/yarn : File ......\LogseqDigitalGardenTemplate\Node\yarn.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ ../Node/yarn install --frozen-lockfile
+ ~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [],PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

Modify the execution policy to allow the current user to run local scripts:

```
Set-ExecutionPolicy Remotesigned -Scope CurrentUser
```

##### Initialize the /GraphsFile/ Directory

Initialize a Logseq graph in the `/GraphsFile/` directory using Logseq. Generally, if there are no images, the `assets` directory won't exist. For debugging purposes, you can create one manually.

Then, initialize a Git repository in the same directory:

```
git init
git add -A
git commit -m "Init"
```

Copy the two scripts from the `/GitHookBak/` directory into the `/GraphsFile/.git/hook/` directory.

##### Initialize the /PublishWeb/ Directory

> Before generating the Logseq webpage, ensure you have specified which pages to publish in Logseq, or you can choose to publish all pages.

This directory contains two workflows designed to automatically delete GitHub deployments and workflow run records.

Remember to replace the repository name in `/.github/delete-workflow-runs.yml` with your own.

```yaml
jobs:
  del_runs:
    steps:
        with:
          repository: 'your-github-io-repository-address-here'
```

Create an initial Git repository in this directory:

```
git init
git add -A
git commit -m "Init"
```

Add your GitHub remote repository:

```
git branch -M main
git remote add origin <your-github-repository-address>
```

> By the way, if you are using Git for the first time, remember to configure your Git username and email:
> git config --global user.email <Your email>
> git config --global user.name <Your Name>

##### Test it out by writing something

Enable Logseq's automatic commit feature (toggle it on and off, it will trigger once).

### File Directory Description

```
filetree
├── /GitHookBak/        # Backup of Git hook scripts
│   ├── post-commit
│   └── pre-commit
├── /GraphsFile/        # Stores Logseq graph data
│   ├── /.git/
│   └── ...              # Omitted Logseq graph directory structure
├── /ImageToAVIF/       # Scripts for converting images to AVIF format
├── /Node/              # Node.js with pre-installed dependencies
├── /OtherDependencies/ # Some dependencies for installation, you can download the latest versions
├── /publish-spa/       # Project folder for publish-spa
├── /PublishWeb/        # Generated Logseq graph webpage
│   ├── /.git/
│   └── ...              # Omitted Logseq graph webpage structure
├── creatWeb.bat        # Manually generate webpage, but it will not upload
├── ImageToAVIF.bat     # Manually convert all images in the graph to AVIF format
├── PublishWeb.bat      # Manually perform Commit on /GraphsFile/, trigger hook to generate webpage
├── README.md
├── TestWebByPython.bat # Start HTTP server using Python for webpage testing
└── upload.log          # Git hook logs
```

### Projects Used by This Project

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