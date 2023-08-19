import streamlit as st
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI
from database import run_query
template = """以下是原本的題目內容:{question} 解答是: {answer}
根據上面敘述，處理以下事情：
題目與答案換句話說，內文意思不變，並依照以下格式輸出，
題目：
答案："""
prompt = PromptTemplate(template=template, input_variables=[
                        "question", "answer"])


st.header("題目生成系統：換個方式思考")
st.subheader("這裡可以透過輸入過的題目來產生新的題目和答案，讓你換個方式思考題目和答案！")
options = st.selectbox("請選擇題目:", [i[0]
                       for i in run_query("SELECT * from questions;")])
# st.session_state["OPEN_AI_API"] = st.text_input("請輸入OpenAI的API KEY")
st.session_state["OPEN_AI_API"] = "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"
try:
    llm = OpenAI(
        openai_api_key=st.session_state["OPEN_AI_API"],
        model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    question = options
    answer = run_query(
        f"SELECT answer from questions WHERE question='{options}';")
    st.code(llm_chain.run(
        {"question": question, "answer": answer}))
except:
    st.write("尚未輸入KEY或者輸入有誤！")
