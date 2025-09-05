from piper import PiperVoice
from googletrans import Translator
import sounddevice as sd
import asyncio

class VoiceBox:
    def __init__(self, src_lang:str, dest_lang:str, voice_path:str, output_device:int):
        self.__current_text = ""
        self.__last_time = 0
        self.__src_lang = src_lang
        self.__dest_lang = dest_lang
        self.__voice = PiperVoice.load(voice_path)
        sd.default.device = output_device
    
    def get_src_lang(self):
        return self.__src_lang
    
    def get_dest_lang(self):
        return self.__dest_lang
    
    def set_src_lang(self, lang:str):
        self.__src_lang = lang
    
    def set_dest_lang(self, lang:str):
        self.__dest_lang = lang
    
    def set_device(self, device_index):
        sd.default.device = device_index

    async def translate_current_text(self, text):
        async with Translator() as translator:
            result = await translator.translate(text=text, src=self.__src_lang, dest=self.__dest_lang)
            return result.text
    
    def process_text(self, metadata):
        for chunck in metadata:
            end_time = float(chunck['end'])
            print(end_time, self.__last_time)

            if end_time > self.__last_time:
                self.__last_time = end_time

                translated_text = asyncio.run(self.translate_current_text(chunck['text']))
                return translated_text
        
        return None


    def process_live_text(self, text, metadata):
        if text == self.__current_text:
            return
        
        self.__current_text = text
        translated_text = asyncio.run(self.translate_current_text())
        return translated_text

    def use_voice(self, text:str):
        print(text)
        for chunk in self.__voice.synthesize(text):
            sd.play(chunk.audio_float_array, chunk.sample_rate)
            sd.wait()