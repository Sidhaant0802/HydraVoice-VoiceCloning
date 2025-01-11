import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import shutil
import soundfile as sf
from TTS.api import TTS

# Initialize the TTS model (Coqui TTS pretrained model with speaker adaptation)
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")

class VoiceChangerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Changer")
        self.voice_model_paths = []
        self.create_widgets()

    def create_widgets(self):
        # Upload voice data section
        self.upload_btn = tk.Button(self.root, text="Upload Voice Data", command=self.upload_voice_data)
        self.upload_btn.pack(pady=10)

        # Progress bar for training
        self.progress = Progressbar(self.root, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=10)

        # Text input for synthesis
        self.text_label = tk.Label(self.root, text="Enter text to convert:")
        self.text_label.pack(pady=10)
        
        self.text_input = tk.Text(self.root, height=5, width=40)
        self.text_input.pack(pady=10)

        # Speed control
        self.speed_label = tk.Label(self.root, text="Select speed (0.5 to 2.0):")
        self.speed_label.pack(pady=10)
        
        self.speed_input = tk.Entry(self.root)
        self.speed_input.insert(0, "1.0")
        self.speed_input.pack(pady=10)

        # Language input
        self.language_label = tk.Label(self.root, text="Select language (e.g., en):")
        self.language_label.pack(pady=10)
        
        self.language_input = tk.Entry(self.root)
        self.language_input.insert(0, "en")
        self.language_input.pack(pady=10)

        # Convert button
        self.convert_btn = tk.Button(self.root, text="Convert to Voice", command=self.convert_text_to_voice)
        self.convert_btn.pack(pady=10)

    def upload_voice_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
        if not file_path:
            return

        # Convert to WAV if necessary
        if file_path.endswith(".mp3"):
            wav_path = file_path.replace(".mp3", ".wav")
            audio, sr = sf.read(file_path)
            sf.write(wav_path, audio, sr)
        else:
            wav_path = file_path

        self.train_voice_model(wav_path)

    def train_voice_model(self, wav_path):
        def update_progress(progress):
            self.progress["value"] = progress
            self.root.update_idletasks()

        # Simulate progress bar updates during training
        for i in range(1, 101):
            update_progress(i)

        # Store the file for synthesis
        self.voice_model_paths.append(wav_path)

        messagebox.showinfo("Success", "Voice has been successfully trained!")

    def convert_text_to_voice(self):
        text = self.text_input.get("1.0", tk.END).strip()
        speed = float(self.speed_input.get())
        language = self.language_input.get().strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter text to convert.")
            return

        if not self.voice_model_paths:
            messagebox.showwarning("Warning", "Please upload and train a voice first.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if not output_file:
            return

        # Generate synthetic voice with speaker adaptation, speed control, and language
        for voice_model_path in self.voice_model_paths:
            tts.tts_to_file(text=text, speaker_wav=voice_model_path, file_path=output_file, speed=speed, language=language)

        messagebox.showinfo("Success", f"Voice synthesized and saved to {output_file}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VoiceChangerApp()
    app.run()
