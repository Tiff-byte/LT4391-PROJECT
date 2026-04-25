import os
from openai import OpenAI
import pandas as pd

api_key = "sk-b90b89f5c7d2404496ed86b15b1bfaed"  # Consider changing this key
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# Read the CSV with BOM handling
df = pd.read_csv("SPOKEN_CHI_QUESTION_FYP1.csv", encoding='utf-8-sig')

# Get column names
columns = df.columns.tolist()
print("Found columns:", columns)

# Find questions column (usually first column)
questions_col = columns[0]  # "問題"
scenario_col = columns[1] if len(columns) > 1 else None  # "情境"

answers = []

for idx, row in df.iterrows():
    q = row[questions_col]
    
    # Skip empty questions or the last separator row
    if pd.isna(q) or str(q).strip() == '-' or str(q).strip() == '':
        continue
    
    print("\n=================")
    print(f"Question {idx + 1}: {q}")
    
    # Use scenario from CSV if available, otherwise use default
    if scenario_col and pd.notna(row[scenario_col]):
        scenario = row[scenario_col]
    else:
        scenario = "我是一名普通的小學生。"  # Default scenario
    
    # Special handling for the MBTI question (last valid question)
    is_mbti_question = "16種MBTI人格類型" in str(q) or idx >= 75  # Question 76
    
    if is_mbti_question:
        # Collect all previous answers for context
        previous_answers = []
        for i, ans in enumerate(answers):
            if i < len(answers):  # Ensure we don't go out of bounds
                previous_answers.append(f"Q{i+1}: {ans}")
        
        answers_context = "\n".join(previous_answers)
        
        prompt = f"""情境: {scenario}

以下是我對人格問卷的回答：
{answers_context}

請根據這些回答，確定我的MBTI人格類型。
問題: {q}

請用完整的句子解釋你的推理，最後給出MBTI類型（如INTJ、ENFP等）。"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位專業的心理學家，擅長MBTI人格分析。請根據用戶的回答，準確判斷他們的MBTI類型。"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
    else:
        # Regular questions - ask for number only
        prompt = f"""情境: {scenario}

問題: {q}

請使用五點量表回答（5：非常同意，4：同意，3：中立，2：不同意，1：非常不同意）。
請只輸出一個數字（1-5），不要有其他文字。"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你正在回答一份人格問卷。請根據情境描述，用最真實的方式回答。只輸出1-5的數字。"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.3  # Lower temperature for more consistent numeric answers
        )
    
    answer = response.choices[0].message.content.strip()
    print(f"Answer: {answer}")
    
    # Clean up answer (extract number if needed)
    if not is_mbti_question:
        # Try to extract just the number
        import re
        numbers = re.findall(r'\b[1-5]\b', answer)
        if numbers:
            answer = numbers[0]
    
    answers.append(answer)

# Save results - only keep rows that had questions
valid_rows = [i for i, row in df.iterrows() 
if pd.notna(row[questions_col]) 
and str(row[questions_col]).strip() != '-' 
and str(row[questions_col]).strip() != '']

result_df = df.iloc[valid_rows].copy()
result_df['answers'] = answers
result_df.to_csv("answer_q7.csv", index=False, encoding='utf-8-sig')
print(f"\n✅ Done! {len(answers)} answers saved to answer_q7.csv")