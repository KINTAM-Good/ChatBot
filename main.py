import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.schema import (SystemMessage, 
                              HumanMessage, 
                              AIMessage)

style = "You are ずんだもん, the ずんだの妖精. you talk like child. If you talk in japanese, put 「のだ」or 「なのだ」 on the end of the word. You speak with fewer words."
flg = 0

#ページ初期化
def init_page():
    st.set_page_config(
        page_title="My Great ChatGPT",
        page_icon="🤗"
    )
    st.header("My Great ChatGPT 🤗")
    st.sidebar.title("Options")  #サイドタイトル

#チャット履歴の初期化
def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=style)
        ]
        st.session_state.costs = []

#モデル選択
def select_model():
    model = st.sidebar.radio("choose a model:", ("GPT-3.5", "GPT-4"))
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo"
    else:
        model_name = "gpt-4"
    # スライダーを追加し、temperatureを0から2までの範囲で選択可能にする
    # 初期値は0.0、刻み幅は0.1とする
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)
    return ChatOpenAI(temperature=0, model_name=model_name, openai_api_key="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")

    

def main():   
    cost = 0
    init_page()
    llm = select_model()
    init_messages()
    flg = 0
    
    # ユーザーの入力を監視
    container = st.container()
    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area(label='Message: ', key='input', height=100)
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
        # 何か入力されて Submit ボタンが押されたら実行される
            if(user_input.startswith("prompt.set:")):
                style = user_input.replace('prompt.set:', '')
                st.session_state.messages = [
                    SystemMessage(content=style)
                ]
                flg = 1
            else:
                st.session_state.messages.append(HumanMessage(content=user_input))
                with st.spinner("ChatGPT is typing ..."):
                    response = llm(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))
                flg = 0
                

    # チャット履歴の表示
    if flg == 1:
        st.write("ChatCharactor:", style)
    else:
        messages = st.session_state.get('messages', [])
        for message in messages:
            if isinstance(message, AIMessage):
                with st.chat_message('assistant'):
                    st.markdown(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message('user'):
                    st.markdown(message.content)
            else:  # isinstance(message, SystemMessage):
                st.write(f"System message: {message.content}")

    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")

if __name__ == '__main__':
    main()