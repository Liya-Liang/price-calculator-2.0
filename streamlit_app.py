import streamlit as st
import streamlit.components.v1 as components
import os

# 设置页面配置
st.set_page_config(
    page_title="亚马逊价格规划看板",
    page_icon="📊",
    layout="wide"
)

# 读取HTML文件
html_file_path = "amazon_pricing_dashboard_v1.5.html"

if os.path.exists(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 在Streamlit中显示HTML内容
    components.html(html_content, height=800, scrolling=True)
else:
    st.error("HTML文件未找到，请确保文件存在于应用目录中")
