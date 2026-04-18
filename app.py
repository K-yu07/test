import streamlit as st
import pandas as pd
import random

st.title("暗記アプリ（4択）")

df = pd.read_excel("quiz.xlsx")

# 問題保持
if "question" not in st.session_state:
    st.session_state.question = df.sample(1).iloc[0]

# 選択肢生成（Noneなら作る）
if "choices" not in st.session_state or st.session_state.choices is None:
    q = st.session_state.question
    choices = [
        q["選択肢1"],
        q["選択肢2"],
        q["選択肢3"],
        q["選択肢4"]
    ]
    random.shuffle(choices)
    st.session_state.choices = choices

q = st.session_state.question
choices = st.session_state.choices

# 表示
st.subheader(q["問題"])

# 回答
user_answer = st.radio("選択してください", choices)

# 判定
if st.button("答え合わせ"):
    if user_answer == q["正解"]:
        st.success("正解！🎉")
    else:
        st.error(f"不正解… 正解は {q['正解']}")

# 次の問題
if st.button("次の問題"):
    st.session_state.question = df.sample(1).iloc[0]
    st.session_state.choices = None  # ←これで再生成される
    st.rerun()
