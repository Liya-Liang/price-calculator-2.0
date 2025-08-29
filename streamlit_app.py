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

# 自定义CSS
st.markdown("""
<style>
    .main { padding-top: 0rem; }
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    
    /* 右上角按钮样式 */
    .top-buttons {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .top-btn {
        background: linear-gradient(135deg, #ff9900, #ff7700);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(255,153,0,0.3);
        font-weight: bold;
        text-decoration: none;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .top-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,153,0,0.4);
    }
    
    /* 弹窗样式 */
    .modal-overlay {
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
    }
    
    .modal-content {
        background: white;
        padding: 40px;
        border-radius: 20px;
        max-width: 600px;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        position: relative;
    }
    
    .close-btn {
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 24px;
        cursor: pointer;
        color: #999;
    }
    
    .close-btn:hover {
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# 促销规则配置
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

# 状态管理
if 'show_help' not in st.session_state:
    st.session_state.show_help = True
if 'show_calendar' not in st.session_state:
    st.session_state.show_calendar = False

# 右上角按钮
buttons_html = '<div class="top-buttons">'
if not st.session_state.show_help:
    buttons_html += '<div class="top-btn" onclick="showHelp()">📖 使用说明</div>'
if not st.session_state.show_calendar:
    buttons_html += '<div class="top-btn" onclick="showCalendar()">📅 促销日历</div>'
buttons_html += '</div>'

st.markdown(buttons_html, unsafe_allow_html=True)

# 使用说明弹窗
if st.session_state.show_help:
    st.markdown("""
    <div class="modal-overlay" onclick="closeHelp()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="close-btn" onclick="closeHelp()">✕</div>
            <h2 style="color: #667eea; margin-bottom: 30px; text-align: center;">
                📖 价格计算工具使用说明
            </h2>
            
            <h3 style="color: #667eea;">📖 功能简介</h3>
            <ul style="line-height: 1.8;">
                <li>快速计算商品活动前价格要求，并给出价格策略建议</li>
                <li>支持单条计算和批量导入/导出</li>
                <li>支持CSV和XLSX格式</li>
                <li>支持实时可视化结果</li>
            </ul>
            
            <h3 style="color: #764ba2;">🚀 使用方法</h3>
            <ol style="line-height: 1.8;">
                <li><strong>单条计算</strong>：在对应输入框中输入参数，点击计算，查看计算结果和操作建议</li>
                <li><strong>批量导入/导出</strong>：下载模板，填写后上传，查看计算结果和操作建议，可直接线上查看结果也可批量下载结果</li>
            </ol>
            
            <h3 style="color: #e67e22;">💡 提示</h3>
            <ul style="line-height: 1.8;">
                <li>所有数据仅在当前会话有效</li>
                <li>支持导出计算结果</li>
                <li style="color: #e74c3c; font-weight: 600;">此工具仅作为价格推算参考，实际价格要求以卖家后台为准</li>
            </ul>
            
            <hr style="margin: 25px 0; border: none; border-top: 2px solid #eee;">
            <p style="text-align: center; color: #888; margin: 0;">
                © 版权所有：SL merchandising team + Liya Liang
            </p>
        </div>
    </div>
    
    <script>
    function closeHelp() {
        document.querySelector('[data-testid="close_help_btn"]').click();
    }
    function showHelp() {
        document.querySelector('[data-testid="show_help_btn"]').click();
    }
    </script>
    """, unsafe_allow_html=True)
    
    if st.button("", key="close_help_btn"):
        st.session_state.show_help = False
        st.rerun()

# 促销日历弹窗
if st.session_state.show_calendar:
    calendar_content = """
    <div class="modal-overlay" onclick="closeCalendar()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="close-btn" onclick="closeCalendar()">✕</div>
            <h2 style="color: #667eea; margin-bottom: 30px; text-align: center;">
                📅 2025年大促日历
            </h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                <div>
                    <h3 style="color: #764ba2;">🇺🇸 美国站</h3>
    """
    
    for event in MAJOR_SALES_CALENDAR["US"]:
        calendar_content += f'<p><strong>{event["name"]}</strong><br>{event["start"]} 至 {event["end"]}</p>'
    
    calendar_content += """
                </div>
                <div>
                    <h3 style="color: #764ba2;">🇨🇦 加拿大站</h3>
    """
    
    for event in MAJOR_SALES_CALENDAR["CA"]:
        calendar_content += f'<p><strong>{event["name"]}</strong><br>{event["start"]} 至 {event["end"]}</p>'
    
    calendar_content += """
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function closeCalendar() {
        document.querySelector('[data-testid="close_calendar_btn"]').click();
    }
    function showCalendar() {
        document.querySelector('[data-testid="show_calendar_btn"]').click();
    }
    </script>
    """
    
    st.markdown(calendar_content, unsafe_allow_html=True)
    
    if st.button("", key="close_calendar_btn"):
        st.session_state.show_calendar = False
        st.rerun()

# 隐藏的按钮用于JavaScript调用
if not st.session_state.show_help:
    if st.button("", key="show_help_btn"):
        st.session_state.show_help = True
        st.rerun()

if not st.session_state.show_calendar:
    if st.button("", key="show_calendar_btn"):
        st.session_state.show_calendar = True
        st.rerun()

# 主标题
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(102,126,234,0.9), rgba(118,75,162,0.9)); 
            color: white; padding: 40px; border-radius: 20px; text-align: center; 
            box-shadow: 0 25px 50px rgba(0,0,0,0.2); margin-bottom: 30px;">
    <h1 style="margin: 0; font-size: 2.5em; font-weight: 300;">亚马逊价格规划看板</h1>
    <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">专业的促销价格规划工具</p>
</div>
""", unsafe_allow_html=True)

