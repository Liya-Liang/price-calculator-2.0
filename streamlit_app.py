import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 页面配置
st.set_page_config(
    page_title="亚马逊价格规划看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS - 完全复制HTML版本的样式
st.markdown("""
<style>
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* 主体样式 */
    .main { 
        padding-top: 0rem; 
        padding-bottom: 0rem;
    }
    
    .stApp { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 容器样式 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* 帮助卡片样式 */
    .help-card {
        background: rgba(255,255,255,0.98);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.15);
        margin-bottom: 30px;
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255,255,255,0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    /* 标题样式 */
    .main-header {
        background: linear-gradient(135deg, rgba(102,126,234,0.9) 0%, rgba(118,75,162,0.9) 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    .main-header h1 {
        font-size: 2.8em;
        margin-bottom: 15px;
        font-weight: 300;
        letter-spacing: 2px;
        position: relative;
        z-index: 1;
        margin: 0;
    }
    
    .main-header p {
        font-size: 1.2em;
        opacity: 0.9;
        position: relative;
        z-index: 1;
        margin: 10px 0 0 0;
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 18px 35px;
        border: 2px solid transparent;
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(102,126,234,0.3);
        border-color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102,126,234,0.4);
    }
    
    /* 内容区域样式 */
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(255,255,255,0.98);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.15);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255,255,255,0.3);
        margin-top: 20px;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {
        background: rgba(255,255,255,0.9);
        border: 2px solid rgba(102,126,234,0.2);
        border-radius: 12px;
        padding: 15px 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 5px 15px rgba(102,126,234,0.1);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 10px 25px rgba(102,126,234,0.2);
        transform: translateY(-2px);
    }
    
    /* 标签样式 */
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stDateInput > label {
        font-weight: 600;
        color: #2c3e50;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    
    /* 复选框样式 */
    .stCheckbox {
        background: rgba(255,255,255,0.8);
        padding: 15px;
        border-radius: 12px;
        border: 2px solid rgba(102,126,234,0.1);
        transition: all 0.3s ease;
        margin: 5px 0;
    }
    
    .stCheckbox:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102,126,234,0.2);
        border-color: rgba(102,126,234,0.3);
        background: rgba(255,255,255,0.9);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 18px 40px;
        border-radius: 15px;
        font-size: 16px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(102,126,234,0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* 指标卡片样式 */
    .metric-card {
        background: rgba(255,255,255,0.95);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.3);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateX(5px);
        box-shadow: 0 15px 40px rgba(102,126,234,0.2);
    }
    
    .price-highlight {
        font-size: 24px;
        font-weight: bold;
        color: #667eea;
        margin: 10px 0;
    }
    
    /* 结果区域样式 */
    .results-section {
        background: rgba(248,249,250,0.95);
        padding: 30px;
        border-radius: 20px;
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0 20px 45px rgba(0,0,0,0.1);
        margin-top: 30px;
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* 数据框样式 */
    .stDataFrame {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* 图表容器样式 */
    .chart-container {
        background: rgba(255,255,255,0.98);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255,255,255,0.3);
        margin-top: 20px;
    }
    
    /* 动画效果 */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2.2em; }
        .block-container { padding: 15px; }
        .stTabs [data-baseweb="tab-panel"] { padding: 25px; }
    }
</style>
""", unsafe_allow_html=True)

# 促销规则配置 - 根据文档更新
PROMO_RULES = {
    "US": {
        "regular": {
            "manualBestDeal": {"discount": 20, "hamp_net_requirement": True, "was_price_requirement": True},
            "selfServiceBestDeal": {"discount": 10, "hamp_net_requirement": True, "was_price_requirement": True},
            "lightningDeal": {"discount": 15, "hamp_net_requirement": True, "was_price_requirement": True},
            "priceDiscount": {"discount": 5, "t30_discount": 5, "current_price_discount": 5},
            "primeExclusive": {"discount": 5, "t30_discount": 5, "current_price_discount": 5},
            "coupon": {"discount_min": 5, "discount_max": 50, "was_price_max_increase": 30, "was_price_discount": 5}
        },
        "major": {
            "manualBestDeal": {"discount": 30, "hamp_net_requirement": True, "was_price_discount": 5},
            "selfServiceBestDeal": {"discount": 15, "hamp_net_requirement": True, "was_price_discount": 5},
            "lightningDeal": {"discount": 20, "hamp_net_requirement": True, "was_price_discount": 5},
            "priceDiscount": {"discount": 5, "t30_discount": 5, "current_price_discount": 5},
            "primeExclusive": {"discount": 15, "t30_discount": 5, "was_price_discount": 5, "t30_promo_requirement": True},
            "coupon": {"discount_min": 5, "discount_max": 50, "was_price_max_increase": 30, "was_price_requirement": True}
        }
    },
    "CA": {
        "regular": {
            "manualBestDeal": {"discount": 20, "hamp_net_requirement": True, "was_price_requirement": True},
            "selfServiceBestDeal": {"discount": 10, "hamp_net_requirement": True, "was_price_requirement": True},
            "lightningDeal": {"discount": 15, "hamp_net_requirement": True, "was_price_requirement": True},
            "priceDiscount": {"discount": 5, "t30_discount": 5, "current_price_discount": 5},
            "primeExclusive": {"discount": 5, "t30_discount": 5, "current_price_discount": 5},
            "coupon": {"discount_min": 5, "discount_max": 50, "was_price_max_increase": 30, "was_price_requirement": True}
        },
        "major": {
            "manualBestDeal": {"discount": 30, "hamp_net_requirement": True, "was_price_discount": 5},
            "selfServiceBestDeal": {"discount": 15, "hamp_net_requirement": True, "was_price_discount": 5},
            "lightningDeal": {"discount": 20, "hamp_net_requirement": True, "was_price_discount": 5},
            "priceDiscount": {"discount": 5, "t30_discount": 5, "current_price_discount": 5},
            "primeExclusive": {"discount": 15, "t30_discount": 5, "was_price_discount": 5, "t30_promo_requirement": True},
            "coupon": {"discount_min": 5, "discount_max": 50, "was_price_max_increase": 30, "was_price_requirement": True}
        }
    }
}

# 大促日历信息
MAJOR_SALES_CALENDAR = {
    "US": [
        {"name": "Prime Big Deal Day", "start": "2025-10-07", "end": "2025-10-08"},
        {"name": "BFCM", "start": "2025-11-20", "end": "2025-12-01"}
    ],
    "CA": [
        {"name": "Prime Big Deal Day", "start": "2025-10-07", "end": "2025-10-10"},
        {"name": "BFCM", "start": "2025-11-20", "end": "2025-12-01"}
    ]
}

# 使用说明
# 通过查询参数控制初始弹出与再次打开：首次进入自动打开；之后仅当带有 help=open 时打开
def _get_query_params_safe():
    try:
        # 新版 Streamlit
        return dict(st.query_params)
    except Exception:
        try:
            # 兼容旧版
            return {k: v[0] if isinstance(v, list) and v else v for k, v in st.experimental_get_query_params().items()}
        except Exception:
            return {}

if 'help_initialized' not in st.session_state:
    st.session_state.help_initialized = True
    st.session_state.show_help = True
else:
    params = _get_query_params_safe()
    st.session_state.show_help = params.get('help') == 'open'

# 右上角使用说明按钮（始终显示）
st.markdown("""
<style>
    .help-button {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        border: none;
        padding: 12px 20px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
        transition: all 0.3s ease;
        text-decoration: none !important;
        display: inline-block;
    }
    .help-button:hover { transform: translateY(-3px); box-shadow: 0 12px 35px rgba(102,126,234,0.4); }
    
    .help-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(5px);
    }
    
    .help-modal-content {
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.3);
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        position: relative;
        animation: modalSlideIn 0.3s ease-out;
    }
    
    @keyframes modalSlideIn {
        from { opacity: 0; transform: translateY(-30px) scale(0.9); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    .close-button {
        position: absolute;
        top: 15px;
        right: 20px;
        background: #f8f9fa;
        border: none;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 18px;
        color: #666;
        transition: all 0.3s ease;
    }
    
    .close-button:hover {
        background: #e9ecef;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# 右上角使用说明按钮（固定位置，点击通过URL参数打开弹窗）
st.markdown('<a class="help-button" href="?help=open">📖 使用说明</a>', unsafe_allow_html=True)

# 使用说明弹窗
if st.session_state.show_help:
    st.markdown("""
<div class="help-modal" id="helpModal">
<div class="help-modal-content">
<a class="close-button" href="?help=close" style="display:inline-flex; align-items:center; justify-content:center; text-decoration:none;">×</a>
<h2 style="color: #667eea; margin-bottom: 25px; text-align: center;">📖 价格计算工具使用说明</h2>

<div style="margin-bottom: 25px;">
<h3 style="color: #764ba2; margin-bottom: 15px;">🚀 功能简介</h3>
<ul style="line-height: 1.8; color: #555;">
<li>快速计算商品活动前价格要求，并给出价格策略建议</li>
<li>支持单条计算和批量导入/导出</li>
<li>支持CSV和XLSX格式</li>
<li>支持实时可视化结果</li>
</ul>
</div>

<div style="margin-bottom: 25px;">
<h3 style="color: #764ba2; margin-bottom: 15px;">📋 使用方法</h3>
<ol style="line-height: 1.8; color: #555;">
<li><strong>单条计算</strong>：在对应输入框中输入参数，点击计算，查看计算结果和操作建议</li>
<li><strong>批量导入/导出</strong>：下载模板，填写后上传，查看计算结果和操作建议，可直接线上查看结果也可批量下载结果</li>
</ol>
</div>

<div style="margin-bottom: 25px;">
<h3 style="color: #764ba2; margin-bottom: 15px;">💡 提示</h3>
<ul style="line-height: 1.8; color: #555;">
<li>所有数据仅在当前会话有效</li>
<li>支持导出计算结果</li>
<li><strong>此工具仅作为价格推算参考，实际价格要求以卖家后台为准</strong></li>
</ul>
</div>

<div style="text-align: center; padding-top: 20px; border-top: 1px solid #eee;">
<p style="color: #888; margin: 0;">© 版权所有：SL merchandising team + Liya Liang</p>
</div>
</div>
</div>

<script></script>
""", unsafe_allow_html=True)

# 主标题和促销日历布局
col_main, col_calendar = st.columns([3, 1])

with col_main:
    st.markdown("""
    <div class="main-header">
        <h1>亚马逊价格规划看板</h1>
        <p>专业的促销价格规划工具</p>
    </div>
    """, unsafe_allow_html=True)

with col_calendar:
    # 大促日历模块 - 优化后的样式
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,249,250,0.95) 100%); 
                padding: 25px; 
                border-radius: 20px; 
                box-shadow: 0 15px 40px rgba(0,0,0,0.1); 
                margin-top: 20px;
                border: 1px solid rgba(255,255,255,0.3);
                backdrop-filter: blur(20px);">
        
        <div style="text-align: center; margin-bottom: 25px;">
            <h3 style="color: #667eea; margin: 0; font-size: 18px; font-weight: 600;">
                📅 2025年大促日历
            </h3>
        </div>
        
        <div style="margin-bottom: 25px; padding: 15px; background: rgba(102,126,234,0.1); border-radius: 12px;">
            <h4 style="color: #667eea; margin: 0 0 12px 0; font-size: 16px; font-weight: 600;">
                🇺🇸 美国站
            </h4>
            <div style="font-size: 13px; line-height: 1.6;">
    """, unsafe_allow_html=True)
    
    for event in MAJOR_SALES_CALENDAR["US"]:
        st.markdown(f"""
        <div style="margin-bottom: 8px; padding: 8px; background: white; border-radius: 8px; border-left: 3px solid #667eea;">
            <div style="font-weight: 600; color: #2c3e50; margin-bottom: 4px;">{event['name']}</div>
            <div style="color: #666; font-size: 12px;">{event['start']} 至 {event['end']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
        
        <div style="padding: 15px; background: rgba(118,75,162,0.1); border-radius: 12px;">
            <h4 style="color: #764ba2; margin: 0 0 12px 0; font-size: 16px; font-weight: 600;">
                🇨🇦 加拿大站
            </h4>
            <div style="font-size: 13px; line-height: 1.6;">
    """, unsafe_allow_html=True)
    
    for event in MAJOR_SALES_CALENDAR["CA"]:
        st.markdown(f"""
        <div style="margin-bottom: 8px; padding: 8px; background: white; border-radius: 8px; border-left: 3px solid #764ba2;">
            <div style="font-weight: 600; color: #2c3e50; margin-bottom: 4px;">{event['name']}</div>
            <div style="color: #666; font-size: 12px;">{event['start']} 至 {event['end']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(0,0,0,0.1);">
            <div style="font-size: 12px; color: #888;">
                💡 点击右上角"使用说明"查看详细功能
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 标签页
tab1, tab2 = st.tabs(["🔍 单个ASIN查询", "📊 批量ASIN处理"])

def validate_promo_types(selected_types):
    """验证促销类型组合"""
    exclusive_types = ['manualBestDeal', 'selfServiceBestDeal', 'lightningDeal', 'priceDiscount', 'primeExclusive']
    selected_exclusive = [t for t in selected_types if t in exclusive_types]
    has_coupon = 'coupon' in selected_types
    
    if len(selected_exclusive) > 1:
        return {"valid": False, "message": "禁止：顶级促销、Z划算、秒杀、Prime专享折扣、价格折扣不能同时选择"}
    
    if has_coupon and len(selected_exclusive) > 0:
        return {"valid": True, "message": "价格将会叠加：优惠券与其他促销类型叠加计算"}
    
    return {"valid": True, "message": ""}

def calculate_stacked_discount(selected_types, vrp):
    """计算叠加折扣"""
    exclusive_types = ['manualBestDeal', 'selfServiceBestDeal', 'lightningDeal', 'priceDiscount', 'primeExclusive']
    selected_exclusive = [t for t in selected_types if t in exclusive_types]
    has_coupon = 'coupon' in selected_types
    
    if not has_coupon:
        return 0
    
    coupon_discount = 0.25  # 优惠券25%
    
    if any(t in ['manualBestDeal', 'selfServiceBestDeal', 'lightningDeal'] for t in selected_exclusive):
        # 秒杀/顶级促销/Z划算(20% off) + 优惠券(25% off) = 45% off
        total_discount = 0.45
    elif any(t in ['primeExclusive', 'priceDiscount'] for t in selected_exclusive):
        # 优惠券(25% off) + Prime专享折扣/价格折扣(30% off) = 47.5% off
        total_discount = 0.475
    else:
        total_discount = coupon_discount
    
    return vrp * (1 - total_discount)

def calculate_pricing(historical_price, vrp, t30_lowest_price, t30_lowest_price_with_promo, selected_types, rules):
    """根据文档要求计算价格"""
    results = {
        "prePromoMaxPrice": vrp * 0.95,
        "promoMaxPrice": vrp,
        "postPromoPrice": vrp * 0.95,
        "logic": []
    }
    
    if not selected_types:
        results["logic"].append("无促销活动，建议保持VRP价格")
        return results
    
    # 验证促销类型组合
    validation = validate_promo_types(selected_types)
    if not validation["valid"]:
        results["logic"].append(f"错误：{validation['message']}")
        return results
    
    if validation["message"]:
        results["logic"].append(validation["message"])
    
    # 计算叠加折扣
    if 'coupon' in selected_types and len([t for t in selected_types if t in ['manualBestDeal', 'selfServiceBestDeal', 'lightningDeal', 'priceDiscount', 'primeExclusive']]) > 0:
        stacked_price = calculate_stacked_discount(selected_types, vrp)
        results["promoMaxPrice"] = stacked_price
        results["logic"].append(f"叠加计算后最终价格: ${stacked_price:.2f}")
        return results
    
    # 单独促销类型计算
    min_promo_price = vrp
    
    for promo_type in selected_types:
        if promo_type not in rules:
            continue
            
        rule = rules[promo_type]
        
        if promo_type == 'coupon':
            # 优惠券特殊处理
            discount_price = vrp * 0.75  # 默认25%折扣
            
            # 检查was_price要求
            if rule.get("was_price_requirement") and discount_price >= historical_price:
                discount_price = historical_price * 0.95
            
            # 检查was_price最大增幅要求
            if rule.get("was_price_max_increase"):
                max_current_price = historical_price * (1 + rule["was_price_max_increase"] / 100)
                if vrp > max_current_price:
                    results["logic"].append(f"警告：当前价格超过was_price的{rule['was_price_max_increase']}%限制")
            
            min_promo_price = min(min_promo_price, discount_price)
            results["logic"].append(f"优惠券: 建议价格 ${discount_price:.2f}")
            
        else:
            # 其他促销类型
            discount_price = vrp * (1 - rule["discount"] / 100)
            
            # HAMP Net Price要求
            if rule.get("hamp_net_requirement") and discount_price > t30_lowest_price:
                discount_price = t30_lowest_price
                results["logic"].append(f"{promo_type}: 受HAMP Net Price限制")
            
            # was_price要求
            if rule.get("was_price_requirement") and discount_price >= historical_price:
                discount_price = historical_price * 0.95
                results["logic"].append(f"{promo_type}: 受was_price限制")
            
            # was_price折扣要求
            if rule.get("was_price_discount"):
                required_price = historical_price * (1 - rule["was_price_discount"] / 100)
                if discount_price > required_price:
                    discount_price = required_price
                    results["logic"].append(f"{promo_type}: 受was_price折扣要求限制")
            
            # T30含促销价要求
            if rule.get("t30_promo_requirement") and discount_price > t30_lowest_price_with_promo:
                discount_price = t30_lowest_price_with_promo
                results["logic"].append(f"{promo_type}: 受T30含促销价限制")
            
            min_promo_price = min(min_promo_price, discount_price)
            results["logic"].append(f"{promo_type}: 建议价格 ${discount_price:.2f}")
    
    results["promoMaxPrice"] = min_promo_price
    return results

# 单个ASIN查询
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        asin = st.text_input("ASIN", placeholder="输入ASIN")
        historical_price = st.number_input("历史售价 ($)", min_value=0.0, step=0.01)
        rating = st.number_input("评分", min_value=0.0, max_value=5.0, step=0.1)
        vrp = st.number_input("VRP ($)", min_value=0.0, step=0.01)
        t30_lowest_price = st.number_input("T30最低价 ($)", min_value=0.0, step=0.01)
        t30_lowest_price_with_promo = st.number_input("含促销T30最低价 ($)", min_value=0.0, step=0.01)
    
    with col2:
        market = st.selectbox("市场", ["US", "CA"])
        promo_type = st.selectbox("促销计划", ["with", "without"])
        promo_period = st.selectbox("促销时期", ["regular", "major"])
        promo_start_date = st.date_input("促销开始时间")
        promo_end_date = st.date_input("促销结束时间")
    
    st.subheader("促销类型 (可多选)")
    promo_options = {
        "manualBestDeal": "顶级促销",
        "selfServiceBestDeal": "Z划算", 
        "lightningDeal": "秒杀",
        "primeExclusive": "Prime专享折扣",
        "priceDiscount": "价格折扣",
        "coupon": "优惠券"
    }
    
    selected_promos = []
    cols = st.columns(3)
    for i, (key, label) in enumerate(promo_options.items()):
        with cols[i % 3]:
            if st.checkbox(label, key=f"single_{key}"):
                selected_promos.append(key)
    
    if st.button("生成价格规划", type="primary"):
        if asin and historical_price and vrp and t30_lowest_price:
            rules = PROMO_RULES[market][promo_period]
            results = calculate_pricing(historical_price, vrp, t30_lowest_price, t30_lowest_price_with_promo, selected_promos, rules)
            
            st.markdown('<div class="results-section">', unsafe_allow_html=True)
            st.subheader("90天价格建议")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>活动前最高可设价格</h4>
                    <div class="price-highlight">${results['prePromoMaxPrice']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>活动期间最高可设价格</h4>
                    <div class="price-highlight" style="color: #28a745;">${results['promoMaxPrice']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>活动后建议价格</h4>
                    <div class="price-highlight" style="color: #007bff;">${results['postPromoPrice']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.subheader("价格建议逻辑")
            for logic in results["logic"]:
                st.write(f"• {logic}")
            
            # 图表数据
            dates = [datetime.now() + timedelta(days=i) for i in range(90)]
            chart_data = []
            
            for date in dates:
                if promo_start_date <= date.date() <= promo_end_date:
                    price = results["promoMaxPrice"]
                elif date.date() > promo_end_date:
                    price = results["postPromoPrice"]
                else:
                    price = results["prePromoMaxPrice"]
                chart_data.append({"日期": date.strftime("%Y-%m-%d"), "建议价格": price})
            
            chart_df = pd.DataFrame(chart_data)
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("90天价格趋势图")
            st.line_chart(chart_df.set_index("日期"))
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error("请填写所有必填字段")

# 批量ASIN处理
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        batch_market = st.selectbox("市场", ["US", "CA"], key="batch_market")
        batch_promo_period = st.selectbox("促销时期", ["regular", "major"], key="batch_promo_period")
    
    with col2:
        batch_promo_start_date = st.date_input("促销开始时间", key="batch_start")
        batch_promo_end_date = st.date_input("促销结束时间", key="batch_end")
    
    st.subheader("促销类型 (可多选)")
    batch_selected_promos = []
    cols = st.columns(3)
    for i, (key, label) in enumerate(promo_options.items()):
        with cols[i % 3]:
            if st.checkbox(label, key=f"batch_{key}"):
                batch_selected_promos.append(key)
    
    # 模板下载功能
    st.subheader("📥 下载批量上传模板")
    
    # 创建模板数据
    template_data = {
        'ASIN': ['B08N5WRWNW'],
        '历史售价': [27.99],
        '评分': [4.5],
        'VRP': [29.99],
        'T30最低价': [25.99],
        '含促销T30最低价': [23.99]
    }
    template_df = pd.DataFrame(template_data)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        csv_template = template_df.to_csv(index=False)
        st.download_button(
            label="📄 下载CSV模板",
            data=csv_template,
            file_name="amazon_pricing_template.csv",
            mime="text/csv",
            help="下载包含示例数据的CSV模板文件"
        )
    
    with col2:
        st.info("💡 模板包含示例数据，请按照格式填写您的ASIN信息")
    
    # 文件上传
    st.subheader("📤 上传填写完成的文件")
    uploaded_file = st.file_uploader("选择文件上传", type=['csv'], help="请上传按模板格式填写的CSV文件")
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ 文件上传成功！共读取到 {len(df)} 条ASIN数据")
            
            st.subheader("📋 数据预览")
            st.dataframe(df, use_container_width=True)
            
            if st.button("🚀 生成价格规划", type="primary", use_container_width=True):
                if not batch_selected_promos:
                    st.warning("⚠️ 请至少选择一种促销类型")
                else:
                    rules = PROMO_RULES[batch_market][batch_promo_period]
                    results_list = []
                    
                    # 显示进度条
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, row in df.iterrows():
                        # 更新进度
                        progress = (i + 1) / len(df)
                        progress_bar.progress(progress)
                        status_text.text(f'正在处理第 {i+1}/{len(df)} 个ASIN...')
                        
                        asin = row.get('ASIN', f'ASIN_{i+1}')
                        historical_price = float(row.get('历史售价', 27.99))
                        rating = float(row.get('评分', 4.5))
                        vrp = float(row.get('VRP', 29.99))
                        t30_lowest = float(row.get('T30最低价', 25.99))
                        t30_lowest_with_promo = float(row.get('含促销T30最低价', 23.99))
                        
                        pricing = calculate_pricing(historical_price, vrp, t30_lowest, t30_lowest_with_promo, batch_selected_promos, rules)
                        
                        results_list.append({
                            'ASIN': asin,
                            '历史售价': f"${historical_price:.2f}",
                            '评分': rating,
                            'VRP': f"${vrp:.2f}",
                            'T30最低价': f"${t30_lowest:.2f}",
                            '含促销T30最低价': f"${t30_lowest_with_promo:.2f}",
                            '活动类型': ', '.join(batch_selected_promos),
                            '活动时间': f"{batch_promo_start_date} 至 {batch_promo_end_date}",
                            '活动前建议价格': f"${pricing['prePromoMaxPrice']:.2f}",
                            '活动中建议价格': f"${pricing['promoMaxPrice']:.2f}",
                            '活动后建议价格': f"${pricing['postPromoPrice']:.2f}",
                            '价格建议逻辑': '; '.join(pricing['logic'])
                        })
                    
                    # 清除进度条
                    progress_bar.empty()
                    status_text.empty()
                    
                    results_df = pd.DataFrame(results_list)
                    
                    st.markdown('<div class="results-section">', unsafe_allow_html=True)
                    st.subheader("📊 批量处理结果")
                    
                    # 显示统计信息
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("处理ASIN数量", len(results_df))
                    with col2:
                        avg_promo_price = results_df['活动中建议价格'].str.replace('$', '').astype(float).mean()
                        st.metric("平均活动价格", f"${avg_promo_price:.2f}")
                    with col3:
                        min_promo_price = results_df['活动中建议价格'].str.replace('$', '').astype(float).min()
                        st.metric("最低活动价格", f"${min_promo_price:.2f}")
                    with col4:
                        max_promo_price = results_df['活动中建议价格'].str.replace('$', '').astype(float).max()
                        st.metric("最高活动价格", f"${max_promo_price:.2f}")
                    
                    # 显示结果表格
                    st.subheader("📋 详细结果预览")
                    st.dataframe(results_df, use_container_width=True)
                    
                    # 下载按钮
                    col1, col2 = st.columns(2)
                    with col1:
                        csv_result = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 下载完整结果 (CSV)",
                            data=csv_result,
                            file_name=f"amazon_pricing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col2:
                        # 创建简化版结果
                        simple_results = results_df[['ASIN', '活动前建议价格', '活动中建议价格', '活动后建议价格']].copy()
                        csv_simple = simple_results.to_csv(index=False)
                        st.download_button(
                            label="📥 下载简化结果 (CSV)",
                            data=csv_simple,
                            file_name=f"amazon_pricing_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"❌ 文件处理错误: {str(e)}")
            st.info("💡 请确保文件格式正确，包含所需的列：ASIN, 历史售价, 评分, VRP, T30最低价, 含促销T30最低价")
