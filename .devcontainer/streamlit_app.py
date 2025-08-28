import streamlit as st
import streamlit.components.v1 as components
import os

# 设置页面配置
st.set_page_config(
    page_title="亚马逊价格规划看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main > div {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        margin: 0;
        padding: 0;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 使用说明弹窗样式 */
    .help-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.7);
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .help-content {
        background: white;
        padding: 30px;
        border-radius: 15px;
        max-width: 600px;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: slideIn 0.3s ease-out;
    }
    
    .help-minimized {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #ff9900, #ff7700);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        z-index: 1000;
        box-shadow: 0 5px 15px rgba(255,153,0,0.3);
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .help-minimized:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,153,0,0.4);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# 使用说明弹窗HTML和JavaScript
help_modal_html = """
<div id="helpModal" class="help-modal" style="display: block;">
    <div class="help-content">
        <div style="text-align: right; margin-bottom: 15px;">
            <button onclick="closeHelp()" style="background: #ff4444; color: white; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-weight: bold;">✕ 关闭</button>
        </div>
        <div style="line-height: 1.8; color: #333;">
            <h2 style="color: #667eea; margin-bottom: 20px;">📖 价格计算工具使用说明</h2>
            
            <h3 style="color: #764ba2; margin-top: 25px;">📖 功能简介</h3>
            <ul style="margin-left: 20px;">
                <li>快速计算商品活动前价格要求，并给出价格策略建议</li>
                <li>支持单条计算和批量导入/导出</li>
                <li>支持CSV和XLSX格式</li>
                <li>支持实时可视化结果</li>
            </ul>
            
            <h3 style="color: #764ba2; margin-top: 25px;">🚀 使用方法</h3>
            <ol style="margin-left: 20px;">
                <li><strong>单条计算</strong>：在对应输入框中输入参数，点击计算，查看计算结果和操作建议</li>
                <li><strong>批量导入/导出</strong>：下载模板，填写后上传，查看计算结果和操作建议，可直接线上查看结果也可批量下载结果</li>
            </ol>
            
            <h3 style="color: #764ba2; margin-top: 25px;">💡 提示</h3>
            <ul style="margin-left: 20px;">
                <li>所有数据仅在当前会话有效</li>
                <li>支持导出计算结果</li>
                <li>此工具仅作为价格推算参考，实际价格要求以卖家后台为准</li>
            </ul>
            
            <hr style="margin: 25px 0; border: none; border-top: 2px solid #eee;">
            <p style="text-align: center; color: #888; font-size: 14px;">© 版权所有：SL Merchandising Team + Liya Liang</p>
        </div>
    </div>
</div>

<div id="helpButton" class="help-minimized" onclick="showHelp()" style="display: none;">
    📖 使用说明
</div>

<script>
function closeHelp() {
    document.getElementById('helpModal').style.display = 'none';
    document.getElementById('helpButton').style.display = 'block';
}

function showHelp() {
    document.getElementById('helpModal').style.display = 'block';
    document.getElementById('helpButton').style.display = 'none';
}

// 点击模态框外部关闭
document.getElementById('helpModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeHelp();
    }
});
</script>
"""

# 显示帮助弹窗
components.html(help_modal_html, height=0)

# 读取并修改HTML文件以适配网页版
html_file_path = "amazon_pricing_dashboard_v1.5.html"

if os.path.exists(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 修改HTML以适配Streamlit和提升视觉效果
    enhanced_html = html_content.replace(
        '<body>',
        '''<body style="margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
        <style>
            .container { 
                max-width: 100% !important; 
                margin: 0 !important; 
                padding: 10px !important; 
            }
            .header {
                background: linear-gradient(135deg, rgba(102,126,234,0.9) 0%, rgba(118,75,162,0.9) 100%) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255,255,255,0.2) !important;
                box-shadow: 0 25px 50px rgba(0,0,0,0.2) !important;
            }
            .tab-content {
                background: rgba(255,255,255,0.98) !important;
                backdrop-filter: blur(30px) !important;
                border: 1px solid rgba(255,255,255,0.3) !important;
                box-shadow: 0 25px 60px rgba(0,0,0,0.15) !important;
            }
            .tab {
                background: rgba(255,255,255,0.95) !important;
                backdrop-filter: blur(15px) !important;
                border: 2px solid rgba(102,126,234,0.2) !important;
                box-shadow: 0 8px 25px rgba(102,126,234,0.1) !important;
            }
            .tab.active {
                background: linear-gradient(135deg, #667eea, #764ba2) !important;
                box-shadow: 0 15px 35px rgba(102,126,234,0.4) !important;
            }
            .btn {
                background: linear-gradient(135deg, #667eea, #764ba2) !important;
                box-shadow: 0 10px 30px rgba(102,126,234,0.3) !important;
                transform: translateY(0) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            .btn:hover {
                transform: translateY(-5px) !important;
                box-shadow: 0 20px 40px rgba(102,126,234,0.4) !important;
            }
            .price-card {
                background: rgba(255,255,255,0.95) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255,255,255,0.3) !important;
                box-shadow: 0 15px 35px rgba(0,0,0,0.1) !important;
                border-left: 5px solid #667eea !important;
            }
            .results {
                background: rgba(248,249,250,0.95) !important;
                backdrop-filter: blur(25px) !important;
                border: 1px solid rgba(255,255,255,0.4) !important;
                box-shadow: 0 20px 45px rgba(0,0,0,0.1) !important;
            }
            .form-group input, .form-group select {
                background: rgba(255,255,255,0.9) !important;
                backdrop-filter: blur(10px) !important;
                border: 2px solid rgba(102,126,234,0.2) !important;
                box-shadow: 0 5px 15px rgba(102,126,234,0.1) !important;
            }
            .form-group input:focus, .form-group select:focus {
                border-color: #667eea !important;
                box-shadow: 0 10px 25px rgba(102,126,234,0.2) !important;
            }
            .checkbox-item {
                background: rgba(255,255,255,0.8) !important;
                backdrop-filter: blur(15px) !important;
                border: 2px solid rgba(102,126,234,0.1) !important;
                box-shadow: 0 5px 15px rgba(102,126,234,0.05) !important;
            }
            .checkbox-item:hover {
                border-color: rgba(102,126,234,0.3) !important;
                box-shadow: 0 10px 25px rgba(102,126,234,0.15) !important;
            }
            .chart-container {
                background: rgba(255,255,255,0.98) !important;
                backdrop-filter: blur(25px) !important;
                border: 1px solid rgba(255,255,255,0.3) !important;
                box-shadow: 0 20px 50px rgba(0,0,0,0.1) !important;
            }
        </style>'''
    )
    
    # 在Streamlit中显示增强的HTML内容，调整高度以适配网页版
    components.html(enhanced_html, height=1200, scrolling=True)
else:
    st.error("HTML文件未找到，请确保文件存在于应用目录中")
