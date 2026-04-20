import streamlit as st
import pandas as pd

st.title("COFFEE MEISTER")

# ----------------------
# データ読み込み
# ----------------------
df = pd.read_excel("quiz.xlsx")
df.columns = df.columns.str.strip()  # 列名のスペース対策

# ----------------------
# 初期化
# ----------------------
if "quiz_list" not in st.session_state:
    st.session_state.quiz_list = []

if "index" not in st.session_state:
    st.session_state.index = 0

if "correct" not in st.session_state:
    st.session_state.correct = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "wrong_questions" not in st.session_state:
    st.session_state.wrong_questions = []

# ----------------------
# 設定（ジャンル・問題数）
# ----------------------
genres = df["ジャンル"].dropna().unique()
selected_genre = st.selectbox("ジャンルを選択", genres)

num_questions = st.selectbox("問題数", [10, 30, 100])

# ----------------------
# スタートボタン
# ----------------------
if st.button("スタート", key="start", use_container_width=True):
    filtered_df = df[df["ジャンル"] == selected_genre]

    st.session_state.quiz_list = filtered_df.sample(
        min(num_questions, len(filtered_df))
    ).to_dict("records")

    st.session_state.index = 0
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.answered = False
    st.session_state.wrong_questions = []

    st.rerun()

# ----------------------
# クイズ開始後
# ----------------------
if st.session_state.quiz_list:

    # 終了処理
    if st.session_state.index >= len(st.session_state.quiz_list):
        st.success("終了！お疲れ様 🎉")
        st.write(f"最終スコア: {st.session_state.correct}/{st.session_state.total}")
        st.stop()

    q = st.session_state.quiz_list[st.session_state.index]

    # 問題番号
    st.write(f"{st.session_state.index + 1} / {len(st.session_state.quiz_list)} 問")

    # 問題表示
    st.subheader(q["問題"])

    # 正解率
    if st.session_state.total > 0:
        accuracy = st.session_state.correct / st.session_state.total * 100
        st.write(f"正解率: {accuracy:.1f}%（{st.session_state.correct}/{st.session_state.total}）")

    # 入力欄（問題ごとにリセット）
    user_answer = st.text_input(
        "答えを入力",
        key=f"input_{st.session_state.index}"
    )

    st.divider()

    # ----------------------
    # 答え合わせ
    # ----------------------
    if st.button("答え合わせ", key="check", use_container_width=True) and not st.session_state.answered:
        st.session_state.total += 1
        st.session_state.answered = True

        correct_answer = str(q["正解"]).strip()
        user_input = str(user_answer).strip()

        # 判定（ゆるめ：部分一致 + 小文字対応）
        if correct_answer.lower() in user_input.lower():
            st.success("〇 正解！")
            st.session_state.correct += 1
        else:
            st.error(f"× 不正解… 正解は「{correct_answer}」")
            st.session_state.wrong_questions.append(q)

    # ----------------------
    # 次の問題
    # ----------------------
    if st.button("次の問題", key="next", use_container_width=True):
        st.session_state.index += 1
        st.session_state.answered = False
        st.rerun()

# ----------------------
# リセット
# ----------------------
if st.button("リセット", key="reset", use_container_width=True):
    st.session_state.clear()
    st.rerun()
