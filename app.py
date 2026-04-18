import streamlit as st
import pandas as pd
import random

st.title("暗記アプリ（4択）")

df = pd.read_excel("quiz.xlsx")

# 列名の余計なスペース対策
df.columns = df.columns.str.strip()

# ----------------------
# 初期化
# ----------------------
if "correct" not in st.session_state:
    st.session_state.correct = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "wrong_questions" not in st.session_state:
    st.session_state.wrong_questions = []

if "quiz_list" not in st.session_state:
    st.session_state.quiz_list = []

if "index" not in st.session_state:
    st.session_state.index = 0

if "choices" not in st.session_state:
    st.session_state.choices = None

# ----------------------
# ジャンル・問題数選択
# ----------------------
genres = df["ジャンル"].unique()
selected_genre = st.selectbox("ジャンルを選択", genres)

num_questions = st.selectbox("問題数", [5, 10, 20])

# クイズ開始ボタン
if st.button("スタート", key="start"):
    filtered_df = df[df["ジャンル"] == selected_genre]

    st.session_state.quiz_list = filtered_df.sample(
        min(num_questions, len(filtered_df))
    ).to_dict("records")

    st.session_state.index = 0
    st.session_state.choices = None
    st.session_state.correct = 0
    st.session_state.total = 0
    st.rerun()

# ----------------------
# クイズがあるときだけ表示
# ----------------------
if st.session_state.quiz_list:

    # 終了判定
    if st.session_state.index >= len(st.session_state.quiz_list):
        st.success("終了！お疲れ様 🎉")
        st.write(f"最終スコア: {st.session_state.correct}/{st.session_state.total}")
        st.stop()

    q = st.session_state.quiz_list[st.session_state.index]

    # 選択肢生成
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

    # 表示
    st.subheader(q["問題"])

    # 正解率
    if st.session_state.total > 0:
        accuracy = st.session_state.correct / st.session_state.total * 100
        st.write(f"正解率: {accuracy:.1f}%（{st.session_state.correct}/{st.session_state.total}）")

    user_answer = st.radio("選択してください", choices)

    # 答え合わせ
    if st.button("答え合わせ", key="check"):
        st.session_state.total += 1

        if user_answer == q["正解"]:
            st.success("正解！🎉")
            st.session_state.correct += 1
        else:
            st.error(f"不正解… 正解は {q['正解']}")
            st.session_state.wrong_questions.append(q)

    # 次の問題
    if st.button("次の問題", key="next"):
        st.session_state.index += 1
        st.session_state.choices = None
        st.rerun()

# ----------------------
# リセット
# ----------------------
if st.button("リセット", key="reset"):
    st.session_state.clear()
    st.rerun()
