# Selenium + Pytest + Jenkins Demo — Setup Notes

A reference document describing the project layout and the terminal steps performed
to bring this project from an empty PyCharm directory to a working Selenium test
suite runnable both locally and from a Jenkins pipeline.

---

## 1. Project root layout (`C:\Users\Lenovo\PycharmProjects\selenium-jenkins-demo`)

```
selenium-jenkins-demo/
├── .git/                  # Git repository (initialized by PyCharm / git init)
├── .idea/                 # PyCharm project settings (auto-generated)
├── .junie/                # JetBrains AI assistant workspace (memory/plans)
├── .pytest_cache/         # Pytest's local cache (auto-generated on first run)
├── .venv/                 # Python virtual environment (created with `python -m venv`)
├── pages/                 # Page Object Model classes
│   ├── __init__.py
│   └── google_page.py     # Page object for google.com
├── tests/                 # Pytest test modules
│   ├── __init__.py
│   ├── conftest.py        # Shared fixtures + screenshot-on-failure hook
│   ├── test_google_page.py    # POM-based tests
│   └── test_google_search.py  # Plain Selenium tests
├── reports/               # Test reports (results.xml, report.html) — generated
├── screenshots/           # Screenshots saved by conftest on test failure
├── Jenkinsfile            # Declarative Jenkins pipeline definition
├── main.py                # Default PyCharm stub (not used by tests)
├── pytest.ini             # Pytest configuration (testpaths, discovery, addopts)
└── requirements.txt       # Pinned Python dependencies
```

---

## 2. Terminal steps performed (in order)

All commands were run from the project root in a PowerShell terminal inside PyCharm.

### 2.1 Create + activate the virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

PyCharm typically creates the `.venv` automatically when a new project is started;
the explicit command above is what the Jenkinsfile mirrors for CI.

### 2.2 Install Python dependencies

```powershell
python -m pip install --upgrade pip
pip install selenium pytest pytest-html webdriver-manager python-dotenv
pip freeze > requirements.txt
```

The `pip freeze` snapshot is what `requirements.txt` now contains
(selenium 4.44.0, pytest 9.0.3, pytest-html 4.2.0, webdriver-manager 4.1.1, …).

### 2.3 Create the project scaffold

```powershell
mkdir pages tests reports screenshots
ni pages\__init__.py
ni tests\__init__.py
```

Then the page object (`pages/google_page.py`), the tests
(`tests/test_google_search.py`, `tests/test_google_page.py`) and the shared
fixtures (`tests/conftest.py`) were authored in PyCharm.

### 2.4 Configure pytest

`pytest.ini` was created so that `pytest` (with no args) discovers everything
under `tests/`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v
```

### 2.5 Run the tests locally

```powershell
# basic run
pytest

# the same invocation Jenkins uses — produces JUnit XML + standalone HTML report
pytest --junitxml=reports\results.xml --html=reports\report.html --self-contained-html
```

The most recent local run produced `reports/results.xml` (4 tests, 0 failures,
~20 s total — timestamp 2026-05-26 10:28) and `reports/report.html`.

### 2.6 Commit to git

```powershell
git add .
git commit -m "Initial Selenium Pytest Jenkins framework"
```

Branch: `main`. Two commits exist on this branch (both initial scaffolding).

### 2.7 Wire up Jenkins

`Jenkinsfile` (declarative pipeline) was committed at the project root with four
stages — Checkout → Create venv → Install deps → Run Selenium tests — and a
`post { always { … } }` block that publishes the JUnit XML, the HTML report, and
archives screenshots. A Jenkins job was then pointed at this repo with
"Pipeline script from SCM" so each build executes the Jenkinsfile.

---

## 3. What each piece does

| File | Purpose |
| --- | --- |
| `pages/google_page.py` | Page Object for google.com. Exposes `open_google()`, `get_title()`, `is_search_box_visible()`. |
| `tests/conftest.py` | Defines the headless Chrome `driver` fixture and a `pytest_runtest_makereport` hook that saves a PNG into `screenshots/` whenever a test's `call` phase fails. |
| `tests/test_google_page.py` | POM-based tests: title contains "Google", search box visible. (Currently redeclares its own `driver` fixture — overrides the conftest one.) |
| `tests/test_google_search.py` | Plain (non-POM) Selenium tests covering the same two assertions; uses a maximized non-headless browser fixture. |
| `pytest.ini` | Tells pytest where tests live and to run verbose. |
| `requirements.txt` | Pinned dependency list — re-installed in Jenkins via `pip install -r`. |
| `Jenkinsfile` | CI definition; recreates the venv on the agent, installs deps, runs pytest with JUnit + HTML output, then publishes the reports and archives screenshots. |
| `main.py` | Leftover PyCharm sample — not referenced by tests, safe to delete. |

---

## 4. Re-running from scratch

To reproduce the whole flow on a fresh machine:

```powershell
git clone <repo-url> selenium-jenkins-demo
cd selenium-jenkins-demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest --junitxml=reports\results.xml --html=reports\report.html --self-contained-html
```

Open `reports\report.html` in a browser to view the run; any failures will have a
matching `screenshots\<test_name>.png` saved alongside.
