import re
import nltk
from nltk.tokenize import sent_tokenize
from spellchecker import SpellChecker
from deepmultilingualpunctuation import PunctuationModel
import os

nltk.data.path.append('./nltk_data')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir='./nltk_data')

# Enabling for lazy loading
model = None
spell = None


def fix_common_errors(text):
    # list of uncommon mistakes that are unlikely to be picked up in the spell checks etc, this list will grow in time
    # with user input
    corrections = {
        "pause": "pores",
        "trend tinny": "tretinoin",
        "tropical helps": "topical helps",
        "bacterium": "bacteria",
        "sick acid": "salicylic acid",
        "our our": "ow ow",
        "so civic": "salicylic acid"
    }

    for error, correction in corrections.items():
        text = re.sub(rf'\b{error}\b', correction, text, flags=re.IGNORECASE)

    return text


# spell check
def spell_check_text(transcript):
    # Lazy loading
    global spell
    if spell is None:
        spell = SpellChecker()
    # basic spell checker
    words = transcript.split()
    corrected_words: str = [spell.correction(word) for word in words]

    return " ".join(corrected_words)


# grammar
def grammar_check_function(text):
    global model
    if not text.strip():
        return ""

    try:
        if model is None:
            model = PunctuationModel()
        output = model.restore_punctuation(text)
        if isinstance(output, list):
            output = " ".join(output)
        return output
    except Exception as e:
        print("Grammar check failed!", e)
        return text


def formatting_check_function(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s([?.!,])", r"\1", text)
    return text.strip()


# Speaker identification
# Common keywords
doctor_key = ["prescribe", "diagnose", "treatment", "recommend", "medication", "follow up", "symptoms", "pain",
              "suffer"]
patient_key = ["i have", "i've", "i feel", "my", "pain", "headache", "hurt", "doctor", "ask"]


def key_score(sentence, key):
    return sum(1 for word in key if word in sentence.lower())


# heuristic using keywords
def key_label(sentence):
    doctor_score = key_score(sentence, doctor_key)
    print(f"\n\nDoctor Score: {doctor_score}")
    patient_score = key_score(sentence, patient_key)
    print(f"Patient Score: {patient_score}")


    if any(word in sentence.lower() for word in {"prescribe", "diagnose", "treatment", "I believe", "this is due to",
                                                 "do you"}):
        print("\nDoctor Definite\n")
        return "Doctor"

    if any(word in sentence.lower() for word in {"i feel", "I have", "my"}):
        print("\nPatient Definite\n")
        return "Patient"

    if doctor_score > patient_score:
        return "Doctor"
    elif patient_score > doctor_score:
        return "Patient"

    return "Unknown"


# Adding turn base logic to identify responder base on questioner
# TODO: didnt detect a question
def is_question(sentence):
    question_words = (
        "what", "why", "how", "when", "where", "do", "does", "is", "are", "have", "can", "could", "should", "would",
        "will", "do you")
    stripped = sentence.strip().lower()
    return stripped.endswith('?') or stripped.startswith(question_words)


# need to double-check this part
def opposite_speaker(speaker):
    if speaker == "Doctor":
        return "Patient"
    elif speaker == "Patient":
        return "Doctor"
    else:
        return "Unknown"


# Using previous speaker to work out speaker
# TODO: Getting stuck in unknown speaker so stuck in last speaker loop. need to apply more turn base logic such as greetings etc
def multi_turn_simulation(transcript):
    speakers = []
    last_speaker = None
    last_question = None
    expecting_response = False

    for sentence in transcript:
        speaker = key_label(sentence)
        print(f"\n Last Speaker: {last_speaker}")
        print(f"Last Question: {last_question}")
        print(f"Current Speaker: {speaker}")

        if is_question(sentence):
            last_speaker = speaker if speaker != "Unknown" else last_speaker
            expecting_response = True
            print("question detected")

        elif expecting_response:

            if speaker == "Unknown" and last_speaker:
                speaker = opposite_speaker(last_speaker)
                print("speaker was unknown so switching speaker")
                print(f"new speaker: {speaker}")
            expecting_response = False

        if speaker == "Unknown" and last_speaker:
            speaker = last_speaker
            print(f"Speaker was unknown. Resorting to last speaker")

        speakers.append((speaker, sentence))
        last_speaker = speaker

    return speakers


def full_clean(raw_text):
    if isinstance(raw_text, list):
        raw_text = " ".join(raw_text)

    cleaned = fix_common_errors(raw_text)
    cleaned = spell_check_text(cleaned)
    cleaned = grammar_check_function(cleaned)
    cleaned = formatting_check_function(cleaned)

    sentences = sent_tokenize(cleaned)
    print("\nSentence:")
    print(sentences)
    speaker_label = multi_turn_simulation(sentences)
    print("\nSpeaker Label:")
    print(speaker_label)

    return speaker_label

if __name__ == "__main__":
    # 1. Use raw strings (r"...") so Windows backslashes (\U, \m, \t) don't cause errors
    # 2. Replaced 'raw_test_text_1' with 'raw_test_text.txt' (or change to your exact extension)
    input_path = r"C:\Users\mathi\OneDrive\Desktop\mediScript_test_convos\raw_test_text_1.txt"

    # 3. Added a specific filename ('cleaned_results.txt') to the output path
    output_path = r"C:\Users\mathi\OneDrive\Desktop\mediScript_test_convos\cleaned_results.txt"

    # Read the raw file
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Process the data through your cleaning function
    clean = full_clean(content)

    # Save the results to the new file
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(
            "\n".join(
                f"{speaker}: {sentence}"
                for speaker, sentence in clean
            )
        )
