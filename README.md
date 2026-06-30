# MCP Word Server

一個基於 Flask 實作的 MCP（Model Context Protocol）伺服器，提供 Word 文件讀取工具，可綁定 MaiAgent 使用。Agent 只需輸入檔案路徑，即可讀取並回傳 Word 文件內容。

## 功能說明

- 實作 JSON-RPC 2.0 協議，符合 MCP 標準介面
- 提供 `open_word` 工具，讀取指定路徑的 `.docx` 檔案內容
- 內建健康檢查端點，方便確認伺服器運行狀態
- 自動擷取文件前 20 段落內容，避免回傳過長文字

## 技術棧

- Python
- Flask
- python-docx
- JSON-RPC 2.0
- MCP（Model Context Protocol）

## 使用情境

此工具設計用於整合至 MaiAgent，讓 Agent 在對話過程中能直接讀取使用者指定路徑的 Word 文件，並將內容作為回應依據，省去人工開啟、複製貼上文件內容的步驟。

## 安裝與啟動

```bash
pip install flask python-docx
python mcp_server.py
```

伺服器預設啟動於 `http://localhost:5005`。

## API 說明

### 健康檢查

```
GET /health
```

回傳伺服器運行狀態。

### MCP 初始化

```
POST /
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "initialize",
  "id": 1
}
```

### 列出可用工具

```
POST /
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 2
}
```

### 讀取 Word 文件

```
POST /
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "open_word",
    "arguments": {
      "file_path": "C:/path/to/document.docx"
    }
  },
  "id": 3
}
```

回傳格式：

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "檔案: ...\n\n內容:\n..."
      }
    ]
  },
  "id": 3
}
```

## 後續規劃

- 支援讀取段落以外的內容（表格、頁首頁尾）
- 擴充工具清單，支援 Word 文件寫入與編輯
- 加入錯誤重試機制與更完整的例外處理
