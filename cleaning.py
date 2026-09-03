import re
import nltk
from nltk.tokenize import sent_tokenize
from spellchecker import SpellChecker
from deepmultilingualpunctuation import PunctuationModel

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
    corrected_words = [spell.correction(word) for word in words]

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
patient_key = ["i have", "i feel", "my", "pain", "headache", "hurt", "doctor", "ask"]


def key_score(sentence, key):
    return sum(1 for word in key if word in sentence.lower())


# heuristic using keywords
def key_label(sentence):
    doctor_score = key_score(sentence, doctor_key)
    patient_score = key_score(sentence, patient_key)

    if any(word in sentence.lower() for word in {"prescribe", "diagnose", "treatment", "I believe", "this is due to",
                                                 "do you"}):
        return "Doctor"

    if any(word in sentence.lower() for word in {"i feel", "I have", "my"}):
        return "Patient"

    if doctor_score > patient_score:
        return "Doctor"
    elif patient_score > doctor_score:
        return "Patient"

    return "Unknown"


# Adding turn base logic to identify responder base on questionare
def is_question(sentence):
    question_words = (
        "what", "why", "how", "when", "where", "do", "does", "is", "are", "have", "can", "could", "should", "would",
        "will", "do you")
    stripped = sentence.strip().lower()
    return stripped.endswith('?') or stripped.startswith(question_words)


# need to double check this part
def opposite_speaker(speaker):
    if speaker == "Doctor":
        return "Patient"
    elif speaker == "Patient":
        return "Doctor"
    else:
        return "Unknown"


# Using previous speaker to work out speaker
def multi_turn_simulation(transcript):
    speakers = []
    last_speaker = None
    last_question = None
    expecting_response = False

    for sentence in transcript:
        speaker = key_label(sentence)

        if is_question(sentence):
            last_speaker = speaker if speaker != "Unknown" else last_speaker
            expecting_response = True

        elif expecting_response:

            if speaker == "Unknown" and last_speaker:
                speaker = opposite_speaker(last_speaker)
            expecting_response = False

        if speaker == "Unknown" and last_speaker:
            speaker = last_speaker

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
    speaker_label = multi_turn_simulation(sentences)

    return speaker_label
