<div style="display: flex; align-items: center;">
<picture><img src="assets/logo.png" alt="Basic logo" width="70" style="border-radius : 8px;">
</picture>
<h1 style="margin-left:20px; border:none; font-size: 4rem; margin-bottom:-30px;">Basic</h1>
</div>

## Basic Programming Language
### Welcome to Basic
Basic is programming language built using python as interpreter. It has clean modular and easy to understand syntax.

Basic is a lightweight, intuitive programming language designed as an accessible entry point for students starting their programming journey. While it draws foundational inspiration from Python and other modern languages, it intentionally diverges in its implementation to prioritize simplicity and core logic.

## Getting Started
### Windows
installation is simple in windows if you have python already installed in your system 

if your system doesn't have python get from here [**Get Python**](https://www.python.org/downloads/)

1. Go to the [Release Page](https://github.com/muhammadrayyans/interpreter/releases)
2. Get the latest `win-basic` zip file installed
3. Unzip it and run on powershell
```ps1
 .\install.ps1
```

### Mac / Linux
installation in unix based os is also short step process

1. Go to the [Release Page](https://github.com/your-username/your-repo/releases)
2. Get the latest `unix-basic` zip file installed
3. Unzip it and run on terminal
```sh
$ ./install.sh
``` 
### Post installation
After this you can run `basic path/to/your_file.bc` from anywhere on your system to execute basic files. files should be created with the extension `.bc` vs-code intelligence for basic will be released shortly.

## Architectural Conventions
To maintain optimal parsing performance during this MVP stage, the language enforces the following compiler structures:

### Scope execution
- Block Definition: All execution items are contained within curly braces `{}`. This ensures that the interpreter clearly defines the boundaries of each scope.

- Conditional Evaluation: Conditions are evaluated using parentheses `(<condition_one> <operator> <condition_two>)`.
### Variables and Data Handling
- Variable Allocation: Due to the current architecture of Version 1.01, direct inline mathematical expressions are in development. For now, please perform calculations by assigning values to variables first.

- Declaration Requirements: To ensure stability in this MVP stage, all variables must be declared at the top of the scope before they are utilized.

- Modular Scope: The system utilizes scope-based variable management, allowing modules to interact seamlessly while maintaining clean data encapsulation.


