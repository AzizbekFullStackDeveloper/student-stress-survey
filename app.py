import json
import streamlit as st
import matplotlib.pyplot as plt

# -------- VARIABLES --------
version_float = 1.1

# -------- QUESTIONS (15) --------
questions = [
    {"q": "Notes are usually taken by handwriting rather than typing.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "Typing notes feels faster and more efficient than handwriting.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]},

    {"q": "Handwritten notes help with better understanding of material.",
     "opts": [("Strongly agree",0),("Agree",1),("Neutral",2),("Disagree",3),("Strongly disagree",4)]},

    {"q": "Typed notes are easier to organize and review later.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]},

    {"q": "More information is remembered when writing notes by hand.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "While typing, attention is often distracted by other applications.",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "Handwriting notes requires deeper thinking about the material.",
     "opts": [("Strongly agree",0),("Agree",1),("Neutral",2),("Disagree",3),("Strongly disagree",4)]},

    {"q": "Typed notes are preferred for long lectures or large content.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]},

    {"q": "Reviewing handwritten notes improves recall during exams.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "Typed notes often include more detailed information than handwritten notes.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]},

    {"q": "It is easier to focus when taking notes by hand.",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "Typing notes helps save time during lectures.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]},

    {"q": "Handwritten notes are more useful for long-term memory.",
     "opts": [("Strongly agree",0),("Agree",1),("Neutral",2),("Disagree",3),("Strongly disagree",4)]},

    {"q": "Typed notes are preferred due to readability and neatness.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]},

    {"q": "Combining both handwriting and typing improves learning outcomes.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Neutral",2),("Agree",3),("Strongly agree",4)]}
]

# -------- STATES --------
psych_states = {
    "Strong Handwriting Preference (High Retention)": (0, 15),
    "Balanced Method User (Effective Learning)": (16, 30),
    "Moderate Retention (Method Dependent)": (31, 45),
    "Typing Preference (Lower Retention Risk)": (46, 60)
}

# -------- FUNCTIONS --------
def interpret_score(score):
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def build_result_data(total_score, result, answers):
    return {
        "score": total_score,
        "result": result,
        "answers": answers,
        "version": version_float,
    }

def init_state():
    st.session_state.setdefault("started", False)
    st.session_state.setdefault("index", 0)
    st.session_state.setdefault("total_score", 0)
    st.session_state.setdefault("answers", [])
    st.session_state.setdefault("finished", False)


def reset_survey():
    st.session_state.started = False
    st.session_state.index = 0
    st.session_state.total_score = 0
    st.session_state.answers = []
    st.session_state.finished = False


def render_charts(scores):
    labels = [f"Q{i+1}" for i in range(len(scores))]

    fig, ax = plt.subplots()
    ax.bar(labels, scores)
    ax.set_title("Scores per Question")
    ax.set_xlabel("Questions")
    ax.set_ylabel("Score")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    handwriting = sum(1 for s in scores if s <= 2)
    typing = sum(1 for s in scores if s > 2)

    fig2, ax2 = plt.subplots()
    ax2.pie([handwriting, typing], labels=["Handwriting", "Typing"], autopct="%1.1f%%")
    ax2.set_title("Preference Distribution")
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)


def render_app():
    st.set_page_config(page_title="Handwriting vs Typing Retention Survey", layout="centered")
    init_state()

    st.title("Handwriting vs Typing Retention Survey")

    if not st.session_state.started:
        st.write("Survey Program")
        if st.button("Start Survey", type="primary"):
            st.session_state.started = True
            st.rerun()
        return

    if st.session_state.finished:
        result = interpret_score(st.session_state.total_score)
        st.success("Completed!")
        st.write(f"Score: {st.session_state.total_score}")
        st.write(f"Result: {result}")

        scores = [a["score"] for a in st.session_state.answers]
        render_charts(scores)

        payload = build_result_data(st.session_state.total_score, result, st.session_state.answers)
        st.download_button(
            "Save Results (JSON)",
            data=json.dumps(payload, indent=2),
            file_name="survey_results.json",
            mime="application/json",
        )

        if st.button("Back to Menu"):
            reset_survey()
            st.rerun()
        return

    q = questions[st.session_state.index]
    st.subheader(f"Question {st.session_state.index + 1}/{len(questions)}")
    st.write(q["q"])

    option_texts = [text for text, _ in q["opts"]]
    selected_text = st.radio("Choose one option", option_texts, index=None)

    if st.button("Next"):
        if selected_text is None:
            st.error("Select an option")
            return

        selected = next(item for item in q["opts"] if item[0] == selected_text)
        text, score = selected
        st.session_state.total_score += score
        st.session_state.answers.append({"question": q["q"], "answer": text, "score": score})
        st.session_state.index += 1

        if st.session_state.index >= len(questions):
            st.session_state.finished = True

        st.rerun()


render_app()