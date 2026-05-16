import streamlit as st

# 1. 设置为宽屏模式，页面看起来更大气
st.set_page_config(
    page_title="COMM7780 | Media Analytics Dashboard",
    page_icon="👁️‍🗨️",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. 注入自定义 CSS 隐藏 Streamlit 默认的红线和菜单，提升“自研 App”的沉浸感
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* 优化顶部留白 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* 优化标题颜色与字体 */
    h1 {
        color: #2C3E50;
        font-weight: 800;
        letter-spacing: -1px;
    }
    h2, h3 {
        color: #34495E;
    }
    /* 给卡片加一点阴影效果的感觉 */
    div.stInfo {
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 头部视觉区
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("<h1 style='font-size: 75px; margin-top: -20px;'>📡</h1>", unsafe_allow_html=True)
with col2:
    st.title("Digital Resonance 👁️‍🗨️")
    st.markdown("### COMM7780: Big Data Analytics for Media and Communication")

st.markdown("---")

# 4. 核心文案区（学术感 + 逼格）
st.markdown("""
#### 📌 项目愿景 (Project Vision)
在算法驱动的 Web 2.0 时代，受众不再是沉默的接收者，而是情绪与数据的狂热生产者。本项目 (**Digital Resonance / 数字共振**) 摒弃了传统的静态学术报告，采用 **Python 实时抓取 + 大语言模型 (LLM) 语义降维** 的前沿技术，构建了一个**实时交互式的传媒数据洞察仪表盘**。

我们致力于透过海量且混沌的数字痕迹（Digital Footprints），透视数字时代下受众的**情绪传染 (Emotional Contagion)**、**群体极化 (Group Polarization)** 与 **寄生性社会关系 (Parasocial Interaction)**。
""")

st.write("") # 空行留白

# 5. 模块导航卡片区 (使用 Columns 并排展示，打破垂直单调)
col_a, col_b = st.columns(2)

with col_a:
    st.info("""
    #### 🎮 模块一：Steam 玩家傲娇指数雷达
    **研究视域：亚文化与硬核游戏社区**
    
    *   **核心逻辑**：打破“好评/差评”的二元对立，引入【游玩时长】这一行为变量。
    *   **洞察目标**：利用 LLM 挖掘玩家“口嫌体正直”（高时长 + 差评）背后的深层情绪痛点，透视游戏玩家特有的赛博发泄文化。
    *   👉 *请在左侧边栏点击进入测试*
    """)

with col_b:
    st.info("""
    #### 📺 模块二：YouTube 评论区 X 光机
    **研究视域：主流视频媒介与受众框架**
    
    *   **核心逻辑**：实时抽样热门视频的前排高赞评论，进行文本去噪。
    *   **洞察目标**：利用数字人类学视角，一键解剖评论区的情绪主基调、观点阵营划分，并洞察粉丝狂欢、信息茧房等典型传播学现象。
    *   👉 *请在左侧边栏点击进入测试*
    """)

st.markdown("---")
st.caption("👨‍💻 **Powered by:** Python | Streamlit | YouTube Data API v3 | Steamworks API | NVIDIA Llama-3.1-70B")