# 计算函数
def validate_promo_types(selected_types):
    exclusive_types = ['manualBestDeal', 'selfServiceBestDeal', 'lightningDeal', 'priceDiscount', 'primeExclusive']
    selected_exclusive = [t for t in selected_types if t in exclusive_types]
    has_coupon = 'coupon' in selected_types
    
    if len(selected_exclusive) > 1:
        return {"valid": False, "message": "禁止：顶级促销、Z划算、秒杀、Prime专享折扣、价格折扣不能同时选择"}
    
    if has_coupon and len(selected_exclusive) > 0:
        return {"valid": True, "message": "价格将会叠加：优惠券与其他促销类型叠加计算"}
    
    return {"valid": True, "message": ""}

def calculate_stacked_discount(selected_types, vrp):
    exclusive_types = ['manualBestDeal', 'selfServiceBestDeal', 'lightningDeal', 'priceDiscount', 'primeExclusive']
    selected_exclusive = [t for t in selected_types if t in exclusive_types]
    has_coupon = 'coupon' in selected_types
    
    if not has_coupon:
        return 0
    
    coupon_discount = 0.25
    
    if any(t in ['manualBestDeal', 'selfServiceBestDeal', 'lightningDeal'] for t in selected_exclusive):
        total_discount = 0.45
    elif any(t in ['primeExclusive', 'priceDiscount'] for t in selected_exclusive):
        total_discount = 0.475
    else:
        total_discount = coupon_discount
    
    return vrp * (1 - total_discount)

def calculate_pricing(historical_price, vrp, t30_lowest_price, t30_lowest_price_with_promo, selected_types, rules):
    results = {
        "prePromoMaxPrice": vrp * 0.95,
        "promoMaxPrice": vrp,
        "postPromoPrice": vrp * 0.95,
        "logic": []
    }
    
    if not selected_types:
        results["logic"].append("无促销活动，建议保持VRP价格")
        return results
    
    validation = validate_promo_types(selected_types)
    if not validation["valid"]:
        results["logic"].append(f"错误：{validation['message']}")
        return results
    
    if validation["message"]:
        results["logic"].append(validation["message"])
    
    if 'coupon' in selected_types and len([t for t in selected_types if t in ['manualBestDeal', 'selfServiceBestDeal', 'lightningDeal', 'priceDiscount', 'primeExclusive']]) > 0:
        stacked_price = calculate_stacked_discount(selected_types, vrp)
        results["promoMaxPrice"] = stacked_price
        results["logic"].append(f"叠加计算后最终价格: ${stacked_price:.2f}")
        return results
    
    min_promo_price = vrp
    
    for promo_type in selected_types:
        if promo_type not in rules:
            continue
            
        rule = rules[promo_type]
        
        if promo_type == 'coupon':
            discount_price = vrp * 0.75
            
            if rule.get("was_price_requirement") and discount_price >= historical_price:
                discount_price = historical_price * 0.95
            
            if rule.get("was_price_max_increase"):
                max_current_price = historical_price * (1 + rule["was_price_max_increase"] / 100)
                if vrp > max_current_price:
                    results["logic"].append(f"警告：当前价格超过was_price的{rule['was_price_max_increase']}%限制")
            
            min_promo_price = min(min_promo_price, discount_price)
            results["logic"].append(f"优惠券: 建议价格 ${discount_price:.2f}")
            
        else:
            discount_price = vrp * (1 - rule["discount"] / 100)
            
            if rule.get("hamp_net_requirement") and discount_price > t30_lowest_price:
                discount_price = t30_lowest_price
                results["logic"].append(f"{promo_type}: 受HAMP Net Price限制")
            
            if rule.get("was_price_requirement") and discount_price >= historical_price:
                discount_price = historical_price * 0.95
                results["logic"].append(f"{promo_type}: 受was_price限制")
            
            if rule.get("was_price_discount"):
                required_price = historical_price * (1 - rule["was_price_discount"] / 100)
                if discount_price > required_price:
                    discount_price = required_price
                    results["logic"].append(f"{promo_type}: 受was_price折扣要求限制")
            
            if rule.get("t30_promo_requirement") and discount_price > t30_lowest_price_with_promo:
                discount_price = t30_lowest_price_with_promo
                results["logic"].append(f"{promo_type}: 受T30含促销价限制")
            
            min_promo_price = min(min_promo_price, discount_price)
            results["logic"].append(f"{promo_type}: 建议价格 ${discount_price:.2f}")
    
    results["promoMaxPrice"] = min_promo_price
    return results

