import streamlit as st
import json
import requests

#----------------------------------------#
# 定义一个函数，用于调用API并获取响应
#----------------------------------------#   
def main(promot):
        
    url = "https://qianfan.baidubce.com/v2/app/conversation/runs"
    
    payload = json.dumps({
        "app_id": "9d75b4fd-68ed-466d-b02e-78b73ae76e02", 
        "query": promot,
        "conversation_id": "6364af97-370d-48ae-9c73-f0a6d2021576",
        "stream": False
    }, ensure_ascii=False)
    headers = {
        'Content-Type': 'application/json',
        'X-Appbuilder-Authorization': 'Bearer bce-v3/ALTAK-p9qRLsft9cRyQk3bbmlal/fceb7d71a4e1b8a0059d74123e8b1517962e20bb'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    
    
    return response.text  
#----------------------------------------#

st.set_page_config(    
    page_title="运动心电图预测心衰问答",    
    page_icon="❤️",    
    layout="wide",    
    initial_sidebar_state="expanded")    
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    [data-testid="stSidebar"] {
            min-width: 450px;
            max-width: 450px;
        }
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('bg-heart.png')

st.header('🤖运动心电图预测心衰问答')
 
with st.sidebar:
    st.image('logo.png')
    with st.container():
        st.write('说明：')
        st.write('''该APP的主要功能是使用用户输入的运动心电图数据对用户患有心力衰竭风险以及通过SHAP分析得到的各个变量的对预测结果的贡献值。
                        大语言模型对以上结果进行解释，并根据以上结果提供个性化的建议。用户通过查看示例数据获得输入参数的格式，并在对话框中输自己的数据进行预测。''')
    '---'
    st.write('''
    问句示例：
    1. 示例数据
    2. 输入模拟数据到预测模型(或者复制数据到对话框)
    3. 解释结果                   
    ''')
    '---'
    st.write("模型效能评价：")
    # st.image('time_dependent_auc.png')
    st.write('变量重要性：')
    # st.image('variable_important.png')
    
    
# 经典的问句
# api_key=st.secrets["API_key"]
# secret_key=st.secrets["secret_key"]

# 检查会话状态中是否存在'messages'键，如果不存在，则初始化'messages'列表
# 并添加一条欢迎消息
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "欢迎使用运动心电图预测心衰问答系统。希望能为你提供心力衰竭方面预防方面的建议！"}]

# 获取用户输入的文本，并将其添加到会话状态的'messages'列表中
if prompt := st.chat_input():   #赋值表达式
    st.session_state.messages.append({"role": "user", "content": prompt})

# 遍历会话状态中的消息列表，并使用Streamlit的chat_message组件显示每条消息
for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 如果最后一条消息不是来自助手，则生成新的响应
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # 调用main函数处理用户输入，并获取响应
            response = main(prompt)
            # 将响应解析为JSON格式
            msg = json.loads(response)
            # 提取响应中的答案部分
            answer = msg["answer"]
            # 将助手的回答添加到会话状态的'messages'列表中
            st.session_state.messages.append({'role':'assistant','content':answer})
            # 使用Streamlit的write组件显示助手的回答
            st.write(answer)
