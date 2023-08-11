import streamlit as st
from database import run_query
from itertools import count
counter = count(0)

st.header("題目分類")
st.write("可進行刪除或修改")
tabs = st.tabs(st.session_state["label"])
st.session_state["questions"] = run_query("SELECT * from questions;")
for tab, label in zip(tabs, st.session_state["label"]):
    with tab:
        st.header(label)
        question_with_label = [
            x for x in st.session_state["questions"] if label in x[2]]
        for questions in question_with_label:
            # st.subheader("題目")
            st.code(f"{questions[0]}")
            with st.expander("答案"):
                st.code(f"{questions[1]}")
            st.write(f"""標籤：{", ".join(questions[2])}""")
            col1, col2 = st.columns([0.1, 0.9])
            st.divider()
            if col1.button("刪除題目", key=f"D_{(tmp:=next(counter))}"):
                run_query(
                    f"DELETE FROM questions WHERE question = '{questions[0]}';")
                st.experimental_rerun()
            with col2.expander("修正題目"):
                fixed_question = st.text_area(
                    "請修正考古題題目：", value=questions[0])
                fixed_answer = st.text_area("請修正該題答案：", value=questions[1])
                fixed_label = st.multiselect(
                    "修正後的標籤",
                    st.session_state["label"],
                    default=questions[2],
                    key=f"U_{tmp}")
                submitted = st.button("Submit", key=f"submit_{tmp}")
                if submitted:
                    st.write("hahahhahaha")
                    run_query(
                        f"""UPDATE questions SET
                            question='{fixed_question}',answer='{fixed_answer}',\
                                label=ARRAY{fixed_label} \
                                    WHERE question = '{questions[0]}';
                                """)
                    st.experimental_rerun()
