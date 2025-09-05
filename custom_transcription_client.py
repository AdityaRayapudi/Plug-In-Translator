from whisper_live.client import TranscriptionTeeClient, TranscriptionClient, Client


class CustomTranscriptionTeeClient(TranscriptionTeeClient):
    def __init__(self, clients, input_device_index = 0, save_output_recording=False, output_recording_filename="./output_recording.wav", mute_audio_playback=False):
        super().__init__(clients, save_output_recording, output_recording_filename, mute_audio_playback)
        try:
            self.stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                input_device_index = input_device_index
            )
        except OSError as error:
            print(f"[WARN]: Unable to access microphone. {error}")
            self.stream = None


class CustomTranscriptionClient(CustomTranscriptionTeeClient):
   def __init__(self, host, port, input_device_index = 0, lang=None, translate=False, model="small", use_vad=True, use_wss=False, save_output_recording=False, output_recording_filename="./output_recording.wav", output_transcription_path="./output.srt", log_transcription=True, max_clients=4, max_connection_time=600, mute_audio_playback=False, send_last_n_segments=10, no_speech_thresh=0.45, clip_audio=False, same_output_threshold=10, transcription_callback=None):
        self.client = Client(
            host,
            port,
            lang,
            translate,
            model,
            srt_file_path=output_transcription_path,
            use_vad=use_vad,
            use_wss=use_wss,
            log_transcription=log_transcription,
            max_clients=max_clients,
            max_connection_time=max_connection_time,
            send_last_n_segments=send_last_n_segments,
            no_speech_thresh=no_speech_thresh,
            clip_audio=clip_audio,
            same_output_threshold=same_output_threshold,
            transcription_callback=transcription_callback,
        )

        if save_output_recording and not output_recording_filename.endswith(".wav"):
            raise ValueError(f"Please provide a valid `output_recording_filename`: {output_recording_filename}")
        if not output_transcription_path.endswith(".srt"):
            raise ValueError(f"Please provide a valid `output_transcription_path`: {output_transcription_path}. The file extension should be `.srt`.")
        CustomTranscriptionTeeClient.__init__(
            self,
            [self.client],
            input_device_index,
            save_output_recording=save_output_recording,
            output_recording_filename=output_recording_filename,
            mute_audio_playback=mute_audio_playback
        )