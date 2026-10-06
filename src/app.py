from flask import Flask, request, jsonify
from flask_cors import CORS
from calculator import calculate_expression
import database

app = Flask(__name__)
CORS(app)  # 允许跨域，方便本地调试

# 初始化数据库
database.init_db()

@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    """计算接口：接收表达式，后端计算并存入历史"""
    data = request.get_json()
    if not data or "expression" not in data:
        return jsonify({
            "success": False,
            "message": "缺少expression参数"
        }), 400
    
    expression = data["expression"].strip()
    success, result = calculate_expression(expression)
    
    if success:
        database.add_history(expression, result)
        return jsonify({
            "success": True,
            "expression": expression,
            "result": result
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": result
        }), 400

@app.route("/api/history", methods=["GET"])
def api_get_history():
    """获取全部计算历史"""
    history = database.get_all_history()
    return jsonify({
        "success": True,
        "data": history
    }), 200

@app.route("/api/history/<int:record_id>", methods=["DELETE"])
def api_delete_history(record_id):
    """删除指定ID的历史记录"""
    success = database.delete_history_by_id(record_id)
    if success:
        return jsonify({
            "success": True,
            "message": "删除成功"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "记录不存在"
        }), 404

@app.route("/api/history", methods=["DELETE"])
def api_clear_history():
    """清空所有历史（扩展功能）"""
    count = database.clear_all_history()
    return jsonify({
        "success": True,
        "message": f"已清空{count}条记录"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
