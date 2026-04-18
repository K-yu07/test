import streamlit as st
import pandas as pd
import random

st.title("暗記アプリ（4択）")

df = pd.read_excel("quiz.xlsx")
# ジャンル一覧取得
genres = df["ジャンル"].unique()

# 選択UI
selected_genre = st.selectbox("ジャンルを選択", genres)

# 問題数選択
num_questions = st.selectbox("問題数", [5, 10, 20])
filtered_df = df[df["ジャンル"] == selected_genre]

# ----------------------
# 初期化（最初に書く）
# ----------------------
if "question" not in st.session_state:
    st.session_state.question = df.sample(1).iloc[0]

if "choices" not in st.session_state:
    st.session_state.choices = None

if "correct" not in st.session_state:
    st.session_state.correct = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "wrong_questions" not in st.session_state:
    st.session_state.wrong_questions = []

# ----------------------
# 問題・選択肢
# ----------------------
q = st.session_state.question

if st.session_state.choices is None:
    choices = [
        q["選択肢1"],
        q["選択肢2"],
        q["選択肢3"],
        q["選択肢4"]
    ]
    random.shuffle(choices)
    st.session_state.choices = choices

choices = st.session_state.choices

# ----------------------
# 表示
# ----------------------
st.subheader(q["問題"])

# ⭐ 正解率表示（ここで出す）
if st.session_state.total > 0:
    accuracy = st.session_state.correct / st.session_state.total * 100
    st.write(f"正解率: {accuracy:.1f}%（{st.session_state.correct}/{st.session_state.total}）")

user_answer = st.radio("選択してください", choices)

# ----------------------
# 答え合わせ（1つだけ！）
# ----------------------
if st.button("答え合わせ", key="check"):
    st.session_state.total += 1

    if user_answer == q["正解"]:
        st.success("正解！🎉")
        st.session_state.correct += 1
    else:
        st.error(f"不正解… 正解は {q['正解']}")
        st.session_state.wrong_questions.append(q)

# ----------------------
# 次の問題
# ----------------------
if st.button("次の問題", key="next"):
    st.session_state.question = df.sample(1).iloc[0]
    st.session_state.choices = None
    st.rerun()

# ----------------------
# リセット
# ----------------------
if st.button("リセット", key="reset"):
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.wrong_questions = []
    st.rerun()
