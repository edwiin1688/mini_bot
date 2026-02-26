# macOS 環境開發規則

## 1. 終端機

- 建議使用 **iTerm2** + **Oh My Zsh** 以獲得更好的開發體驗
- 使用 **Homebrew** 管理開發工具

## 2. Shell 指令語法

使用 Bash/Zsh 語法：

```bash
# 正確
find minibot -name "*.py" -type f | xargs wc -l
mkdir -p ~/.minibot
cp config.example.json ~/.minibot/config.json

# 錯誤（不要使用 PowerShell 語法）
Get-ChildItem
New-Item
Copy-Item
```

## 3. 路徑分隔符

- 使用正斜線 `/`
- 使用 `~` 代表使用者家目錄

## 4. 常用指令

```bash
# 安裝 Python 版本管理
brew install pyenv
pyenv install 3.11.9
pyenv local 3.11.9

# 安裝依賴
pip install -e .
```
