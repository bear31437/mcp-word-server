import pandas
from flask import Flask, request, jsonify
from docx import Document
import os
import json

app = Flask(__name__)

def create_json_rpc_response(result, id=None):
    """建立符合 JSON-RPC 2.0 的回應"""
    return jsonify({
        "jsonrpc": "2.0",
        "result": result,
        "id": id
    })

def create_json_rpc_error(code, message, id=None):
    """建立 JSON-RPC 2.0 錯誤回應"""
    return jsonify({
        "jsonrpc": "2.0",
        "error": {
            "code": code,
            "message": message
        },
        "id": id
    })

@app.route("/", methods=["GET", "POST"])
def handle_json_rpc():
    """處理 MCP JSON-RPC 請求"""
    # 處理 GET 請求 (健康檢查或連線測試)
    if request.method == "GET":
        return jsonify({
            "status": "ok",
            "message": "MCP Word Server is running",
            "protocol": "JSON-RPC 2.0",
            "endpoints": {
                "rpc": "POST /",
                "health": "GET /health"
            }
        })
    
    try:
        data = request.get_json()
        
        if not data:
            return create_json_rpc_error(-32700, "Parse error"), 400
        
        method = data.get("method")
        params = data.get("params", {})
        req_id = data.get("id")
        
        # MCP 初始化
        if method == "initialize":
            return create_json_rpc_response({
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "word-reader",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "tools": {}
                }
            }, req_id)
        
        # 列出可用工具
        elif method == "tools/list":
            return create_json_rpc_response({
                "tools": [
                    {
                        "name": "open_word",
                        "description": "開啟並讀取 Word 文件內容",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Word 檔案的完整路徑"
                                }
                            },
                            "required": ["file_path"]
                        }
                    }
                ]
            }, req_id)
        
        # 執行工具
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name == "open_word":
                file_path = tool_args.get("file_path")
                
                if not file_path or not os.path.exists(file_path):
                    return create_json_rpc_response({
                        "content": [
                            {
                                "type": "text",
                                "text": f"錯誤: 找不到檔案 {file_path}"
                            }
                        ],
                        "isError": True
                    }, req_id)
                
                try:
                    doc = Document(file_path)
                    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
                    content = "\n".join(paragraphs[:20])
                    
                    return create_json_rpc_response({
                        "content": [
                            {
                                "type": "text",
                                "text": f"檔案: {file_path}\n\n內容:\n{content}"
                            }
                        ]
                    }, req_id)
                    
                except Exception as e:
                    return create_json_rpc_response({
                        "content": [
                            {
                                "type": "text",
                                "text": f"讀取檔案時發生錯誤: {str(e)}"
                            }
                        ],
                        "isError": True
                    }, req_id)
            
            return create_json_rpc_error(-32601, f"Unknown tool: {tool_name}", req_id)
        
        # 未知方法
        else:
            return create_json_rpc_error(-32601, f"Method not found: {method}", req_id)
            
    except Exception as e:
        return create_json_rpc_error(-32603, f"Internal error: {str(e)}"), 500

@app.route("/health", methods=["GET"])
def health():
    """健康檢查端點"""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    print("🚀 MCP Word Server 啟動中...")
    print("📍 位址: http://localhost:5005")
    print("💡 使用 JSON-RPC 2.0 協議")
    app.run(host="0.0.0.0", port=5005, debug=False, use_reloader=False)