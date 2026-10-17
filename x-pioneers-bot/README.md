# 🚀 X PIONEERS | Official Telegram Bot

> **"One Team. One Vision. A Bigger Future."**

Official Telegram Bot for the **X PIONEERS** technology team (@XPioneersOfficialBot). Built with modern Python 3.12+, **aiogram 3.x**, **aiosqlite**, and **pytest**.

---

## 🌟 Overview & Identity

* **Bot Name:** X PIONEERS | Official
* **Username:** [@XPioneersOfficialBot](https://t.me/XPioneersOfficialBot)
* **Founder & Admin:** [@devazamov](https://t.me/devazamov)
* **Assistant Admin:** [@xvoid11](https://t.me/xvoid11)
* **Flagship Project:** **MAKTAB X** (Interactive educational platform & 3D learning world)
* **Mission:** Build a professional technology community focused on AI, software development, educational technology, and innovative projects.

---

## 🗂 Project Architecture

```text
x-pioneers-bot/
├── bot.py                  # Main async entry point, polling loop, DI container & command setup
├── config.py               # Settings, environment loader, project catalog, and security checks
├── requirements.txt        # Production dependencies (aiogram 3, aiosqlite, python-dotenv, pytest)
├── pytest.ini              # Automated test runner configuration
├── .env.example            # Environment variables template (NO SECRETS)
├── .gitignore              # Ignores .env, SQLite databases, Python caches, and logs
├── README.md               # Beginner-friendly setup guide for Windows & deployment
├── database/
│   ├── __init__.py
│   ├── db.py               # Asynchronous SQLite connection manager and auto-migration
│   ├── models.py           # Typed dataclasses (User, NewsPost, TeamApplication, BotEvent)
│   └── repository.py       # SQL repository with parameterized queries
├── handlers/
│   ├── __init__.py         # Router registration
│   ├── start.py            # /start welcome message, /help, main navigation
│   ├── about.py            # /about team information, mission, leadership
│   ├── projects.py         # /projects catalog and MAKTAB X detail screens
│   ├── news.py             # /news announcements & empty state handler
│   ├── applications.py     # 4-step Join the Team FSM form with review screen
│   ├── contact.py          # /contact official links to leadership
│   └── admin.py            # /admin dashboard, stats, news publisher, 2-step broadcast
├── keyboards/
│   ├── __init__.py
│   ├── main_menu.py        # 6-button main menu inline keyboard
│   ├── projects.py         # Dynamic catalog navigation buttons
│   └── admin.py            # Admin actions, status toggles, broadcast confirmation
├── services/
│   ├── __init__.py
│   ├── application_service.py  # Application data validation and review formatter
│   ├── news_service.py         # Announcement formatting and publishing
│   └── notification_service.py # Admin alerts and rate-limited user broadcast
├── states/
│   ├── __init__.py
│   ├── application_states.py   # ApplicationSG FSM states
│   └── admin_states.py         # PublishNewsSG & BroadcastSG FSM states
└── tests/
    ├── conftest.py         # Isolated in-memory SQLite fixtures
    ├── test_keyboards.py   # Inline keyboard structure tests
    ├── test_auth.py        # Numeric ID role authorization tests
    ├── test_applications.py# Validation & submission lifecycle tests
    ├── test_news.py        # Empty state & publishing tests
    └── test_callbacks.py   # Project catalog & event audit tests
```

---

## 🪟 Complete Beginner Setup Guide for Windows

Follow these step-by-step instructions in Windows using **PowerShell** or **Command Prompt (CMD)**.

### Step 1: Install Python
1. Visit [python.org/downloads](https://www.python.org/downloads/) and download **Python 3.12** (or 3.10+).
2. Run the installer. **CRITICAL:** Check the box that says:
   > ☑️ **"Add python.exe to PATH"** before clicking "Install Now".
3. Verify installation by opening PowerShell and running:
   ```powershell
   python --version
   ```

---

### Step 2: Open the Project Folder in VS Code
1. Open Visual Studio Code.
2. Select **File -> Open Folder...** and choose `x-pioneers-bot`.
3. Open the integrated terminal in VS Code using the shortcut:
   `Ctrl + \`` (backtick) or go to **Terminal -> New Terminal**.

---

### Step 3: Create a Virtual Environment
Isolating dependencies prevents conflicts with other Python projects on your computer.

In PowerShell:
```powershell
# Create the virtual environment named .venv
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell shows an `Execution_Policies` restriction, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once, then activate again).*

If using Command Prompt (cmd.exe):
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```
You will notice `(.venv)` appears at the start of your terminal prompt.

---

### Step 4: Install Dependencies
With your virtual environment active, run:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 5: Copy `.env.example` to `.env`
In PowerShell:
```powershell
Copy-Item .env.example .env
```
Or in CMD:
```cmd
copy .env.example .env
```

---

### Step 6: Configure the Bot Token Locally
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the instructions to create your bot name and username.
3. BotFather will provide an HTTP API token (e.g., `7123456789:AAHk...`).
4. Open the `.env` file in VS Code and paste your token:
   ```env
   BOT_TOKEN=7123456789:AAHk123456789...
   ```

---

### Step 7: Configure Founder & Assistant Admin Numeric Telegram IDs

> ⚠️ **IMPORTANT SECURITY NOTE:** Usernames can change at any time. Security and role-based permissions in this bot are enforced strictly through permanent **numeric Telegram IDs**.

#### How to find your numeric Telegram ID:
1. In Telegram, open [@userinfobot](https://t.me/userinfobot) or [@raw_data_bot](https://t.me/raw_data_bot).
2. Click **Start**. The bot will immediately reply with your numeric ID (e.g., `Id: 184729103`).
3. Have `@devazamov` and `@xvoid11` get their IDs.
4. Put the numbers into your `.env` file:
   ```env
   FOUNDER_ID=184729103
   ASSISTANT_ADMIN_ID=982374112
   ```

*(Optional)* You can also set `CHANNEL_URL=https://t.me/your_channel` or leave it blank to show the placeholder message.

---

### Step 8: Run the Bot
Start the bot using:
```powershell
python bot.py
```

You will see logging output confirming startup:
```text
2026-10-17 14:00:00 | INFO    | xpioneers | Starting X PIONEERS | Official (@XPioneersOfficialBot)...
2026-10-17 14:00:00 | INFO    | xpioneers.database | Initializing SQLite database at xpioneers.db
2026-10-17 14:00:00 | INFO    | xpioneers | Bot commands successfully registered with Telegram.
2026-10-17 14:00:00 | INFO    | xpioneers | Bot is ready. Starting polling loop...
```

---

### Step 9: Test Commands in Telegram
Open your bot in Telegram and test all features:
* Send `/start` — View the 6 main buttons.
* Click **👥 About the Team** — View team vision, areas, leadership, and flagship project.
* Click **🚀 Our Projects** — View the catalog and tap **MAKTAB X** for details.
* Click **📰 Latest News** — Shows empty state if none, or latest posts.
* Click **🤝 Join the Team** — Walk through the 4-step application form and submit. Notice leadership gets an instant notification!
* Send `/cancel` — Gracefully cancels any open form.
* Send `/admin` — Accessible only to your numeric ID! Try clicking **Publish News** or **Bot Statistics**.

---

### Step 10: Run Automated Tests
Unit tests run locally with isolated in-memory/temporary SQLite databases without needing an actual Telegram token:
```powershell
pytest
```
Or for detailed output:
```powershell
pytest -v
```

All 17 unit tests will pass in under 1 second!

---

### Step 11: Upload Code Safely to GitHub
Your `.gitignore` file already protects `.env`, database files, and caches. Verify:
```powershell
git status
```
Ensure `.env` and `*.db` are **NOT** listed under untracked files.

Commit and push:
```powershell
git init
git add .
git commit -m "feat: initial production-ready X PIONEERS telegram bot"
git branch -M main
git remote add origin https://github.com/your-username/x-pioneers-bot.git
git push -u origin main
```

---

### Step 12: Production Deployment Options

#### Option A: Linux VPS (Ubuntu / Debian) with `systemd` (Recommended)
1. Clone repo onto VPS:
   ```bash
   git clone https://github.com/your-username/x-pioneers-bot.git /opt/x-pioneers-bot
   cd /opt/x-pioneers-bot
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env && nano .env
   ```
2. Create systemd service `/etc/systemd/system/xpioneers-bot.service`:
   ```ini
   [Unit]
   Description=X PIONEERS Telegram Bot Service
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/opt/x-pioneers-bot
   ExecStart=/opt/x-pioneers-bot/.venv/bin/python bot.py
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```
3. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable xpioneers-bot
   sudo systemctl start xpioneers-bot
   ```

#### Option B: Docker Container
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```
Run with:
```bash
docker build -t xpioneers-bot .
docker run -d --name xpioneers-bot --env-file .env xpioneers-bot
```

---

## 🔒 Security Principles Enforced
* **Zero Secret Leakage:** Tokens and IDs reside strictly in `.env`.
* **Permanent Authorization:** Admin access is tied to numeric IDs, not mutable usernames.
* **SQL Injection Immune:** All SQLite queries use parameterized placeholders (`?`).
* **Non-blocking Event Loop:** `aiosqlite` runs all database operations asynchronously.
* **Broadcasting Safety:** Rate-limiting delay and 2-step confirmation prevent accidental spam.

---

## 📄 License & Community
Built for **X PIONEERS | Official**.  
Founder: @devazamov | Assistant: @xvoid11  
*One Team. One Vision. A Bigger Future.*
