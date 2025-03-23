# 🤖 AIChat-CLI

**AIChat-CLI** is a powerful and user-friendly command-line tool built in **Python** to provide intelligent conversational capabilities directly from the terminal. Designed with developers and tech enthusiasts in mind, it integrates seamlessly with the **OpenAI API** (GPT-4o), allowing real-time, markdown-formatted, AI-assisted interaction — all without requiring a graphical interface.

---

## ✨ Features

- ✅ **OpenAI GPT-4o Support**
- ✅ **Code block rendering**
- ✅ **Markdown formatting**
- ✅ **Loading indicators**
- 🛠️ **Coming soon:**
  - Gemini API integration
  - Prompt stream mod

---

## ⚙️ Requirements

- Python `3.10+`
- `venv` (Python Virtual Environment)
- OpenAI API Key
- Linux, macOS, or Windows

---

## 📦 Installation

### 🔻 Clone the repository:
```bash
git clone https://github.com/gustavofalcao1/AIChat-CLI.git
cd AIChat-CLI
```

### 🚀 Auto-install (Linux only):
```bash
sudo chmod +x install.sh
sudo ./install.sh
```

### 🧹 Auto-uninstall (Linux only):
```bash
sudo chmod +x uninstall.sh
sudo ./uninstall.sh
```

---

## 🧰 Pre-execution Setup

### 📦 Linux Dependencies:
```bash
sudo apt install -y python3.10 python3.10-venv python3-pip binutils
```

### 🐍 Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

For **Windows**:
```powershell
venv\Scripts\activate
```

---

## ▶️ Execution

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the CLI:
```bash
python main.py
```
Or with Python 3 explicitly:
```bash
python3 main.py
```

### View CLI options:
```bash
python main.py -h
```

---

## 🛠 Build

To build a standalone binary (Linux):
```bash
python build.py
# or
python3 build.py
```

Then move the binary to system path:
```bash
sudo mv dist/aichat-cli /usr/local/bin/aichat
```

Now you can run:
```bash
aichat
```

---

## 🖼️ Screenshots

<p align="center">
  <img src="screenshots/screen1.png" alt="AIChat CLI" />
</p>

---

## 🐞 Known Issues

- [ ] Pressing `Enter` with an empty prompt triggers execution — should be ignored
- [ ] Duplciated logs file, on ``~/`` path and ``this root project`` path

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author
**Gustavo Falcão**  
[GitHub @gustavofalcao1](https://github.com/gustavofalcao1)  
[Project Repository](https://github.com/gustavofalcao1/AIChat-CLI)

---

