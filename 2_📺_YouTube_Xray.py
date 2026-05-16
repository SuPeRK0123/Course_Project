import streamlit as st
import requests
import re
import pandas as pd
import plotly.express as px

# 【请在这里填入你的两个 API Key】
YOUTUBE_API_KEY = "xxx"
NVIDIA_API_KEY = "xxx"

# --- 页面全局配置 ---
st.set_page_config(page_title="YouTube X-Ray", page_icon="📺", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# --- 辅助函数 ---
def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

# --- 核心功能 ---
@st.cache_data(ttl=120)
def get_youtube_comments(video_id, max_results=20):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {'part': 'snippet', 'videoId': video_id, 'key': YOUTUBE_API_KEY, 'maxResults': max_results, 'textFormat': 'plainText'}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        items = response.json().get('items',[])
        formatted_text = ""
        raw_data =[]
        
        for i, item in enumerate(items):
            snippet = item['snippet']['topLevelComment']['snippet']
            author = snippet['authorDisplayName']
            text = snippet['textDisplay'].replace('\n', ' ')
            like_count = int(snippet.get('likeCount', 0))
            
            formatted_text += f"评论 {i+1}[作者: {author}, 点赞: {like_count}]: {text[:200]}\n"
            raw_data.append({"作者": author, "点赞数": like_count, "评论内容": text})
            
        return formatted_text, pd.DataFrame(raw_data)
    else:
        st.error(f"YouTube API 请求失败: {response.json().get('error', {}).get('message', '未知错误')}")
        return None, None

def analyze_youtube_comments_with_llm(comments_text):
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""
    你是一位资深的传媒与社会学学者。阅读以下YouTube热门视频的前排评论，生成一份【评论区 X 光透视报告】：
    1. 【情绪主基调】：整体是正面、负面还是充满争议？主要的情绪是什么（狂欢/愤怒/吃瓜/感动）？
    2. 【观点阵营划分】：总结出“支持方”和“反对方/质疑方”的核心观点。如无对立，总结大家最共鸣的点。
    3. 【传播学毒舌点评】：用一句话总结这群受众在这个视频下的群体表现（例如涉及信息茧房、群体极化、或寄生性社会关系）。
    数据：
    {comments_text}
    """
    
    payload = {"model": "meta/llama-3.1-70b-instruct", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 600}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return f"请求失败: {response.text}"

# --- UI 布局设计 ---
st.title("📺 YouTube 评论区 X 光机")
st.markdown("通过抓取高赞评论并进行语义降维，瞬间解剖视频背后的**受众情绪**与**阵营划分**。")
st.markdown("---")

# 1. 侧边栏控制台
with st.sidebar:
    st.header("🎛️ 链接解析 (Console)")
    video_url = st.text_input("🔗 粘贴 YouTube 视频链接:", placeholder="https://www.youtube.com/watch?v=...")
    sample_size = st.slider("抓取前排热评数量", min_value=10, max_value=50, value=20, step=10)
    start_btn = st.button("🔍 启动深度透视", use_container_width=True, type="primary")

    st.markdown("---")
    st.caption("💡 小提示：你可以尝试输入不同立场的新闻报道、热门科技评测、或是爆款恶搞视频的链接进行对比。")

# 2. 主展示区
if start_btn:
    if not video_url:
        st.warning("👈 请先在左侧输入视频链接哦！")
    else:
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("无法识别的 YouTube 链接格式，请检查后重试。")
        else:
            with st.spinner('📡 正在通过 API 穿越回 YouTube 抓取高赞评论...'):
                comments_text, df = get_youtube_comments(video_id, max_results=sample_size)
                
            if df is not None and not df.empty:
                # --- 核心指标 KPI ---
                total_likes = df['点赞数'].sum()
                max_likes = df['点赞数'].max()
                top_author = df.loc[df['点赞数'].idxmax()]['作者'] if not df.empty else "无"
                
                st.subheader("📊 评论区热度声量大盘")
                col1, col2, col3 = st.columns(3)
                col1.metric(label="成功抓取热评数", value=f"{len(df)} 条")
                col2.metric(label="采样评论总点赞量", value=f"{total_likes:,}")
                col3.metric(label="最高赞评论作者", value=f"{top_author}", delta=f"{max_likes:,} 赞", delta_color="normal")
                
                st.write("") # 留白
                
                # --- 图表与报告区 ---
                col_chart, col_report = st.columns([1, 1.2])
                
                with col_chart:
                    st.markdown("**📈 头部声量矩阵 (悬浮查看详情)**")
                    
                    chart_df = df.sort_values(by="点赞数", ascending=False).head(10)
                    
                    if chart_df['点赞数'].sum() == 0:
                        st.warning("👀 当前抓取到的评论点赞数均为 0，可能是由于最新评论或 UP 主隐藏了数据，暂无图表生成。")
                    else:
                        # 召唤 Plotly 绘制动态渐变交互图
                        fig = px.bar(
                            chart_df, 
                            x="作者", 
                            y="点赞数", 
                            color="点赞数", 
                            color_continuous_scale="Tealgrn", 
                            hover_data={"评论内容": True, "点赞数": True, "作者": False},
                            text="点赞数" 
                        )
                        
                        fig.update_layout(
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#F3F4F6"),
                            margin=dict(l=0, r=0, t=30, b=0),
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True, gridcolor="#374151")
                        )
                        fig.update_traces(textposition='outside', textfont_color='#00E5FF')
                        st.plotly_chart(fig, use_container_width=True)
                        
                with col_report:
                    with st.spinner('🧠 呼叫 AI 学者进行传播学深度剖析...'):
                        report = analyze_youtube_comments_with_llm(comments_text)
                    st.markdown("**💡 传播学受众洞察报告**")
                    st.info(report)
