import random
import time

def generate_problem(operation, level):
    if level == "easy":
        num_range = (1, 10)
    elif level == "medium":
        num_range = (1, 50)
    else:
        num_range = (1, 100)
    
    num1 = random.randint(*num_range)
    num2 = random.randint(*num_range)

    if operation == "addition":
        correct_answer = num1 + num2
        operation_symbol = "+"
    elif operation == "subtraction":
        correct_answer = num1 - num2
        operation_symbol = "-"
    elif operation == "multiplication":
        correct_answer = num1 * num2
        operation_symbol = "*"
    else:
        num1 = random.randint(*num_range) * num2  # Ensures a clean division
        correct_answer = round(num1 / num2, 2)
        operation_symbol = "/"
    
    return num1, num2, operation_symbol, correct_answer

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"Time left: {i} seconds", end="\r")
        time.sleep(1)
    print("Time's up!                  ")

def show_achievement_message(achievement):
    print(f"\n*** Achievement Unlocked: {achievement} ***")

def math_game():
    print("Welcome to the Math Game!")
    
    player_name = input("Enter your name: ")
    score = 0
    level_up_threshold = 3
    level = "easy"
    max_time = 10
    streak = 0
    achievements = []
    lifelines = {"50-50": 1, "Skip": 1, "Hint": 1}
    
    while True:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. View Achievements")
        print("6. Quit")
        
        operation_choice = input("Enter the number of your choice: ")
        
        if operation_choice == "1":
            operation = "addition"
        elif operation_choice == "2":
            operation = "subtraction"
        elif operation_choice == "3":
            operation = "multiplication"
        elif operation_choice == "4":
            operation = "division"
        elif operation_choice == "5":
            print("\nYour Achievements:")
            if achievements:
                for ach in achievements:
                    print(f"- {ach}")
            else:
                print("No achievements yet. Keep playing!")
            continue
        elif operation_choice == "6":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        print("\nChoose a difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        
        level_choice = input("Enter the number of your choice: ")
        
        if level_choice == "1":
            level = "easy"
        elif level_choice == "2":
            level = "medium"
        elif level_choice == "3":
            level = "hard"
        else:
            print("Invalid choice. Please try again.")
            continue

        num_correct = 0
        num_questions = 5
        
        for _ in range(num_questions):
            num1, num2, operation_symbol, correct_answer = generate_problem(operation, level)
            
            print(f"\nWhat is {num1} {operation_symbol} {num2}?")
            
            # Offer lifelines
            if any(lifelines.values()):
                print("\nLifelines:")
                for lifeline, count in lifelines.items():
                    if count > 0:
                        print(f"- {lifeline} ({count} left)")

                use_lifeline = input("Do you want to use a lifeline? (yes/no): ").lower()
                if use_lifeline == "yes":
                    lifeline_choice = input("Which lifeline would you like to use? ").lower()
                    if lifeline_choice == "50-50" and lifelines["50-50"] > 0:
                        # 50-50 Lifeline: Eliminate two incorrect answers (not possible with text, just a concept)
                        print("50-50 Lifeline used! Two incorrect answers eliminated.")
                        lifelines["50-50"] -= 1
                    elif lifeline_choice == "skip" and lifelines["Skip"] > 0:
                        print("Skip Lifeline used! Moving to the next question.")
                        lifelines["Skip"] -= 1
                        continue
                    elif lifeline_choice == "hint" and lifelines["Hint"] > 0:
                        print(f"Hint Lifeline used! The answer is close to {round(correct_answer / 2, 2)}.")
                        lifelines["Hint"] -= 1
                    else:
                        print("Invalid lifeline choice or no uses left.")
                        continue
            
            # Start the timer
            countdown_timer(max_time)
            start_time = time.time()
            
            try:
                player_answer = float(input("Your answer: "))
                elapsed_time = time.time() - start_time
                if elapsed_time > max_time:
                    print("Too slow! Time's up.")
                    streak = 0
                    continue
            except ValueError:
                print("Please enter a valid number.")
                streak = 0
                continue
            
            if player_answer == correct_answer:
                print("Correct!")
                num_correct += 1
                streak += 1
                score += max(1, int(10 - elapsed_time))  # Faster answers yield more points
                
                # Streak bonuses
                if streak >= 3:
                    bonus = streak * 2
                    print(f"Streak bonus! +{bonus} points")
                    score += bonus

                # Unlock achievements
                if streak == 5 and "5 Correct in a Row" not in achievements:
                    achievements.append("5 Correct in a Row")
                    show_achievement_message("5 Correct in a Row")
            else:
                print(f"Incorrect. The correct answer was {correct_answer}.")
                streak = 0
        
        print(f"\nYou got {num_correct} out of {num_questions} correct!")

        # Difficulty scaling
        if num_correct >= level_up_threshold:
            print("Great job! You're leveling up!")
            if level == "easy":
                level = "medium"
            elif level == "medium":
                level = "hard"
            print(f"New level: {level.title()}")

        # Unlock more achievements
        if score >= 50 and "Score 50 Points" not in achievements:
            achievements.append("Score 50 Points")
            show_achievement_message("Score 50 Points")

        print(f"Your current score: {score}")
        
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print(f"Thanks for playing, {player_name}! Your final score is {score}.")
            break

# Run the game
math_game()
