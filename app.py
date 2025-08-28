import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 页面配置
st.set_page_config(
    page_title="Seller Interview Analysis Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    .challenge-card {
        background: #fff5f5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #e53e3e;
        margin: 0.5rem 0;
    }
    .solution-card {
        background: #f0fff4;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #38a169;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 主标题
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Seller Interview Analysis Dashboard</h1>
        <p>Deep Insights from 6 Sellers Across Different Markets & Categories</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.selectbox(
        "Choose Analysis View",
        ["Overview", "Market Analysis", "Category Insights", "Requirements", "Recommendations"]
    )
    
    if page == "Overview":
        show_overview()
    elif page == "Market Analysis":
        show_market_analysis()
    elif page == "Category Insights":
        show_category_insights()
    elif page == "Requirements":
        show_requirements()
    elif page == "Recommendations":
        show_recommendations()

def show_overview():
    st.header("📈 Interview Overview")
    
    # 统计指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #3498db; margin: 0;">6</h2>
            <p style="margin: 0;">Interviewed Sellers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #3498db; margin: 0;">3</h2>
            <p style="margin: 0;">Target Markets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #3498db; margin: 0;">3</h2>
            <p style="margin: 0;">Main Categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #3498db; margin: 0;">9</h2>
            <p style="margin: 0;">Core Questions</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 分布图表
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Market Distribution")
        market_data = {"Market": ["US", "EU", "JP"], "Count": [4, 1, 1]}
        fig = px.pie(market_data, values="Count", names="Market", 
                    color_discrete_sequence=["#3498db", "#e74c3c", "#f39c12"])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Category Distribution")
        category_data = {"Category": ["Apparel", "Luggage", "Shoes"], "Count": [3, 2, 1]}
        fig = px.bar(category_data, x="Category", y="Count",
                    color="Category", color_discrete_sequence=["#e74c3c", "#27ae60", "#f39c12"])
        st.plotly_chart(fig, use_container_width=True)

def show_market_analysis():
    st.header("🌍 Market-Specific Analysis")
    
    market = st.selectbox("Select Market", ["All Markets", "US Market", "EU Market", "JP Market"])
    
    if market == "US Market" or market == "All Markets":
        st.subheader("🇺🇸 US Market Challenges")
        st.markdown("""
        <div class="challenge-card">
            <h4>Supply Chain & Return Rate Issues</h4>
            <p>• Insufficient supply chain capabilities<br>
            • High return rates in apparel affecting profitability<br>
            • Sizing and quality issues prominent</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="challenge-card">
            <h4>Operational Security Risks</h4>
            <p>• Frequent competitor attacks and hijacking<br>
            • Listing stability issues<br>
            • Slow appeal process efficiency</p>
        </div>
        """, unsafe_allow_html=True)
    
    if market == "EU Market" or market == "All Markets":
        st.subheader("🇪🇺 EU Market Challenges")
        st.markdown("""
        <div class="challenge-card">
            <h4>Consumer Downgrade Impact</h4>
            <p>• High-price products facing weak demand<br>
            • Premium positioning vs market share loss<br>
            • Brand strategy under pressure</p>
        </div>
        """, unsafe_allow_html=True)
    
    if market == "JP Market" or market == "All Markets":
        st.subheader("🇯🇵 JP Market Challenges")
        st.markdown("""
        <div class="challenge-card">
            <h4>Price Competition Pressure</h4>
            <p>• Low-price products emerging in BSR<br>
            • Forced price reduction affecting profits<br>
            • Difficulty in traffic acquisition</p>
        </div>
        """, unsafe_allow_html=True)

def show_category_insights():
    st.header("📦 Category-Specific Insights")
    
    category = st.selectbox("Select Category", ["All Categories", "Apparel", "Luggage", "Shoes"])
    
    if category == "Apparel" or category == "All Categories":
        st.subheader("👕 Apparel Category")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="challenge-card">
                <h4>Key Challenges</h4>
                <p>• High return rates (sizing issues)<br>
                • Need for local customer feedback<br>
                • Product testing requirements</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="solution-card">
                <h4>Specific Needs</h4>
                <p>• Pre-launch testing platform<br>
                • Local fit testing mechanisms<br>
                • Size optimization tools</p>
            </div>
            """, unsafe_allow_html=True)
    
    if category == "Luggage" or category == "All Categories":
        st.subheader("🧳 Luggage Category")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="challenge-card">
                <h4>Key Challenges</h4>
                <p>• Brand positioning pressure<br>
                • Price competition<br>
                • Premium market focus</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="solution-card">
                <h4>Specific Needs</h4>
                <p>• Brand share monitoring<br>
                • Premium customer analysis<br>
                • Market positioning guidance</p>
            </div>
            """, unsafe_allow_html=True)

