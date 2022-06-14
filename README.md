<h1 align="center">African language Speech Recognition - Speech-to-Text </h1>
<div>
<a href="https://github.com/week4-SpeechRecognition/Speech-to-Text"><img src="https://img.shields.io/github/forks/week4-SpeechRecognition/Speech-to-Text" alt="Forks Badge"/></a>
<a "https://github.com/week4-SpeechRecognition/Speech-to-Text/pulls"><img src="https://img.shields.io/github/issues-pr/week4-SpeechRecognition/Speech-to-Text" alt="Pull Requests Badge"/></a>
<a href="https://github.com/week4-SpeechRecognition/Speech-to-Text/issues"><img src="https://img.shields.io/github/issues/week4-SpeechRecognition/Speech-to-Text" alt="Issues Badge"/></a>
<a href="https://github.com/week4-SpeechRecognition/Speech-to-Text/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/week4-SpeechRecognition/Speech-to-Text?color=2b9348"></a>
<a href="https://github.com/week4-SpeechRecognition/Speech-to-Text/blob/main/LICENCE"><img src="https://img.shields.io/github/license/week4-SpeechRecognition/Speech-to-Text?color=2b9348" alt="License Badge"/></a>
</div>
</br>

## Table of Contents

* [African language Speech Recognition](#African-language-Speech-Recognition)
  - [Introduction](#Introduction)
  - [speech-to-text deep learning architecture](#architecture)
  - [Project Structure](#project-structure)
    * [data](#data)
    * [models](#models)
    * [notebooks](#notebooks)
    * [scripts](#scripts)
    * [sql](#sql)
    * [tests](#tests)
    * [logs](#logs)
    * [root folder](#root-folder)
  - [Installation guide](#installation-guide)

## Introduction

<p> Speech recognition technology allows for hands-free control of smartphones, speakers, and even vehicles in a wide variety of languages. Companies have moved towards the goal of enabling machines to understand and respond to more and more of our verbalized commands. There are many matured speech recognition systems available, such as Google Assistant, Amazon Alexa, and Apple’s Siri. However, all of those voice assistants work for limited languages only. </p>

<p>The World Food Program wants to deploy an intelligent form that collects nutritional information of food bought and sold at markets in two different countries in Africa - Ethiopia and Kenya. The design of this intelligent form requires selected people to install an app on their mobile phone, and whenever they buy food, they use their voice to activate the app to register the list of items they just bought in their own language. The intelligent systems in the app are expected to live to transcribe the speech-to-text and organize the information in an easy-to-process way in a database. </p>

<p>Our responsibility was to build a deep learning model that is capable of transcribing a speech to text in the Amharic language. The model we produce will be accurate and is robust against background noise.</p>

## Installation guide
### Conda Enviroment
```bash
conda create --name mlenv python==3.7.5
conda activate mlenv
```

### Installation of dependencies
```bash
git clone https://github.com/week4-SpeechRecognition/Speech-to-Text.git
cd Speech-to-Text
sudo python3 setup.py install
```

## Architecture

![speech-to-text deep learning architecture](images/Speech-to-Text-Architecture.JPG)

## Project Structure

### [images](images):

- `images/` the folder where all snapshot for the project are stored.

### [data](data):

 - `*.dvc` the folder where the dataset versioned files are stored.

### [.dvc](.dvc):
- `.dvc/`: the folder where dvc configured for data version control.

### [.github](.github):

- `.github/`: the folder where github actions and CML workflow is integrated.

### [.vscode](.vscode):

- `.vscode/`: the folder where local path fix are stored.

### [models](models):

- `models/` the folder where model pickle files are stored.

### [notebooks](notebooks):

- `notebooks/` include all notebooks for deep-learning and meta-data.

###  [scripts](scripts):

- `*.py`: Scripts for modularization, logging, and packaging.

### root folder:

- `requirements.txt`: a text file lsiting the projet's dependancies.
- `README.md`: Markdown text with a brief explanation of the project and the repository structure.
- `Dockerfile`: build users can create an automated build that executes several command-line instructions in a container.

## Contributors

<!-- Copy-paste in your Readme.md file -->
![contributors list](https://contrib.rocks/image?repo=week4-SpeechRecognition/Speech-to-Text)

Made with [contrib.rocks](https://contrib.rocks)