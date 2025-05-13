# 🧪 Software Quality in this Flask REST Project

This project uses a set of **formatting**, **linting**, and **static analysis** tools to ensure clean, readable, secure, and maintainable code.
These tools are automatically executed using [**pre-commit**](https://pre-commit.com/) at every Git commit.

---

## 📋 Table of Contents

1. [Tool Installation](#tool-installation)
2. [Tool Overview](#tool-overview)

   * [Black (auto-formatter)](#1-black)
   * [isort (import sorting)](#2-isort)
   * [flake8 (style analysis)](#3-flake8)
   * [Bandit (security analysis)](#4-bandit)
   * [Pylint (comprehensive analysis)](#5-pylint)
   * [Commit message validation](#6-commit-message-validation)
   * [docformatter (docstring formatter)](#7-docformatter)
   * [detect-secrets (secret detection)](#8-detect-secrets)
   * [General hooks (YAML, EOL, whitespace)](#9-general-hooks)
   * [pytest (unit tests)](#10-pytest)
   * [radon (cyclomatic complexity)](#11-radon)
3. [Manual Use](#manual-use)
4. [Best Practices](#best-practices)

---

## 💾 Tool Installation

1. Install development dependencies:

```bash
pip install -r requirements.dev.txt
```

2. Install Git hooks (only once):

```bash
# Code quality hooks
pre-commit install

# (Optional) Commit message validation hook
pre-commit install --hook-type commit-msg
```

---

## 🛠️ Tool Overview

### 1. [Black](https://black.readthedocs.io/en/stable/) – Auto Formatter

> "The uncompromising code formatter."

* Automatically formats Python code according to strict rules.
* Aims for total consistency: no style debates.
* Compatible with `isort`.

**Configuration:**

* Max line length: `79`
* Excluded directories: `.git`, `.venv`, `build`, etc.

**Manual command:**

```bash
black .
```

---

### 2. [isort](https://pycqa.github.io/isort/) – Import Sorting

> Sorts imports into logical sections.

* Separates standard, third-party, and local imports.
* Compatible with Black style (`profile = "black"`).

**Configuration:**

* Line length: `79`
* Aware of local module `monpackage`

**Manual command:**

```bash
isort .
```

---

### 3. [flake8](https://flake8.pycqa.org/en/latest/) – Style Linting

> Combines PyFlakes, pycodestyle, McCabe complexity checker.

* Detects style, syntax errors, and code complexity.
* Complements Black by catching non-formatting issues.

**Configuration:**

* Max line length: `79`
* Max complexity per function: `10`
* Excluded folders: `.venv`, `.github`

**Manual command:**

```bash
flake8 .
```

---

### 4. [Bandit](https://bandit.readthedocs.io/en/latest/) – Security Analysis

> Looks for common vulnerabilities.

* Flags dangerous functions like `eval`, `exec`, etc.
* Ignores some false positives.
* Configured via `pyproject.toml`.

**Excluded folders:** `tests`, `.venv`, `.github`
**Checks include:** open ports, hardcoded secrets, template injection/XSS, SSL/TLS, etc.

**Manual command:**

```bash
bandit -c pyproject.toml -r .
```

---

### 5. [Pylint](https://pylint.pycqa.org/en/latest/) – Comprehensive Analysis

> Very strict and complete static analysis tool.

* Checks syntax, types, naming conventions, missing docstrings, etc.
* Assigns a quality score to each file.

**Configuration:**

* Max line length: `79`
* Partial disabling of docstring checks (e.g., `missing-module-docstring`)
* Integrated via local hook to avoid version conflicts

**Manual command:**

```bash
pylint monpackage/
```

---

### 6. ✅ Commit Message Validation

> Ensures commit messages follow a convention.

* Local script: `scripts/check_commit_msg.py`
* Executed only at commit time (`commit-msg`)
* Ideal for enforcing [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

---

### 7. [docformatter](https://github.com/PyCQA/docformatter) – Docstring Formatter

> Formats docstrings according to PEP 257.

* Improves inline comment readability.
* Complements Black.

**Manual command:**

```bash
docformatter --in-place --recursive .
```

---

### 8. [detect-secrets](https://github.com/Yelp/detect-secrets) – Secret Detector

> Prevents secrets (API keys, passwords, tokens...) from leaking.

* Scans files before commit.
* Uses a baseline to ignore known false positives.

**Installation and baseline creation:**

```bash
pip install detect-secrets
detect-secrets scan > .secrets.baseline
```

---

### 9. General Hooks – [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)

> General repository hygiene.

* YAML file validation
* Trailing whitespace removal
* Final newline enforcement

---

### 10. [pytest](https://docs.pytest.org/) – Test Execution (optional)

> Prevents commits if tests fail.

* Pre-configured local hook runs `pytest` before commit.

---

### 11. [radon](https://radon.readthedocs.io/) – Complexity Analysis

> Analyzes cyclomatic complexity and maintainability index.

**Manual command:**

```bash
radon cc -nc -s .
```

---

## 🧪 Manual Use

You can run quality tools manually:

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run a specific hook (e.g., Black)
pre-commit run black --all-files
```

---

## ✅ Best Practices

* 🔄 **Before every major commit**: run `pre-commit run --all-files`
* 🧼 **Let Black and isort format code automatically**
* ⚠️ **If a hook fails**, read the error messages (often flake8, bandit or pylint)
* 📚 **Follow naming conventions and document your code**