def show_requirements():
    st.header("🎯 Core Requirements Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Product Intelligence", "Operational Security", "Traffic & Promotion", "AI & Automation"])
    
    with tab1:
        st.subheader("🔍 Product Intelligence & Testing")
        st.markdown("""
        <div class="solution-card">
            <h4>Local Customer Profiling</h4>
            <p>• Precise audience analysis and preference insights<br>
            • Keyword review and analysis for paid sellers<br>
            • Category-specific customer portraits</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="solution-card">
            <h4>Pre-Launch Testing Platform</h4>
            <p>• Local customer feedback collection mechanism<br>
            • Product optimization before official launch<br>
            • Real customer testing and feedback</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("🛡️ Operational Security & Stability")
        st.markdown("""
        <div class="solution-card">
            <h4>Anti-Hijacking Protection</h4>
            <p>• Whitelist review mechanism<br>
            • Proactive product protection<br>
            • Prevention of malicious attacks</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="solution-card">
            <h4>Fast-Track Appeal Process</h4>
            <p>• Green channel for paid sellers<br>
            • Expedited processing for critical listings<br>
            • Dedicated support escalation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("📈 Traffic & Promotion Optimization")
        st.markdown("""
        <div class="solution-card">
            <h4>Traffic Support</h4>
            <p>• Additional traffic channels for specific categories<br>
            • Enhanced promotional opportunities<br>
            • Category-specific traffic allocation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("🤖 AI & Automation")
        st.markdown("""
        <div class="solution-card">
            <h4>AI-Powered Solutions</h4>
            <p>• Automated advertising optimization<br>
            • Content optimization and translation<br>
            • Performance analysis and insights</p>
        </div>
        """, unsafe_allow_html=True)

def show_recommendations():
    st.header("💡 Strategic Recommendations")
    
    st.subheader("🎯 Market-Specific Service Packages")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="solution-card">
            <h4>🇪🇺 EU Brand Package</h4>
            <p><strong>Focus:</strong> Brand Protection<br><br>
            • Brand share monitoring<br>
            • Premium consumer insights<br>
            • Global expansion guidance<br>
            • Competitive analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-card">
            <h4>🇯🇵 JP Localization Package</h4>
            <p><strong>Focus:</strong> Local Market Fit<br><br>
            • Japanese consumer profiling<br>
            • DOTD promotion priority<br>
            • Localized product guidance<br>
            • Cultural adaptation support</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="solution-card">
            <h4>🇺🇸 US Operations Package</h4>
            <p><strong>Focus:</strong> Operational Excellence<br><br>
            • Listing security protection<br>
            • Return rate optimization<br>
            • Fast inventory processing<br>
            • Operational best practices</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("🚀 Innovation Opportunities")
    
    innovations = [
        {
            "title": "Testing Platform",
            "description": "Local customer testing and feedback mechanism for apparel sellers",
            "impact": "High",
            "effort": "Medium"
        },
        {
            "title": "AI Ad Management",
            "description": "Automated advertising optimization and bidding strategies",
            "impact": "High",
            "effort": "High"
        },
        {
            "title": "Whitelist Protection",
            "description": "Proactive product review for paid sellers to prevent attacks",
            "impact": "Medium",
            "effort": "Low"
        },
        {
            "title": "Green Appeal Channel",
            "description": "Fast-track appeal process for critical listing issues",
            "impact": "Medium",
            "effort": "Low"
        }
    ]
    
    for innovation in innovations:
        st.markdown(f"""
        <div class="solution-card">
            <h4>{innovation['title']}</h4>
            <p>{innovation['description']}</p>
            <p><strong>Impact:</strong> {innovation['impact']} | <strong>Effort:</strong> {innovation['effort']}</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
