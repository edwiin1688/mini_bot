# TDD 開發執行指南 (AI Agent 專用)

本指南定義 AI Agent 在執行 TDD（測試驅動開發）時應遵循的流程、互動模式與回報機制。

---

## 1. TDD 核心循環

AI Agent 必須遵循 **Red-Green-Refactor** 循環：

```
┌─────────────────────────────────────────────────────────┐
│  1. RED    │ 寫一個失敗的測試 (預期失敗)                  │
│────────────┼────────────────────────────────────────────│
│  2. GREEN  │ 寫最少的生產程式碼讓測試通過                 │
│────────────┼────────────────────────────────────────────│
│  3. REFACTOR │ 重構程式碼 (保持測試通過)                 │
└─────────────────────────────────────────────────────────┘
         ↑___________________________________↓
              重複循環直到功能完成
```

---

## 2. Task 拆分原則

每個任務應拆分為 **可測試的子任務**：

| 拆分標準 | 說明 |
|----------|------|
| 單一職責 | 每個 function/class 只做一件事 |
| 可測試性 | 輸出可斷言、副作用可隔離 |
| 邊界條件 | 包含正常、邊界、錯誤情況 |

### Task 範例模板

```markdown
## Task: [功能名稱]

### 子任務
- [ ] T1: 寫測試 - [測試項目描述]
- [ ] T2: 實作 - [功能描述]
- [ ] T3: 重構 - [優化點]
- [ ] T4: 整合測試 - [端到端場景]
```

---

## 3. 互動回報機制

### 3.1 回報時機

每個 **子任務 (Sub-task)** 開始與完成時必須回報：

```
📋 [開始] T1: 寫測試 - 驗證使用者登入功能
   └─ 預期：建立 test_login_success, test_login_failure, test_login_invalid_password

✅ [完成] T1: 寫測試 - 通過 3/3 測試
   └─ 紅燈：符合預期
```

### 3.2 回報模板

```markdown
## 🚀 Task 進度回報

### 任務：[功能名稱]
**狀態**：進行中 / 完成

### 子任務進度
| 子任務 | 狀態 | 說明 |
|--------|------|------|
| T1: 寫測試 | ✅ 完成 | 3 tests passed |
| T2: 實作 | 🔄 進行中 | 實作中... |
| T3: 重構 | ⏳ 待處理 | - |
| T4: 整合測試 | ⏳ 待處理 | - |

### 變更檔案
- `src/auth.py` - 新增
- `tests/test_auth.py` - 新增
- `src/utils.py` - 修改

### 遇到問題
無 / [問題描述 + 詢問選項]
```

### 3.3 詢問時機

以下情況 **必須** 詢問開發者：

| 情況 | 詢問範例 |
|------|----------|
| 需求不明確 | 「請問登入失敗時要回傳錯誤訊息還是只回傳狀態碼？」 |
| 技術決策 | 「要用 mock 還是 spy？這個單元測試適合哪種？」 |
| 測試策略 | 「這個整合測試是否需要 mock 外部 API？」 |
| 優先順序 | 「有兩個功能都要做要先做哪個？」 |
| 發現風險 | 「重構可能影響現有功能，是否要額外新增回歸測試？」 |

---

## 4. 測試寫作規範

### 4.1 測試檔案結構

```python
# tests/test_module_name.py
import pytest
from minibot.module import ClassName

class TestClassName:
    """ClassName 的單元測試"""

    @pytest.fixture
    def subject(self):
        """建立測試主體"""
        return ClassName(param="test")

    def test_method_success(self, subject):
        """正常情況：method 應該回傳預期結果"""
        result = subject.method("input")
        assert result == expected

    def test_method_edge_case_empty(self, subject):
        """邊界情況：空輸入應回傳預設值"""
        result = subject.method("")
        assert result == default_value

    def test_method_error_invalid_input(self, subject):
        """錯誤情況：無效輸入應拋出 ValueError"""
        with pytest.raises(ValueError, match="invalid"):
            subject.method("invalid")
```

### 4.2 命名規範

| 類型 | 命名模式 | 範例 |
|------|----------|------|
| 測試檔案 | `test_<module>.py` | `test_auth.py` |
| 測試類別 | `Test<ClassName>` | `TestUserService` |
| 測試方法 | `test_<action>_<scenario>` | `test_login_success` |

### 4.3 測試隔離原則

- **每個測試獨立**：不依賴其他測試的執行順序
- **Given-When-Then**：明確 Arrange / Act / Assert 結構
- **不使用共享狀態**：避免 class variable 跨測試污染

---

## 5. 驗證清單

### 5.1 Task 開始前

- [ ] 確認需求與驗收標準
- [ ] 拆分可測試的子任務
- [ ] 確認測試檔案位置

