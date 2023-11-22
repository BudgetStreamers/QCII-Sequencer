import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Add this line
from pygame import mixer
import numpy as np
import scipy.io.wavfile as wav

class WAVPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("QC2 Sequencer and Generator")

        # Title
        self.title_label = tk.Label(self.master, text="Quik-Call II Sequencer and Generator", font=("Helvetica", 18, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=5, pady=0.1)

        # Sub-text
        self.subtext_label = tk.Label(self.master, text="Made by Brandon Crocker / K4CPN", font=("Helvetica", 10))
        self.subtext_label.grid(row=1, column=0, columnspan=5, pady=0.1)

        # Placeholder for the text logo
        self.logo_label = tk.Label(self.master, text="Version 1.0", font=("Helvetica", 8))
        self.logo_label.grid(row=2, column=0, columnspan=5, pady=0.1)

        # File selection window
        self.file_label = tk.Label(self.master, text="Available Files:")
        self.file_label.grid(row=3, column=0, pady=0)
        self.file_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE)
        self.file_listbox.grid(row=4, column=0, padx=10, pady=10, rowspan=4)

        # Load WAV Files button
        self.load_button = tk.Button(self.master, text="Load WAV Files", command=self.load_files)
        self.load_button.grid(row=4, column=1, pady=2)

        # Play Selected button
        self.play_selected_button = tk.Button(self.master, text="Play Selected File", command=self.play_selected_file)
        self.play_selected_button.grid(row=5, column=1, pady=2)

        # Add to Sequence button
        self.add_to_sequence_button = tk.Button(self.master, text="Add to Sequence", command=self.add_to_sequence)
        self.add_to_sequence_button.grid(row=6, column=1, pady=2)

        # Remove from Sequence button
        self.remove_from_sequence_button = tk.Button(self.master, text="Remove from Sequence", command=self.remove_from_sequence)
        self.remove_from_sequence_button.grid(row=7, column=1, pady=2)

        # Clear Sequence button
        self.clear_sequence_button = tk.Button(self.master, text="Clear Sequence", command=self.clear_sequence)
        self.clear_sequence_button.grid(row=8, column=1, pady=5)
        
        # Time interval entry widget
        self.interval_label = tk.Label(self.master, text="Sequence Interval (seconds):")
        self.interval_label.grid(row=9, column=1, pady=5)
        self.interval_entry = tk.Entry(self.master)
        self.interval_entry.insert(tk.END, "2")  # Default interval
        self.interval_entry.grid(row=9, column=2, pady=5)

        # Play Sequence button
        self.play_sequence_button = tk.Button(self.master, text="Play Sequence", command=self.play_sequence)
        self.play_sequence_button.grid(row=8, column=2, pady=5)
        
        # Divider
        ttk.Separator(self.master, orient='horizontal').grid(row=10, column=0, columnspan=5, sticky='ew', pady=5)

        self.tone1_frequency_label = tk.Label(self.master, text="Tone 1 Frequency:")
        self.tone1_frequency_label.grid(row=11, column=0, pady=5)
        self.tone1_frequency_entry = tk.Entry(self.master)
        self.tone1_frequency_entry.insert(tk.END, "851")  # Default frequency for tone 1
        self.tone1_frequency_entry.grid(row=11, column=1, pady=5)

        self.tone2_frequency_label = tk.Label(self.master, text="Tone 2 Frequency:")
        self.tone2_frequency_label.grid(row=12, column=0, pady=5)
        self.tone2_frequency_entry = tk.Entry(self.master)
        self.tone2_frequency_entry.insert(tk.END, "1349")  # Default frequency for tone 2
        self.tone2_frequency_entry.grid(row=12, column=1, pady=5)

        # Generate Quik-Call II Tone Set button
        self.generate_tone_button = tk.Button(self.master, text="Generate Quik-Call II Tone Set", command=self.generate_tone_set)
        self.generate_tone_button.grid(row=13, column=1, pady=5)

        # Sequence window
        self.file_label = tk.Label(self.master, text="Sequence Order:")
        self.file_label.grid(row=3, column=2, pady=0)
        self.sequence_listbox = tk.Listbox(self.master)
        self.sequence_listbox.grid(row=4, column=2, padx=10, pady=10, rowspan=4)

        self.file_paths = []
        self.mixer = mixer
        self.mixer.init()

        # Selected file index
        self.selected_index = None

        # Selected files in the order of the sequence
        self.sequence_order = []

    def load_files(self):
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            self.file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".wav")]

            # Clear the existing content in the file listbox
            self.file_listbox.delete(0, tk.END)

            for file_path in self.file_paths:
                file_name = os.path.splitext(os.path.basename(file_path))[0]  # Remove file extension
                self.file_listbox.insert(tk.END, file_name)

    def play_sequence(self):
        interval = float(self.interval_entry.get())  # Get the user-specified interval

        for index in self.sequence_order:
            file_path = self.file_paths[index]
            sound = mixer.Sound(file_path)

            sound.play()
            time.sleep(sound.get_length() + interval)

    def play_selected_file(self):
        selected_index = self.file_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "Please select a file to play.")
            return

        file_path = self.file_paths[selected_index[0]]
        sound = self.mixer.Sound(file_path)
        sound.play()

    def add_to_sequence(self):
        selected_index = self.file_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "Please select a file to add to the sequence.")
            return

        # Add the selected file to the end of the sequence
        self.sequence_order.append(selected_index[0])

        # Update the sequence listbox to show the updated sequence order
        self.update_sequence_listbox()

    def remove_from_sequence(self):
        selected_indices = self.sequence_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Info", "Please select a file to remove from the sequence.")
            return

        # Remove selected files from the sequence
        for index in selected_indices:
            if index < len(self.sequence_order):
                del self.sequence_order[index]

        # Update the sequence listbox to show the updated sequence order
        self.update_sequence_listbox()

    def clear_sequence(self):
        # Clear the sequence order and update the sequence listbox
        self.sequence_order = []
        self.update_sequence_listbox()

    def update_sequence_listbox(self):
        # Clear the existing content in the sequence listbox
        self.sequence_listbox.delete(0, tk.END)

        # Insert the updated sequence order into the sequence listbox
        for index in self.sequence_order:
            file_name = os.path.splitext(os.path.basename(self.file_paths[index]))[0]  # Remove file extension
            self.sequence_listbox.insert(tk.END, file_name)

    def generate_tone_set(self):
        # Get the desired WAV file name from the user
        wav_file_name = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])

        if wav_file_name:
            try:
                # Get user-specified frequencies for tone 1 and tone 2
                tone_1_frequency = float(self.tone1_frequency_entry.get())
                tone_2_frequency = float(self.tone2_frequency_entry.get())

                # Generate Quik-Call II tone set
                tone_1_duration = 1  # 1 second
                tone_2_duration = 3  # 3 seconds
                sample_rate = 44100

                # Calculate the number of samples for each tone
                tone_1_samples = int(sample_rate * tone_1_duration)
                tone_2_samples = int(sample_rate * tone_2_duration)

                # Generate tones
                time_points_1 = np.linspace(0, tone_1_duration, tone_1_samples, endpoint=False)
                time_points_2 = np.linspace(0, tone_2_duration, tone_2_samples, endpoint=False)

                tone_1 = np.sin(2 * np.pi * tone_1_frequency * time_points_1)
                tone_2 = np.sin(2 * np.pi * tone_2_frequency * time_points_2)

                # Combine tones
                tone_set = np.concatenate((tone_1, tone_2))

                # Normalize the audio to ensure values are within the valid range
                tone_set = 0.5 * tone_set / np.max(np.abs(tone_set))

                # Save the generated tone set as a WAV file
                wav.write(wav_file_name, sample_rate, (tone_set * 32767).astype(np.int16))  # Convert to 16-bit PCM

                messagebox.showinfo("Info", f"Tone set generated and saved as {os.path.basename(wav_file_name)}")
            except ValueError:
                messagebox.showerror("Error", "Invalid frequency input. Please enter valid numerical values.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WAVPlayerApp(root)
    root.mainloop()
