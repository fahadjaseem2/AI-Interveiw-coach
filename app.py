from speech_to_text import record_audio, speech_to_text
from llm_response import ask_llm
import os


def main():
    while True:
        user_input = input("Press Enter to record OR type exit: ")

        if user_input.lower() == "exit":
            break

        audio_file = record_audio()

        transcript = speech_to_text(audio_file)
        print(f"Question Detected: {transcript}")

        answer = ask_llm(transcript)
        print("\nAI Answer:")
        print(answer)

        os.remove(audio_file)


if __name__ == "__main__":
    main()