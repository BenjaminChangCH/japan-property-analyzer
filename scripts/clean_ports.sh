#!/bin/bash

# 端口清理腳本
# 用於清理被佔用的開發端口，避免 Flask 應用程式啟動衝突
# 作者: Benjamin Chang
# 日期: 2025-07-02

echo "🧹 清理開發端口..."
echo "=================================="

# 定義需要清理的端口
PORTS=(5000 5001 5002 5003 5004 5005 5006 5007 8080)

# 清理函數
clean_port() {
    local port=$1
    echo "檢查端口 $port..."
    
    # 查找佔用端口的程序
    pids=$(lsof -ti:$port 2>/dev/null)
    
    if [ -z "$pids" ]; then
        echo "✅ 端口 $port 可用"
    else
        echo "⚠️  端口 $port 被以下程序佔用: $pids"
        for pid in $pids; do
            # 獲取程序信息
            process_info=$(ps -p $pid -o comm= 2>/dev/null)
            echo "   PID $pid: $process_info"
            
            # 嘗試優雅關閉
            echo "   正在停止程序 $pid..."
            kill $pid 2>/dev/null
            
            # 等待 2 秒
            sleep 2
            
            # 檢查程序是否仍在運行
            if kill -0 $pid 2>/dev/null; then
                echo "   強制停止程序 $pid..."
                kill -9 $pid 2>/dev/null
            fi
        done
        
        # 再次檢查端口
        remaining_pids=$(lsof -ti:$port 2>/dev/null)
        if [ -z "$remaining_pids" ]; then
            echo "✅ 端口 $port 已清理"
        else
            echo "❌ 端口 $port 清理失敗，仍有程序: $remaining_pids"
        fi
    fi
    echo ""
}

# 清理所有端口
for port in "${PORTS[@]}"; do
    clean_port $port
done

echo "=================================="
echo "🎯 建議使用端口: 5001"
echo "啟動命令: PORT=5001 python main.py"
echo ""
echo "📋 當前端口使用情況:"
for port in "${PORTS[@]}"; do
    pids=$(lsof -ti:$port 2>/dev/null)
    if [ -z "$pids" ]; then
        echo "  端口 $port: 可用 ✅"
    else
        echo "  端口 $port: 佔用 ❌ (PID: $pids)"
    fi
done

echo ""
echo "🔧 Google OAuth 設定提醒:"
echo "請確保在 Google Cloud Console 中添加以下授權來源:"
echo "  http://localhost:5001"
echo "  http://localhost:5007"
echo "  http://localhost:8080" 