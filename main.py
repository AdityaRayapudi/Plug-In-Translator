from voice_box import VoiceBox
from custom_transcription_client import CustomTranscriptionClient


INPUT_DEVICE = 5
OUTPUT_DEVICE = 7

english_to_telgu = VoiceBox(
    src_lang="en", 
    dest_lang="te",
    voice_path="voices\\te_IN-venkatesh-medium.onnx",
    output_device=OUTPUT_DEVICE
)

def handle_en_to_te(text, metadata):
    print(metadata)

    te_translated_text = english_to_telgu.process_text(metadata)
    if te_translated_text != None:
        english_to_telgu.use_voice(te_translated_text)

english_to_spanish = VoiceBox(
    src_lang="en", 
    dest_lang="es",
    voice_path="voices\\es_AR-daniela-high.onnx",
    output_device=OUTPUT_DEVICE
)

def handle_en_to_es(text, metadata):
    print(text)

    te_translated_text = english_to_spanish.process_text(metadata)
    if te_translated_text != None:
        english_to_spanish.use_voice(te_translated_text)

client = CustomTranscriptionClient(
    "localhost", 
    9090, 
    input_device_index=INPUT_DEVICE,
    lang="en", 
    translate=False, 
    model="Systran/faster-whisper-base",
    transcription_callback=handle_en_to_te,
    log_transcription=False,
    no_speech_thresh=0.2,
    same_output_threshold=15
)

if __name__ == "__main__":
    print("Running Two-Way-Translator")

    client()