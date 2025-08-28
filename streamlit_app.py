import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io

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
    .css-1d391kg { padding-top: 1rem; }
    
    .help-card {
        background: rgba(255,255,255,0.95);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    .metric-card {
        background: rgba(255,255,255,0.9);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .price-highlight {
        font-size: 24px;
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# 促销规则配置
PROMO_RULES = {
    "US": {
        "regular": {
            "manualBestDeal": {"discount": 20, "t30Requirement": True, "historicalRequirement": True},
            "selfServiceBestDeal": {"discount": 10, "t30Requirement": True, "historicalRequirement": True},
            "lightningDeal": {"discount": 15, "t30Requirement": True, "historicalRequirement": True},
            "priceDiscount": {"discount": 5, "t30Requirement": True, "currentPriceRequirement": True},
            "primeExclusive": {"discount": 5, "t30Requirement": True, "currentPriceRequirement": True},
            "coupon": {"discount": 5, "maxDiscount": 50, "historicalRequirement": True, "maxHistoricalIncrease": 30}
        },
        "major": {
            "manualBestDeal": {"discount": 30, "t30Requirement": True, "historicalRequirement": 5},
            "selfServiceBestDeal": {"discount": 15, "t30Requirement": True, "historicalRequirement": 5},
            "lightningDeal": {"discount": 20, "t30Requirement": True, "historicalRequirement": 5},
            "priceDiscount": {"discount": 5, "t30Requirement": True, "currentPriceRequirement": True},
            "primeExclusive": {"discount": 15, "t30Requirement": True, "historicalRequirement": 5},
            "coupon": {"discount": 5, "maxDiscount": 50, "historicalRequirement": True, "maxHistoricalIncrease": 30}
        }
    },
    "CA": {
        "regular": {
            "manualBestDeal": {"discount": 20, "t30Requirement": True, "historicalRequirement": True},
            "selfServiceBestDeal": {"discount": 10, "t30Requirement": True, "historicalRequirement": True},
            "lightningDeal": {"discount": 15, "t30Requirement": True, "historicalRequirement": True},
            "priceDiscount": {"discount": 5, "t30Requirement": True, "currentPriceRequirement": True},
            "primeExclusive": {"discount": 5, "t30Requirement": True, "currentPriceRequirement": True},
            "coupon": {"discount": 5, "maxDiscount": 50, "historicalRequirement": True}
        },
        "major": {
            "manualBestDeal": {"discount": 30, "t30Requirement": True, "historicalRequirement": 5},
            "selfServiceBestDeal": {"discount": 15, "t30Requirement": True, "historicalRequirement": 5},
            "lightningDeal": {"discount": 20, "t30Requirement": True, "historicalRequirement": 5},
            "priceDiscount": {"discount": 5, "t30Requirement": True, "currentPriceRequirement": True},
            "primeExclusive": {"discount": 15, "t30Requirement": True, "historicalRequirement": 5},
            "coupon": {"discount": 5, "maxDiscount": 50, "historicalRequirement": True}
        }
    }
}

# 使用说明弹窗
if 'show_help' not in st.session_state:
    st.session_state.show_help = True

if st.session_state.show_help:
    with st.container():
        st.markdown("""
        <div class="help-card">
            <h2 style="color: #667eea;">📖 价格计算工具使用说明</h2>
            
            <h3 style="color: #764ba2;">📖 功能简介</h3>
            <ul>
                <li>快速计算商品活动前价格要求，并给出价格策略建议</li>
                <li>支持单条计算和批量导入/导出</li>
                <li>支持CSV和XLSX格式</li>
                <li>支持实时可视化结果</li>
            </ul>
            
            <h3 style="color: #764ba2;">🚀 使用方法</h3>
            <ol>
                <li><strong>单条计算</strong>：在对应输入框中输入参数，点击计算，查看计算结果和操作建议</li>
                <li><strong>批量导入/导出</strong>：下载模板，填写后上传，查看计算结果和操作建议</li>
            </ol>
            
            <h3 style="color: #764ba2;">💡 提示</h3>
            <ul>
                <li>所有数据仅在当前会话有效</li>
                <li>支持导出计算结果</li>
                <li>此工具仅作为价格推算参考，实际价格要求以卖家后台为准</li>
            </ul>
            
            <hr>
            <p style="text-align: center; color: #888;">© 版权所有：SL Merchandising Team + Liya Liang</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("关闭说明", key="close_help"):
            st.session_state.show_help = False
            st.rerun()

# 主标题
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(102,126,234,0.9), rgba(118,75,162,0.9)); 
            color: white; padding: 40px; border-radius: 20px; text-align: center; 
            box-shadow: 0 25px 50px rgba(0,0,0,0.2); backdrop-filter: blur(20px); 
            border: 1px solid rgba(255,255,255,0.2); margin-bottom: 30px;">
    <h1 style="margin: 0; font-size: 2.5em; font-weight: 300;">亚马逊价格规划看板</h1>
    <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">专业的促销价格规划工具</p>
</div>
""", unsafe_allow_html=True)

# 标签页
tab1, tab2 = st.tabs(["🔍 单个ASIN查询", "📊 批量ASIN处理"])

def calculate_pricing(historical_price, vrp, t30_lowest_price, t30_lowest_price_with_promo, selected_types, rules):
    results = {
        "prePromoMaxPrice": vrp * 0.95,
        "promoMaxPrice": 0,
        "postPromoPrice": vrp * 0.95,
        "logic": []
    }
    
    if not selected_types:
        results["promoMaxPrice"] = vrp
        results["logic"].append("无促销活动，建议保持VRP价格")
    else:
        min_promo_price = vrp
        
        for promo_type in selected_types:
            if promo_type in rules:
                rule = rules[promo_type]
                calculated_price = vrp * (1 - rule["discount"] / 100)
                
                if rule.get("t30Requirement") and calculated_price > t30_lowest_price:
                    calculated_price = t30_lowest_price
                
                if rule.get("historicalRequirement") and calculated_price > historical_price * 0.95:
                    calculated_price = historical_price * 0.95
                
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
            results = calculate_pricing(historical_price, vrp, t30_lowest_price, t30_lowest_price_with_promo, selected_promos, rules)
            
            # 显示结果
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
            
            # 价格建议逻辑
            st.subheader("价格建议逻辑")
            for logic in results["logic"]:
                st.write(f"• {logic}")
            
            # 90天价格趋势图
            dates = [datetime.now() + timedelta(days=i) for i in range(90)]
            prices = []
            
            for date in dates:
                if promo_start_date <= date.date() <= promo_end_date:
                    prices.append(results["promoMaxPrice"])
                elif date.date() > promo_end_date:
                    prices.append(results["postPromoPrice"])
                else:
                    prices.append(results["prePromoMaxPrice"])
            
            # 使用matplotlib创建图表
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(dates, prices, color='#667eea', linewidth=3, marker='o', markersize=2)
            ax.fill_between(dates, prices, alpha=0.3, color='#667eea')
            ax.set_title('90天价格趋势图', fontsize=16, fontweight='bold')
            ax.set_xlabel('日期')
            ax.set_ylabel('价格 ($)')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            st.pyplot(fig)
        else:
            st.error("请填写所有必填字段")

# 批量ASIN处理
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        batch_market = st.selectbox("市场", ["US", "CA"], key="batch_market")
        batch_promo_type = st.selectbox("促销计划", ["with", "without"], key="batch_promo_type")
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
    
    # 文件上传
    uploaded_file = st.file_uploader("上传Excel文件", type=['csv', 'xlsx'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
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
                    
                    pricing = calculate_pricing(historical_price, vrp, t30_lowest, t30_lowest, batch_selected_promos, rules)
                    
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
                
                st.subheader("批量处理结果")
                st.dataframe(results_df)
                
                # 下载结果
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="下载结果",
                    data=csv,
                    file_name="amazon_pricing_results.csv",
                    mime="text/csv"
                )
                
        except Exception as e:
            st.error(f"文件处理错误: {str(e)}")

# 右上角帮助按钮
if not st.session_state.show_help:
    if st.button("📖 使用说明", key="show_help_btn"):
        st.session_state.show_help = True
        st.rerun()