# 标签页
tab1, tab2 = st.tabs(["🔍 单个ASIN查询", "📊 批量ASIN处理"])

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
            
            st.subheader("90天价格建议")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("活动前最高可设价格", f"${results['prePromoMaxPrice']:.2f}")
            with col2:
                st.metric("活动期间最高可设价格", f"${results['promoMaxPrice']:.2f}")
            with col3:
                st.metric("活动后建议价格", f"${results['postPromoPrice']:.2f}")
            
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
            st.subheader("90天价格趋势图")
            st.line_chart(chart_df.set_index("日期"))
            
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
    
    # 模板下载
    st.subheader("📥 下载批量上传模板")
    template_data = {
        'ASIN': ['B08N5WRWNW'],
        '历史售价': [27.99],
        '评分': [4.5],
        'VRP': [29.99],
        'T30最低价': [25.99],
        '含促销T30最低价': [23.99]
    }
    template_df = pd.DataFrame(template_data)
    
    csv_template = template_df.to_csv(index=False)
    st.download_button(
        label="📄 下载CSV模板",
        data=csv_template,
        file_name="amazon_pricing_template.csv",
        mime="text/csv"
    )
    
    # 文件上传
    st.subheader("📤 上传填写完成的文件")
    uploaded_file = st.file_uploader("选择文件上传", type=['csv'])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ 文件上传成功！共读取到 {len(df)} 条ASIN数据")
            st.dataframe(df, use_container_width=True)
            
            if st.button("🚀 生成价格规划", type="primary", use_container_width=True):
                if not batch_selected_promos:
                    st.warning("⚠️ 请至少选择一种促销类型")
                else:
                    rules = PROMO_RULES[batch_market][batch_promo_period]
                    results_list = []
                    
                    progress_bar = st.progress(0)
                    
                    for i, row in df.iterrows():
                        progress = (i + 1) / len(df)
                        progress_bar.progress(progress)
                        
                        asin = row.get('ASIN', f'ASIN_{i+1}')
                        historical_price = float(row.get('历史售价', 27.99))
                        vrp = float(row.get('VRP', 29.99))
                        t30_lowest = float(row.get('T30最低价', 25.99))
                        t30_lowest_with_promo = float(row.get('含促销T30最低价', 23.99))
                        
                        pricing = calculate_pricing(historical_price, vrp, t30_lowest, t30_lowest_with_promo, batch_selected_promos, rules)
                        
                        results_list.append({
                            'ASIN': asin,
                            '活动前建议价格': f"${pricing['prePromoMaxPrice']:.2f}",
                            '活动中建议价格': f"${pricing['promoMaxPrice']:.2f}",
                            '活动后建议价格': f"${pricing['postPromoPrice']:.2f}",
                            '价格建议逻辑': '; '.join(pricing['logic'])
                        })
                    
                    progress_bar.empty()
                    results_df = pd.DataFrame(results_list)
                    
                    st.subheader("📊 批量处理结果")
                    st.dataframe(results_df, use_container_width=True)
                    
                    csv_result = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 下载结果",
                        data=csv_result,
                        file_name=f"amazon_pricing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
        except Exception as e:
            st.error(f"❌ 文件处理错误: {str(e)}")
