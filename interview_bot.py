import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

questions = [
    {
        "question": "Tell me about yourself.",
        "keywords": ["education", "skills", "experience", "role"],
        "sample_answer": "I am a final year Computer Science student with strong skills in Python and web development. I have completed internships and worked on projects involving AI and databases. I am excited about this role because it aligns with my skills and career goals."
    },
    {
        "question": "What are your strengths?",
        "keywords": ["problem-solving", "teamwork", "adaptability", "communication", "leadership"],
        "sample_answer": "My strengths include problem-solving, adaptability, teamwork, and effective communication. I can quickly analyze problems and collaborate well with others. I am also learning leadership skills to take initiative when needed."
    },
    {
        "question": "What are your weaknesses?",
        "keywords": ["perfectionist", "time management", "improvement"],
        "sample_answer": "I tend to focus too much on details, which sometimes affects my time management. I am actively improving by setting priorities and managing tasks efficiently."
    },
    {
        "question": "Why should we hire you?",
        "keywords": ["skills", "dedication", "contribution", "fit"],
        "sample_answer": "You should hire me because I have the required technical skills, I am dedicated to learning, and I can contribute to the company’s success. My abilities and work ethic align well with this role."
    },
    {
        "question": "Where do you see yourself in 5 years?",
        "keywords": ["growth", "career", "leadership", "learning"],
        "sample_answer": "In 5 years, I see myself growing into a leadership role where I can mentor juniors, enhance my technical skills, and contribute to the company’s long-term goals."
    },
    {
        "question": "Describe a time you worked in a team.",
        "keywords": ["teamwork", "collaboration", "conflict resolution", "success"],
        "sample_answer": "During a project, I collaborated with my teammates to divide tasks efficiently. We faced conflicts in approach but resolved them through discussion, which helped us successfully complete the project on time."
    },
    {
        "question": "What motivates you?",
        "keywords": ["learning", "challenges", "growth", "impact"],
        "sample_answer": "I am motivated by learning new skills, taking on challenges, and making an impact through my work. Completing projects that benefit others gives me a sense of achievement."
    },
    {
        "question": "How do you handle stress or pressure?",
        "keywords": ["planning", "focus", "priority", "calm"],
        "sample_answer": "I handle stress by planning my tasks, staying focused on priorities, and maintaining a calm mindset. Breaking tasks into smaller steps helps me work efficiently under pressure."
    },
    {
        "question": "Why do you want to work for this company?",
        "keywords": ["company values", "role fit", "interest", "growth"],
        "sample_answer": "I want to work here because the company values innovation and teamwork, which align with my interests. The role fits my skills and offers opportunities for growth and learning."
    },
    {
        "question": "Tell me about a challenge you faced and how you solved it.",
        "keywords": ["challenge", "problem-solving", "initiative", "result"],
        "sample_answer": "In a previous project, we faced a tight deadline and technical issues. I analyzed the problem, suggested a solution, and collaborated with the team. As a result, we completed the project successfully on time."
    }
]

def evaluate_answer(user_answer, keywords):
    feedback = []
    for word in keywords:
        if word.lower() in user_answer.lower():
            feedback.append(f"Covered: {word}")
        else:
            feedback.append(f"Missing: {word}")
    return feedback

st.title("Job Interview Practice Bot")
mode = st.radio("Choose Mode", ["Single Question", "Practice Session"])

# Single Question Mode
if mode == "Single Question":
    q = questions[0]
    st.subheader(q["question"])
    user_answer = st.text_area("Your Answer", key="single_text")
    if st.button("Submit Answer", key="single_btn"):
        feedback = evaluate_answer(user_answer, q["keywords"])
        st.write("Feedback:")
        for f in feedback:
            st.write("-", f)
        st.write("Sample Answer:", q["sample_answer"])

# Practice Session Mode
else:
    if "session_data" not in st.session_state:
        st.session_state.session_data = []
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()

    if st.session_state.q_index < len(questions):
        q = questions[st.session_state.q_index]
        st.subheader(f"Question {st.session_state.q_index+1}: {q['question']}")

        # Timer
        time_limit = 60
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, time_limit - elapsed)
        st.progress(remaining / time_limit)
        st.write(f"Time Remaining: {remaining} seconds")

        answer_key = f"text_{st.session_state.q_index}"
        if remaining > 0:
            user_answer = st.text_area("Your Answer", key=answer_key)
        else:
            user_answer = st.session_state.get(answer_key, "")
            st.text_area("Your Answer (Time is up)", value=user_answer, disabled=True)

        # Auto-submit when time runs out
        if remaining == 0:
            feedback = evaluate_answer(user_answer, q["keywords"])
            covered = sum(1 for f in feedback if "Covered" in f)
            st.session_state.score += covered
            st.session_state.session_data.append({
                "Question": q["question"],
                "Your Answer": user_answer,
                "Feedback": ", ".join(feedback),
                "Sample Answer": q["sample_answer"]
            })
            st.session_state.q_index += 1
            st.session_state.start_time = time.time()
            st.experimental_rerun = lambda: None
            st.experimental_rerun()

        # Manual submit early
        if st.button("Submit Early"):
            feedback = evaluate_answer(user_answer, q["keywords"])
            covered = sum(1 for f in feedback if "Covered" in f)
            st.session_state.score += covered
            st.session_state.session_data.append({
                "Question": q["question"],
                "Your Answer": user_answer,
                "Feedback": ", ".join(feedback),
                "Sample Answer": q["sample_answer"]
            })
            st.session_state.q_index += 1
            st.session_state.start_time = time.time()
            st.experimental_rerun = lambda: None
            st.experimental_rerun()

    else:
        st.success(f"Session completed! Your score: {st.session_state.score}")

        df = pd.DataFrame(st.session_state.session_data)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Report", csv, "session_report.csv", "text/csv")

        # Score Analytics Graph
        df['Covered_Count'] = df['Feedback'].apply(lambda x: x.count("Covered"))
        plt.figure(figsize=(10,4))
        plt.bar(range(len(df)), df['Covered_Count'], color='skyblue')
        plt.xticks(range(len(df)), [f"Q{i+1}" for i in range(len(df))])
        plt.xlabel("Question")
        plt.ylabel("Keywords Covered")
        plt.title("Keyword Coverage per Question")
        st.pyplot(plt)

        # Overall Feedback Summary
        total_keywords = sum([len(q['keywords']) for q in questions])
        covered_keywords = st.session_state.score
        st.write(f"Total Keywords Covered: {covered_keywords} / {total_keywords}")

        if covered_keywords / total_keywords >= 0.8:
            st.success("Excellent! You covered most of the important points.")
        elif covered_keywords / total_keywords >= 0.5:
            st.info("Good. Some points are missing, try to improve.")
        else:
            st.warning("You need more practice. Focus on missing keywords.")

        if st.button("Start New Session"):
            st.session_state.session_data = []
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.experimental_rerun = lambda: None
            st.experimental_rerun()
