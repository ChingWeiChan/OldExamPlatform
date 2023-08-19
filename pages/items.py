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
            tmp = next(counter)
            # st.subheader("題目")
            st.code(f"{questions[0]}")
            with st.expander("答案"):
                st.code(f"{questions[1]}")
            st.write(f"""標籤：{", ".join(questions[2])}""")
            with st.expander("討論區"):
                get_discussion = run_query(
                    f"""SELECT discussion from questions WHERE question = '{questions[0]}';""")
                if get_discussion[0][0]:
                    for discussion in get_discussion[0][0]:
                        st.code(discussion[1:-1])

                st.divider()
                with st.form(key=f"form_{tmp}"):
                    new_user = st.text_input(
                        "討論者名稱：", key=f"user_{tmp}")
                    new_discussion = st.text_area(
                        "討論內容：", key=f"new_discussion_{tmp}")
                    submitted = st.form_submit_button(
                        "加入討論吧！")
                    if submitted:
                        if get_discussion == [(None,)]:
                            content = [f"({new_user}: {new_discussion})"]
                        else:
                            content = get_discussion[0][0] + \
                                [f"({new_user}: {new_discussion})"]
                        run_query(
                            f"""UPDATE questions SET \
                                discussion=ARRAY{content} \
                            WHERE question='{questions[0]}';""")
                        st.write("加入成功！")

            col1, col2 = st.columns([0.1, 0.9])

            st.divider()
            if col1.button("刪除題目", key=f"D_{tmp}"):
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
