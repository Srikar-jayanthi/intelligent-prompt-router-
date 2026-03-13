import sys
from router import process_message

TEST_MESSAGES = [
    "how do i sort a list of objects in python?",
    "explain this sql query for me",
    "This paragraph sounds awkward, can you help me fix it?",
    "I'm preparing for a job interview, any tips?",
    "what's the average of these numbers: 12, 45, 23, 67, 34",
    "Help me make this better.",
    "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
    "hey",
    "Can you write me a poem about clouds?",
    "Rewrite this sentence to be more professional.",
    "I'm not sure what to do with my career.",
    "what is a pivot table",
    "fxi thsi bug pls: for i in range(10) print(i)",
    "How do I structure a cover letter?",
    "My boss says my writing is too verbose.",
]

def run_tests():
    print("Running 15 test messages...")
    for i, msg in enumerate(TEST_MESSAGES, 1):
        print(f"\nTest {i}: {msg}")
        response = process_message(msg)
        print(f"Response: {response}")
    print("\nTests complete. Check route_log.jsonl for logs.")

def interactive_mode():
    print("LLM Prompt Router Interactive Mode")
    print("Type 'exit' to quit.")
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            response = process_message(user_input)
            print(f"\nRouter: {response}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        interactive_mode()
