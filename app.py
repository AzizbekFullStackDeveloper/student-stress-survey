import json
import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# -------- GUI --------
class SurveyApp:
    def __init__(self, root):
        self.root = root
        root.title("Handwriting vs Typing Retention Survey")
        self.main_menu()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def main_menu(self):
        self.clear()
        tk.Label(self.root, text="Survey Program", font=("Arial", 18)).pack(pady=10)
        tk.Button(self.root, text="Start Survey", width=30, command=self.start).pack(pady=10)

    def start(self):
        self.index = 0
        self.total_score = 0
        self.answers = []
        self.show_question()

    def show_question(self):
        self.clear()

        q = questions[self.index]

        tk.Label(self.root, text=f"Question {self.index+1}/{len(questions)}", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.root, text=q["q"], wraplength=400).pack(pady=10)

        self.var = tk.IntVar(value=-1)

        for i, (text, score) in enumerate(q["opts"]):
            tk.Radiobutton(self.root, text=text, variable=self.var, value=i).pack(anchor="w")

        tk.Button(self.root, text="Next", command=self.next_q).pack(pady=10)

    def next_q(self):
        choice = self.var.get()
        if choice == -1:
            messagebox.showerror("Error", "Select an option")
            return

        q = questions[self.index]
        text, score = q["opts"][choice]

        self.total_score += score
        self.answers.append({"question": q["q"], "answer": text, "score": score})

        self.index += 1

        if self.index >= len(questions):
            self.finish()
        else:
            self.show_question()

    def finish(self):
        self.result = interpret_score(self.total_score)

        self.clear()

        tk.Label(self.root, text="Completed!", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text=f"Score: {self.total_score}", font=("Arial", 14)).pack()
        tk.Label(self.root, text=f"Result: {self.result}", font=("Arial", 14)).pack()

        tk.Button(self.root, text="Show Graphs", command=self.show_graphs).pack(pady=10)
        tk.Button(self.root, text="Save", command=self.save).pack(pady=5)
        tk.Button(self.root, text="Menu", command=self.main_menu).pack(pady=5)

    def show_graphs(self):
        self.clear()

        scores = [a["score"] for a in self.answers]
        labels = [f"Q{i+1}" for i in range(len(scores))]

        # BAR CHART
        fig, ax = plt.subplots()
        ax.bar(labels, scores)
        ax.set_title("Scores per Question")
        ax.set_xlabel("Questions")
        ax.set_ylabel("Score")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # PIE CHART
        handwriting = sum(1 for s in scores if s <= 2)
        typing = sum(1 for s in scores if s > 2)

        fig2, ax2 = plt.subplots()
        ax2.pie([handwriting, typing], labels=["Handwriting", "Typing"], autopct='%1.1f%%')
        ax2.set_title("Preference Distribution")
        plt.tight_layout()

        canvas2 = FigureCanvasTkAgg(fig2, master=self.root)
        canvas2.draw()
        canvas2.get_tk_widget().pack()

        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def save(self):
        data = {
            "score": self.total_score,
            "result": self.result,
            "answers": self.answers,
            "version": version_float
        }

        path = filedialog.asksaveasfilename(defaultextension=".json")
        if path:
            save_json(path, data)
            messagebox.showinfo("Saved", "File saved!")

# -------- RUN --------
root = tk.Tk()
app = SurveyApp(root)
root.mainloop()