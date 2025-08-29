import streamlit as st
import re
import pandas as pd
from docx import Document
from datetime import datetime, timedelta

# 页面配置
page_title = "亚马逊价格规划看板"
page_icon = "📊"
layout = "wide"
initial_sidebar_state = "collapsed"
st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
    initial_sidebar_state=initial_sidebar_state
)
def read_word_docx(doc_path):
    doc = Document(doc_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

word_file_path = '/home/guangfl/PricingTool2.0/edit 3.docx'
word_text = read_word_docx(word_file_path)
# 自动提取大促时间点（如：日期、节日等）
def extract_promo_dates(text):
    # 匹配常见日期格式（如2025-09-01、9月1日、9/1等）和节日关键词
    date_pattern = r'(\d{4}[年/-]\d{1,2}[月/-]\d{1,2}日?|\d{1,2}[月/-]\d{1,2}日?|\d{1,2}/\d{1,2})'
    festival_pattern = r'(Prime Day|黑五|网一|圣诞|感恩节|返校|新年|春节|618|双11|双12|Labor Day|Easter|Mother\'s Day|Father\'s Day)'
    matches = re.findall(f'{date_pattern}|{festival_pattern}', text)
    # 整理结果
    promo_dates = []
    for m in matches:
        date_str = ''.join(m)
        if date_str:
            promo_dates.append(date_str)
    return promo_dates

promo_dates = extract_promo_dates(word_text)

# 促销日历弹窗功能
if 'show_calendar' not in st.session_state:
    st.session_state['show_calendar'] = False

calendar_btn_col = st.columns([8,1])[1]
with calendar_btn_col:
    if st.button('促销日历', key='calendar_btn'):
        st.session_state['show_calendar'] = True
        st.rerun()

if st.session_state['show_calendar']:
    with st.container():
        st.markdown("""
        <div style='position:fixed;top:40px;right:40px;width:400px;z-index:9999;background:white;border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,0.18);padding:32px 24px 24px 24px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <h3 style='margin:0;'>促销日历</h3>
                <button onclick="window.location.reload()" style='background:none;border:none;font-size:22px;cursor:pointer;line-height:1;'>×</button>
            </div>
            <hr/>
            <ul style='padding-left:18px;'>
                {promo_items}
            </ul>
        </div>
        """.replace('{promo_items}', ''.join([f"<li style='margin-bottom:8px;font-size:16px;'>{d}</li>" for d in promo_dates])), unsafe_allow_html=True)

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

# 促销规则配置
PROMO_RULES = {
    "US": {
        "regular": {
            "manualBestDeal": {"discount": 20},
            "selfServiceBestDeal": {"discount": 10},
            "lightningDeal": {"discount": 15},
            "priceDiscount": {"discount": 5},
            "primeExclusive": {"discount": 5},
            "coupon": {"discount": 5}
        },
        "major": {
            "manualBestDeal": {"discount": 30},
            "selfServiceBestDeal": {"discount": 15},
            "lightningDeal": {"discount": 20},
            "priceDiscount": {"discount": 5},
            "primeExclusive": {"discount": 15},
            "coupon": {"discount": 5}
        }
    },
    "CA": {
        "regular": {
            "manualBestDeal": {"discount": 20},
            "selfServiceBestDeal": {"discount": 10},
            "lightningDeal": {"discount": 15},
            "priceDiscount": {"discount": 5},
            "primeExclusive": {"discount": 5},
            "coupon": {"discount": 5}
        },
        "major": {
            "manualBestDeal": {"discount": 30},
            "selfServiceBestDeal": {"discount": 15},
            "lightningDeal": {"discount": 20},
            "priceDiscount": {"discount": 5},
            "primeExclusive": {"discount": 15},
            "coupon": {"discount": 5}
        }
    }
}

# 使用说明
if 'show_help' not in st.session_state:
    st.session_state.show_help = True

# 顶部帮助按钮（当说明关闭时显示）
if not st.session_state.show_help:
    col1, col2, col3 = st.columns([6, 1, 1])
    with col2:
        if st.button("📖 使用说明", key="show_help_btn", help="点击查看使用说明"):
            st.session_state.show_help = True
            st.rerun()

if st.session_state.show_help:
    st.markdown("### 📖 价格计算工具使用说明")
    
    with st.container():
        st.markdown("#### 📖 功能简介")
        st.markdown("""
        - 快速计算商品活动前价格要求，并给出价格策略建议
        - 支持单条计算和批量导入/导出
        - 支持CSV和XLSX格式
        - 支持实时可视化结果
        """)
    
    with st.container():
        st.markdown("#### 🚀 使用方法")
        st.markdown("""
        1. **单条计算**：在对应输入框中输入参数，点击计算，查看计算结果和操作建议
        2. **批量导入/导出**：下载模板，填写后上传，查看计算结果和操作建议，可直接线上查看结果也可批量下载结果
        """)
    
    with st.container():
        st.markdown("#### 💡 提示")
        st.markdown("""
        - 所有数据仅在当前会话有效
        - 支持导出计算结果
        - **此工具仅作为价格推算参考，实际价格要求以卖家后台为准**
        """)
    
    st.divider()
    st.markdown("<p style='text-align: center; color: #888;'>© 版权所有：SL merchandising team + Liya Liang</p>", unsafe_allow_html=True)
    
    if st.button("关闭说明", key="close_help"):
        st.session_state.show_help = False
        st.rerun()

# 主标题
st.markdown("""
<div class="main-header">
    <h1>亚马逊价格规划看板</h1>
    <p>专业的促销价格规划工具</p>
</div>
""", unsafe_allow_html=True)

# 标签页
tab1, tab2 = st.tabs(["🔍 单个ASIN查询", "📊 批量ASIN处理"])

def calculate_pricing(historical_price, vrp, t30_lowest_price, selected_types, rules):
    results = {
        "prePromoMaxPrice": vrp * 0.95,
        "promoMaxPrice": vrp,
        "postPromoPrice": vrp * 0.95,
        "logic": []
    }
    
    if not selected_types:
        results["logic"].append("无促销活动，建议保持VRP价格")
    else:
        min_promo_price = vrp
        
        for promo_type in selected_types:
            if promo_type in rules:
                rule = rules[promo_type]
                calculated_price = vrp * (1 - rule["discount"] / 100)
                calculated_price = max(calculated_price, min(t30_lowest_price, historical_price * 0.95))
                min_promo_price = min(min_promo_price, calculated_price)
                results["logic"].append(f"{promo_type}: 建议价格 ${calculated_price:.2f}")
        
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
            results = calculate_pricing(historical_price, vrp, t30_lowest_price, selected_promos, rules)
            
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
    
    uploaded_file = st.file_uploader("上传CSV文件", type=['csv'])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("文件预览:")
            st.dataframe(df.head())
            
            if st.button("批量运算", type="primary"):
                rules = PROMO_RULES[batch_market][batch_promo_period]
                results_list = []
                
                for _, row in df.iterrows():
                    asin = row.get('ASIN', f'ASIN_{len(results_list)+1}')
                    historical_price = float(row.get('was_price', 27.99))
                    vrp = float(row.get('VRP', 29.99))
                    t30_lowest = float(row.get('HAMP Buybox Price', 25.99))
                    
                    pricing = calculate_pricing(historical_price, vrp, t30_lowest, batch_selected_promos, rules)
                    
                    results_list.append({
                        'ASIN': asin,
                        'HAMP Buybox Price': t30_lowest,
                        'VRP': vrp,
                        'was_price': historical_price,
                        '活动类型': ', '.join(batch_selected_promos),
                        '活动时间': f"{batch_promo_start_date} to {batch_promo_end_date}",
                        '活动前建议价格': f"${pricing['prePromoMaxPrice']:.2f}",
                        '活动中建议价格': f"${pricing['promoMaxPrice']:.2f}",
                        '活动后建议价格': f"${pricing['postPromoPrice']:.2f}"
                    })
                
                results_df = pd.DataFrame(results_list)
                
                st.markdown('<div class="results-section">', unsafe_allow_html=True)
                st.subheader("批量处理结果")
                st.dataframe(results_df)
                
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="下载结果",
                    data=csv,
                    file_name="amazon_pricing_results.csv",
                    mime="text/csv"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"文件处理错误: {str(e)}")
