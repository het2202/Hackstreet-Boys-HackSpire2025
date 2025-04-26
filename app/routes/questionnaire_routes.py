from flask import Blueprint, render_template, request
from app.utils.emotion_messages import emotion_messages

questionnaire_bp = Blueprint('questionnaire', __name__)

# Define a function to ask the user the 15 MCQ psychological questions
def ask_questions():
    questions_with_options = [
        # ... (same questions as in your code)
    ]
    
    total_score = 0
    print("Answer the following questions based on your feelings:")

    # Loop through each question and get the user's response
    for i, q in enumerate(questions_with_options, start=1):
        print(f"\nQ{i}: {q['question']}")
        for idx, option in enumerate(q['options'], start=1):
            print(f"{idx}: {option}")
        
        while True:
            try:
                score = int(input("Your choice (1-4): "))
                if score < 1 or score > len(q['options']):
                    print(f"Please enter a number between 1 and {len(q['options'])}.")
                    continue
                # Add points based on answer choice, scoring can be adjusted here.
                total_score += score
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    return total_score

# Function to categorize mood
def detect_mood(total_score):
    # Mood categories based on score
    mood_score = total_score // 3  # Dividing to scale

    if mood_score <= 5:
        mood = 'sad'
    elif mood_score <= 10:
        mood = 'fear'
    elif mood_score <= 15:
        mood = 'neutral'
    elif mood_score <= 20:
        mood = 'anger'
    elif mood_score <= 25:
        mood = 'disgust'
    elif mood_score <= 30:
        mood = 'surprised'
    else:
        mood = 'happy'

    message = emotion_messages[mood]
    return mood, message

@questionnaire_bp.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        total_score = ask_questions()
        mood, message = detect_mood(total_score)
        return render_template('result.html', mood=mood, message=message)
    
    return render_template('questionnaire.html')

