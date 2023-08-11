import streamlit as st
# from Upload import QUESTIONS

st.header("題目標籤分類")

tabs = st.tabs(st.session_state["label"])

for tab, label in zip(tabs, st.session_state["label"]):
    with tab:
        st.header(label)
        question_with_label = [
            x for x in st.session_state["questions"] if label in x.label]
        for questions in question_with_label:
            st.subheader(f"題目{questions.order}")
            st.code(f"{questions.question}")
            with st.expander("答案"):
                st.code(f"{questions.answer}")
            st.write(f"""標籤：{",".join(questions.label)}""")
