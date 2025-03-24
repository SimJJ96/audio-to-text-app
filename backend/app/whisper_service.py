from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment
import numpy as np
import logging

logger = logging.getLogger(__name__)

processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")

forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")
model.config.forced_decoder_ids = forced_decoder_ids


def transcribe(file_path):
    # # Load audio file
    # audio = AudioSegment.from_file(file_path)
    # audio = audio.set_frame_rate(16000)  # Resample to 16kHz
    # audio = audio.set_channels(1)  # Convert to mono

    # # Normalize audio samples
    # samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    # samples = samples / np.max(np.abs(samples))  # Normalize to [-1.0, 1.0]

    # # Use the model and processor to transcribe the audio:
    # input = processor(samples, sampling_rate=16000, return_tensors="pt")
    # input_features = input.input_features


    # # Generate transcription 
    # predicted_ids = model.generate(input_features)
    # transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    # return transcription[0]

    try:
        logger.info(f"Starting transcription for file: {file_path}")

        # Load audio file
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(16000)  # Resample to 16kHz
        audio = audio.set_channels(1)  # Convert to mono

        # Normalize audio samples to [-1.0, 1.0]
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples = samples / np.max(np.abs(samples))

        # Use the model and processor to transcribe the audio
        input = processor(samples, sampling_rate=16000, return_tensors="pt")
        input_features = input.input_features

        # Generate transcription
        predicted_ids = model.generate(input_features)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        logger.info(f"Transcription completed for file: {file_path}")

        return transcription[0]

    except Exception as e:
        logger.error(f"Error during transcription of file {file_path}: {str(e)}", exc_info=True)
        raise