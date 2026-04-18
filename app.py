import streamlit as st
import pandas as pd
import random

st.title("暗記アプリ")

df = pd.read_excel("quiz.xlsx")

if "question" not in st.session_state:
    st.session_state.question = df.sample(1).iloc[0]

q = st.session_state.question

st.subheader(q["問題"])

user_answer = st.text_input("答えを入力")

if st.button("答え合わせ"):
    if user_answer.strip() == str(q["答え"]).strip():
        st.success("正解！")
    else:
        st.error(f"不正解… 正解は {q['答え']}")

if st.button("次の問題"):
    st.session_state.question = df.sample(1).iloc[0]
    st.rerun()
