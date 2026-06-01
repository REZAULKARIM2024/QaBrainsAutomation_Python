# 🐍 QA Brains Automation — Python + Playwright + Behave (BDD)
BDD test automation framework built with Python, Playwright, and Behave, featuring Page Object Model, Allure reporting, tagged smoke/regression suites, and graceful handling of known site issues.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.60.0-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)
![Behave](https://img.shields.io/badge/Behave-BDD-23D96C?style=for-the-badge&logo=cucumber&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-orange?style=for-the-badge)

A robust end-to-end test automation framework built with **Python**, **Playwright**, and **Behave BDD** — using the Page Object Model (POM) design pattern. Tests run against [practice.qabrains.com](https://practice.qabrains.com/).

---

## 📁 Project Structure

```
qaBrainsAutomation_Python/
│
├── config/
│   └── config.properties          # URL, browser, credentials config
│
├── features/                      # Behave BDD feature files
│   ├── Login.feature
│   ├── Logout.feature
│   ├── Registration.feature
│   ├── CartCheckout.feature
│   ├── ForgotPassword.feature
│   ├── SmokeTests.feature
│   ├── RegressionTests.feature
│   ├── environment.py             # before_scenario / after_scenario hooks
│   └── steps/                     # Step definitions
│       ├── common_steps.py
│       ├── login_steps.py
│       ├── logout_steps.py
│       ├── registration_steps.py
│       ├── cart_steps.py
│       ├── forgot_password_steps.py
│       ├── smoke_steps.py
│       └── regression_steps.py
│
├── pages/                         # Page Object Model (POM)
│   ├── login_page.py
│   ├── logout_page.py
│   ├── registration_page.py
│   ├── cart_page.py
│   ├── forgot_password_page.py
│   ├── home_page.py
│   └── search_page.py
│
├── utils/                         # Utility classes
│   ├── base_test.py               # Browser lifecycle manager
│   ├── driver_factory.py          # Thread-local browser factory
│   ├── config_reader.py           # Read config.properties
│   └── driver_helper.py           # Helper utilities
│
├── reports/                       # Test reports & screenshots
│   ├── report.html
│   └── screenshots/               # Auto-captured on failure
│
├── allure-results/                # Allure raw result files
├── behave.ini                     # Behave runner configuration
└── requirements.txt               # Python dependencies
```

---

## 🧪 Test Coverage

| Feature | Scenarios | Tags |
|---|---|---|
| 🔐 Login | Valid login, Invalid login | `@smoke` `@regression` `@Login` |
| 🚪 Logout | Successful logout | `@smoke` `@regression` `@Logout` |
| 📝 Registration | Valid registration, Invalid email | `@smoke` `@regression` `@Registration` |
| 🛒 Cart & Checkout | Add to cart, Remove from cart | `@smoke` `@regression` |
| 🔑 Forgot Password | Registered email, Unregistered email | `@smoke` `@regression` `@ForgotPassword` |
| 💨 Smoke Suite | Home page, Navigation, Wishlist | `@smoke` |
| 🔁 Regression Suite | Multiple products, Quantity update, Search | `@regression` |

---

## ⚙️ Prerequisites

- [Python 3.10+](https://www.python.org/downloads/) — install with **"Add Python to PATH"** checked
- [VS Code](https://code.visualstudio.com/) — recommended editor
- [Java 11+](https://adoptium.net/) — required for Allure reports
- [Allure](https://allurereport.org/) — for beautiful test reports

---

## 🚀 Setup & Installation

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/qaBrainsAutomation_Python.git
cd qaBrainsAutomation_Python
```

**2. Create and activate virtual environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows Command Prompt)
venv\Scripts\activate

# Activate (Windows PowerShell)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1

# Activate (Mac/Linux)
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Install Playwright browser:**
```bash
playwright install chromium
```

**5. Install Allure (for reports):**
```powershell
# Windows — PowerShell
irm get.scoop.sh | iex
scoop install allure

# Mac
brew install allure
```

---

## ▶️ Running Tests

> ⚠️ **Windows Users:** Always activate venv first. Run `behave` from the `qaBrainsAutomation_Python` inner folder.

| Command | Description |
|---|---|
| `behave` | Run all tests (smoke + regression) |
| `behave --tags @smoke` | Run Smoke tests only |
| `behave --tags @regression` | Run Regression tests only |
| `behave --tags @Login` | Run Login tests only |
| `behave --tags @Logout` | Run Logout tests only |
| `behave --tags @Registration` | Run Registration tests only |
| `behave --tags @ForgotPassword` | Run Forgot Password tests only |
| `behave features/Login.feature` | Run a specific feature file |

---

## 📊 Test Reports

### HTML Report (built-in)
After running tests, open:
```bash
# Windows
start reports\report.html

# Mac/Linux
open reports/report.html
```

### Allure Report (detailed & interactive)

**Step 1:** Run tests with Allure formatter:
```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results --no-capture
```

**Step 2:** Serve the report:
```bash
# Windows PowerShell — add PATH first
$env:PATH += ";$env:USERPROFILE\scoop\shims"

allure serve allure-results
```

Browser will open automatically with a beautiful interactive report! 🎉

---

## 🏗️ Framework Architecture

```
Feature File (.feature)
        ↓
Step Definitions (features/steps/*.py)
        ↓
Page Object Model (pages/*.py)
        ↓
BaseTest (utils/base_test.py)
        ↓
Playwright Browser (Chromium)
        ↓
environment.py
(before_scenario → open browser | after_scenario → close + screenshot on fail)
```

---

## 🔧 Configuration

Edit `config/config.properties`:

```properties
url=https://practice.qabrains.com/
browser=chrome
headless=false
timeout=10
valid_email=qa_testers@qabrains.com
valid_password=Password123
screenshot_on_failure=true
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Python](https://www.python.org/) | Programming language |
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [Behave](https://behave.readthedocs.io/) | BDD framework |
| [Allure](https://allurereport.org/) | Test reporting |
| [pytest](https://pytest.org/) | Test utilities |

---

## 👤 Author

**Rezaul Karim**
QA Engineer | QA Brains

---

## 📄 License

This project is for educational and practice purposes via [QA Brains](https://qabrains.com/).
