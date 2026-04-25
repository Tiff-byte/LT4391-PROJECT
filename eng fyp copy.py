import os
from openai import OpenAI
import pandas as pd

os.environ['OPENAI_API_KEY'] = "sk-b90b89f5c7d2404496ed86b15b1bfaed"
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'), base_url="https://api.deepseek.com")

# Read the CSV with BOM handling
df = pd.read_csv("ENG_QUESTION_FYP2.csv", encoding='utf-8-sig')

# Get the actual column names
columns = df.columns.tolist()
print("Found columns:", columns)

# Find the questions column
questions_col = None
for col in columns:
    if 'question' in col.lower():
        questions_col = col
        break

# If not found, use first column
if questions_col is None:
    questions = df.iloc[:, 0]
else:
    questions = df[questions_col]

answers = []

for idx, q in enumerate(questions):
    if pd.notna(q):
        print("\n=================")
        print(f"Question {idx + 1}: {q}")
        
        scenario = "You are a secondary school student who has just finished the DSE exams and is close to graduation. During taking a rest after exams but feel worried about the future, has no clear planning, often overthinks and questions themselves, yet remains social with friends."
        
        # Special handling for the last question (MBTI question)
        if idx == len(questions) - 1:  # Last question
            # Get all previous answers to provide context
            previous_answers = []
            for i, ans in enumerate(answers):
                previous_answers.append(f"Q{i+1}: {ans}")
            
            answers_context = "\n".join(previous_answers)
            
            prompt = f"""{scenario}

Here are my answers to the personality questionnaire:
{answers_context}

Based on these answers, please determine my MBTI personality type. 
Question: {q}

Please answer in complete sentences explaining your reasoning."""
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a secondary school student who has just finished the DSE exams and is close to graduation. During taking a rest after exams but feel worried about the future, has no clear planning, often overthinks and questions themselves, yet remains social with friends."},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )
        else:
            # Regular questions - ask for number only
            prompt = f"{scenario}\n\nPlease answer this question: {q}\n\nProvide your answer as a single number from 1 to 5."
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a secondary school student answering a personality questionnaire. Answer honestly based on your personality. Only respond with a single number from 1 to 5."},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )
        
        answer = response.choices[0].message.content
        print(f"Answer: {answer}")
        answers.append(answer)

# Save results
df['answers'] = answers
df.to_csv("answer_q2.csv", index=False, encoding='utf-8-sig')
print("\n✅ Done! Answers saved to answer.csv")