from transformers import pipeline
from transformers.pipelines.audio_utils import ffmpeg_microphone_live
import sys
from event_bus import Event

class LiveTranscriber:
    def __init__(self, bus=None) -> None:
        self.device = 'cuda'
        self.bus = bus
        self.transcriber = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-small.en",
            device=self.device,
            framework='pt'
        )
        self._stop = False

    def transcribe(self, chunk_length_s=5.0, stream_chunk_s=0.25):
        sampling_rate = self.transcriber.feature_extractor.sampling_rate

        mic = ffmpeg_microphone_live(
            sampling_rate=sampling_rate,
            chunk_length_s=chunk_length_s,
            stream_chunk_s=stream_chunk_s,
        )

        print("Start speaking...")
        for item in self.transcriber(mic, generate_kwargs={"max_new_tokens": 128}):
            if not item["partial"][0]:
                if self.bus:
                    event = Event(type='user_speech', text=item['text'])
                    self.bus.push_event(event)
                else:
                    print(item["text"])

            if self._stop:
                break

    def stop(self):
        self._stop = True

if __name__ == "__main__":
    LiveTranscriber().transcribe()