### 5.2 Red 階段 (寫測試)

- [ ] 寫失敗的測試 (預期 FAILED)
- [ ] 確認失敗原因是「功能未實作」而非「語法錯誤」

### 5.3 Green 階段 (實作)

- [ ] 寫最少量程式碼通過測試
- [ ] 執行 `pytest` 確認全部通過

### 5.4 Refactor 階段

- [ ] 重構程式碼
- [ ] 確保測試仍然通過
- [ ] 檢查是否有重複程式碼

### 5.5 Task 完成前

- [ ] 執行完整測試套件 (`pytest`)
- [ ] 執行 Lint (`pylint` / `ruff`)
- [ ] 執行型別檢查 (`mypy`)
- [ ] 回報進度給開發者

---

## 6. 指令速查

| 動作 | 指令 |
|------|------|
| 執行所有測試 | `pytest` |
| 執行特定檔案 | `pytest tests/test_auth.py` |
| 執行並顯示輸出 | `pytest -v` |
| 執行並顯示覆蓋率 | `pytest --cov=minibot` |
| 只執行失敗的測試 | `pytest --lf` |
| 產生 JUnit XML | `pytest --junitxml=test-results.xml` |
| 最低覆蓋率門檻 | `pytest --cov-fail-under=80` |

---

## 7. 推薦工具與配置

### 7.1 測試覆蓋率

```bash
pip install pytest-cov
```

### 7.2 屬性測試 (Property-Based Testing)

```bash
pip install hypothesis
```

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a
```

### 7.3 Mutation 測試

驗證測試是否真正有效：

```bash
pip install mutmut
mutmut run
```

### 7.4 測試資料工廠

```bash
pip install factory-boy
```

```python
import factory
from minibot.models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    name = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.name}@example.com")
```

### 7.5 Mock 框架

```python
from unittest.mock import Mock, patch
import pytest

@pytest.fixture
def mock_api():
    with patch('minibot.clients.api.requests') as mock:
        mock.get.return_value.json.return_value = {"status": "ok"}
        yield mock
```

### 7.6 推薦的 pytest 配置

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers --cov=minibot --cov-fail-under=80"

[tool.coverage.run]
source = ["minibot"]
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "pass",
    "raise NotImplementedError",
    "@abstractmethod",
]

[tool.mutmut]
backup = false
context = true


---

## 8. 範例：完整 Task 流程

### Task: 新增使用者登入功能

```markdown
## 🚀 Task 進度回報

### 任務：使用者登入功能
**狀態**：進行中

---

### T1: 寫測試 (RED)
**狀態**：✅ 完成

```
$ pytest tests/test_auth.py::TestLogin
FAILED tests/test_auth.py::TestLogin::test_login_success - AttributeError: 'UserService' has no attribute 'login'
```

紅燈：符合預期 (功能未實作)

---

### T2: 實作登入功能 (GREEN)
**狀態**：🔄 進行中

正在實作 `UserService.login()` 方法...
```

```markdown
## 🚀 Task 進度回報

### 任務：使用者登入功能
**狀態**：✅ 完成

---

### T1: 寫測試 - ✅ 完成
- `test_login_success` - 驗證正確帳密
- `test_login_failure` - 驗證錯誤帳密
- `test_login_invalid_password` - 驗證密碼錯誤

### T2: 實作 - ✅ 完成
- `UserService.login()` 已實作
- `pytest tests/test_auth.py` - 3 passed

### T3: 重構 - ✅ 完成
- 提取 `verify_password()` 方法
- 使用 `dataclass` 替代 dict

### T4: 整合測試 - ✅ 完成
- 新增 `test_login_integration` - 通過

---

### 變更檔案
- `minibot/auth.py` - 新增
- `tests/test_auth.py` - 新增

### 驗證結果
```
pytest -v --cov=minibot
========== 15 passed, 1 skipped ==========
```
```

---

## 9. 開發者互動範例

### 範例 1: 需求確認

```
❓ 詢問：關於登入失敗的處理方式，請確認：
1. 是否要記錄失敗次數？（影響帳號鎖定功能）
2. 失敗訊息要顯示「帳號或密碼錯誤」還是分開顯示？
```

### 範例 2: 技術決策

```
❓ 詢問：在實作 HTTP Client 時，有兩個選項：
A. 使用 requests（簡單但同步）
B. 使用 httpx（支援非同步）

請問專案偏好哪個？目前看 `loop.py` 有使用 asyncio。
```

### 範例 3: 優先順序

```
⚠️ 發現：重構 `AuthService` 可能影響現有 3 個功能
- 登入
- 註冊
- 密碼重置

是否要：
1. 先做重構（風險較高）
2. 先新增功能再重構（時程較長）
3. 分階段重構？
```
