# mini_bot 專案開發規則 (AI Agent Guides)

## 1. 核心理念與原則
- **簡潔至上**：恪守 KISS (Keep It Simple, Stupid) 原則，維持 `minibot` 核心程式碼簡潔。
- **千行約定**：專案設計目標為「約 1000 行左右」跑通完整 Agent Loop 與雙通道（CLI + Telegram）的極簡框架，避免過度工程化。

## 2. Windows 開發注意事項
- **終端機**：Windows 環境必須使用 **PowerShell 7** (`pwsh`)，不要使用 CMD 或舊版 PowerShell。
- **Shell 指令**：在 Windows 上執行 Shell 工具時，會自動使用 PowerShell，請使用 PowerShell 語法（如 `Get-ChildItem` 而非 `ls`）。
- **路徑分隔符**：使用反斜線 `\` 或正斜線 `/` 均可相容。

## 3. ShellTool 跨平台問題記錄

### 3.1 問題描述
在 Windows 11 上使用 Python `subprocess` 呼叫 cmd 或內建 PowerShell 時，常遇到 stdout/stderr 無法擷取的問題（命令執行但無輸出）。

**原因**：Windows 11 中 cmd.exe 和內建 PowerShell (v5.1) 的輸出緩衝機制（全緩衝模式），導致 `subprocess.PIPE` 無法即時讀取輸出。

### 3.2 解決方案測試過程
1. **嘗試設定 COMSPEC 指向 內建 PowerShell (v5.1)**：使用 `os.environ["COMSPEC"]` 指向內建 PowerShell (v5.1)，仍有問題
2. **嘗試直接用 `powershell -Command`**：加上 `bufsize=0` 無緩衝，仍無法解決
3. **嘗試 ctypes 取得 Console Code Page**：編碼問題，仍無輸出
4. **最終解決方案**：使用 **plumbum** 庫，它能跨平台正常處理 subprocess 輸出

### 3.3 問題根因
- **有問題**：cmd.exe 與 Windows 內建 PowerShell (v5.1)
- **正常**：PowerShell 7
- **plumbum**：跨平台解決方案，統一處理各平台 subprocess 輸出

### 3.3 最終實作
```python
from plumbum import local
result = local(command, shell=True)
```

### 3.4 依賴
需安裝 `plumbum`：
```bash
pip install plumbum
```

## 4. 任務結束自檢與記錄規範 (Definition of Done)
在完成任何功能開發、Bug 修正或重構任務後，Agent **必須主動**執行以下的「程式碼行數統計」與記錄動作，幫助追蹤專案體積變化：

### 4.1 執行統計指令
請使用 PowerShell 執行以下指令，取得 `minibot` 套件下的最新 `.py` 檔案總行數：

```powershell
$total = (Get-ChildItem -Recurse -File -Filter *.py minibot | Get-Content | Measure-Object -Line).Lines; Write-Host "目前程式碼總行數: $total"
```

### 4.2 收尾與回報
1. **回報差異**：在任務完成的回覆中，主動向使用者報告程式碼行數變化（例如：「本次更新後，總行數由 938 行增至 950 行」）。
2. **自動化更新**：主動根據變更內容更新專案根目錄的 `CHANGELOG.md`。
3. 若單次修改導致行數暴增（>100行），請主動說明原因，並確認是否符合「簡潔至上」的核心原則。
