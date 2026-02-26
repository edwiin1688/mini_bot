# Windows 環境開發規則

## 1. 終端機要求

- **必須使用 PowerShell 7** (`pwsh`)，請勿使用 CMD 或舊版 PowerShell (v5.1)
- Shell 工具在 Windows 上執行時，會自動使用 PowerShell

## 2. Shell 指令語法

使用 PowerShell 語法，而非 CMD 或 Bash：

```powershell
# 正確
Get-ChildItem -Recurse -File -Filter *.py minibot
New-Item -ItemType Directory -Force -Path ~/.minibot
Copy-Item config.example.json ~/.minibot/config.json

# 錯誤
ls -la
mkdir -p
cp
```

## 3. 路徑分隔符

- 使用反斜線 `\` 或正斜線 `/` 均可相容
- 使用 `~` 代表使用者家目錄

## 4. 依賴說明

在 Windows 11 上使用 Python `subprocess` 呼叫 cmd 或內建 PowerShell 時，常遇到 stdout/stderr 無法擷取的問題（命令執行但無輸出）。

**原因**：Windows 11 中 cmd.exe 和內建 PowerShell (v5.1) 的輸出緩衝機制（全緩衝模式），導致 `subprocess.PIPE` 無法即時讀取輸出。

**最終解決方案**：使用 **plumbum** 庫，它能跨平台正常處理 subprocess 輸出。

```python
from plumbum import local
result = local(command, shell=True)
```

**依賴**：
```bash
pip install plumbum
```
