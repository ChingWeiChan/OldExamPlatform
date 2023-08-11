import streamlit as st
from dataclasses import dataclass
from typing import List
from itertools import count


@dataclass
class QUESTIONS:
    order: int
    question: str
    answer: str
    label: List[str]


st.header("考古題輸入平台")
if "questions" not in st.session_state.keys():
    st.session_state["questions"] = []
    st.session_state["label"] = ["計算機科學", "有機化學", "量子物理", "普通生物學"]
    st.session_state["order"] = count(1)

question = st.text_area("請輸入考古題題目：")
answer = st.text_area("請輸入該題答案：")
options = st.multiselect(
    "並輸入與這題相關的標籤",
    st.session_state["label"])
if st.button("上傳"):
    st.session_state["questions"].append(
        QUESTIONS(next(st.session_state["order"]), question,
                  answer,
                  options))

for questions in st.session_state["questions"]:
    st.subheader(f"已新增題目{questions.order}")
    st.code(f"{questions.question}")
    with st.expander("答案"):
        st.code(f"{questions.answer}")
    st.write(f"""標籤：{",".join(questions.label)}""")
