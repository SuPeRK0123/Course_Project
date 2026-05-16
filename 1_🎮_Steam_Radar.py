import streamlit as st
import requests
import pandas as pd

# 【注意：请在这里替换你的真实 NVIDIA API KEY】
NVIDIA_API_KEY = "xxx"

# --- 页面全局配置 ---
st.set_page_config(page_title="Steam Radar", page_icon="🎮", layout="wide")

# 隐藏多余 UI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# --- 核心功能函数 ---
@st.cache_data(ttl=60) # 添加缓存机制，避免重复请求被限制
def get_steam_reviews(app_id, max_reviews=20):
    url = f"https://store.steampowered.com/appreviews/{app_id}"
    params = {'json': 1, 'language': 'schinese', 'filter': 'recent', 'num_per_page': max_reviews}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        reviews = response.json().get('reviews',[])
        formatted_text = ""
        raw_data =[] # 收集原始数据给 Pandas 用
        
        for i, review in enumerate(reviews):
            playtime = review.get('author', {}).get('playtime_forever', 0) / 60
            voted_up = review.get('voted_up')
            content = review.get('review', '').replace('\n', ' ')
            attitude = "👍 推荐" if voted_up else "👎 不推荐"
            
            formatted_text += f"评论 {i+1}: 态度: {attitude}, 游玩时长: {playtime:.1f} 小时, 内容: {content[:150]}\n"
            raw_data.append({
                "推荐状态": attitude, 
                "游玩时长(小时)": round(playtime, 1), 
                "是否好评": 1 if voted_up else 0, # 用于计算图表
                "评论内容": content
            })
            
        return formatted_text, pd.DataFrame(raw_data)
    return None, None

def analyze_reviews_with_llm(reviews_text):
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""
    你是一位毒舌且幽默的游戏传媒分析师。阅读以下Steam玩家评价数据，生成一份【游戏洞察报告】：
    1. 【核心痛点/爽点】：总结玩家在抱怨什么，或者在夸什么。
    2. 【傲娇指数分析】：结合游玩时长，指出是否有“口嫌体正直”（玩了很久却给差评）的现象。
    3. 【毒舌标语】：用一句话给这款游戏写一句犀利的吐槽标语。
    数据：
    {reviews_text}
    """
    payload = {"model": "meta/llama-3.1-70b-instruct", "messages":[{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 512}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return f"请求失败: {response.text}"

# --- UI 布局设计 ---
st.title("🎮 Steam 玩家傲娇指数雷达")
st.markdown("通过抓取近期玩家的**游玩时长**与**推荐状态**，结合 LLM 洞察硬核玩家的情绪特征。")
st.markdown("---")

GAMES = {"赛博朋克 2077": 1091500, "幻兽帕鲁 (Palworld)": 1623730, "绝地求生 (PUBG)": 578080, "黑神话：悟空": 2358720, "Apex 英雄": 1172470}

# 1. 侧边栏控制台
with st.sidebar:
    st.header("🎛️ 控制台 (Console)")
    selected_game_name = st.selectbox("👉 选择分析目标：", list(GAMES.keys()))
    app_id = GAMES[selected_game_name]
    sample_size = st.slider("抓取样本数量", min_value=10, max_value=50, value=20, step=10)
    start_btn = st.button("🚀 启动实时分析", use_container_width=True, type="primary")

# 2. 主展示区
if start_btn:
    with st.spinner(f'正在从 Steam 接口抓取《{selected_game_name}》的最新数据...'):
        reviews_text, df = get_steam_reviews(app_id, max_reviews=sample_size)
        
    if df is not None and not df.empty:
        # --- 核心指标 KPI ---
        avg_playtime = df['游玩时长(小时)'].mean()
        positive_rate = df['是否好评'].mean() * 100
        longest_play = df['游玩时长(小时)'].max()
        
        st.subheader("📊 实时数据看板 (Data Dashboard)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="抓取样本总数", value=f"{len(df)} 条")
        col2.metric(label="玩家平均游玩时长", value=f"{avg_playtime:.1f} hrs")
        col3.metric(label="单人最长游玩纪录", value=f"{longest_play:.1f} hrs")
        col4.metric(label="近期好评率", value=f"{positive_rate:.1f}%")
        
        st.write("") # 留白
        
        # --- 图表与报告区 ---
        col_chart, col_report = st.columns([1, 1.2])
        
        with col_chart:
            st.markdown("**📉 玩家游玩时长分布图**")
            # 简单好用的 Streamlit 原生柱状图
            st.bar_chart(df.set_index("推荐状态")['游玩时长(小时)'], color="#3498db")
            
            with st.expander("📄 查看抓取到的原始数据集"):
                # 隐藏内部的 0/1 列，只展示文本
                st.dataframe(df[['推荐状态', '游玩时长(小时)', '评论内容']], use_container_width=True)
                
        with col_report:
            with st.spinner('🧠 呼叫 NVIDIA 大模型进行传播学解读...'):
                report = analyze_reviews_with_llm(reviews_text)
            st.markdown("**💡 AI 评价洞察报告**")
            st.info(report)
            
    else:
        st.error("数据抓取失败，可能是该游戏近期没有评论，或者网络连接异常。")
else:
    # 初始状态下的引导提示
    st.info("👈 请在左侧边栏选择一款游戏，点击“启动实时分析”生成报告。")
