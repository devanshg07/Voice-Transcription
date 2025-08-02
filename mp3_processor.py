import os
import time
import threading
from pathlib import Path
from typing import Union, Optional
import pyaudio
import wave


class MP3Processor:
    """
    Basic MP3 processor that can absorb MP3 input and record audio.
    """
    
    def __init__(self):
        self.supported_extensions = {'.mp3'}
        self.audio = pyaudio.PyAudio()
        self.recording = False
        self.frames = []
        
    def __del__(self):
        """Clean up audio resources."""
        if hasattr(self, 'audio'):
            self.audio.terminate()
    
    def record_audio(self, output_file: str = "recorded_audio.wav", 
                    sample_rate: int = 44100, channels: int = 1, 
                    chunk_size: int = 1024) -> bool:
        """
        Record audio from microphone until stopped.
        
        Args:
            output_file: Output WAV file path
            sample_rate: Audio sample rate
            channels: Number of audio channels (1=mono, 2=stereo)
            chunk_size: Size of audio chunks to process
            
        Returns:
            bool: True if recording was successful
        """
        try:
            print("🎤 Recording started... Speak now!")
            print("Press Ctrl+C to stop recording")
            
            # Open audio stream
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk_size
            )
            
            self.recording = True
            self.frames = []
            
            print("Recording... (Press Ctrl+C to stop)")
            
            try:
                while self.recording:
                    data = stream.read(chunk_size)
                    self.frames.append(data)
                    
            except KeyboardInterrupt:
                print("\n⏹️  Recording stopped!")
                
            finally:
                # Clean up
                stream.stop_stream()
                stream.close()
                
                # Save the recorded audio
                if self.frames:
                    self._save_audio(output_file, sample_rate, channels)
                    print(f"✅ Audio saved to: {output_file}")
                    return True
                else:
                    print("❌ No audio was recorded")
                    return False
                    
        except Exception as e:
            print(f"❌ Error recording audio: {e}")
            return False
    
    def _save_audio(self, filename: str, sample_rate: int, channels: int):
        """Save recorded audio to WAV file."""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(self.frames))
    
    def stop_recording(self):
        """Stop the current recording."""
        self.recording = False
    
    def absorb_mp3(self, file_path: Union[str, Path]) -> bool:
        """
        Absorb an MP3 file without reading its content.
        
        Args:
            file_path: Path to the MP3 file
            
        Returns:
            bool: True if file is successfully absorbed, False otherwise
        """
        try:
            # Convert to Path object for easier handling
            path = Path(file_path)
            
            # Check if file exists
            if not path.exists():
                print(f"Error: File '{path}' does not exist")
                return False
            
            # Check if it's actually an MP3 file
            if path.suffix.lower() not in self.supported_extensions:
                print(f"Error: File '{path}' is not an MP3 file")
                return False
            
            # Get file size to confirm it's not empty
            file_size = path.stat().st_size
            if file_size == 0:
                print(f"Error: File '{path}' is empty")
                return False
            
            print(f"Successfully absorbed MP3 file: {path}")
            print(f"File size: {file_size} bytes")
            return True
            
        except Exception as e:
            print(f"Error absorbing MP3 file: {e}")
            return False
    
    def absorb_multiple_mp3(self, file_paths: list) -> dict:
        """
        Absorb multiple MP3 files.
        
        Args:
            file_paths: List of paths to MP3 files
            
        Returns:
            dict: Results for each file
        """
        results = {}
        
        for file_path in file_paths:
            success = self.absorb_mp3(file_path)
            results[str(file_path)] = success
            
        return results


def absorb_mp3_file(file_path: Union[str, Path]) -> bool:
    """
    Simple function to absorb a single MP3 file.
    
    Args:
        file_path: Path to the MP3 file
        
    Returns:
        bool: True if successful, False otherwise
    """
    processor = MP3Processor()
    return processor.absorb_mp3(file_path)


def record_and_save(output_file: str = "recorded_audio.wav") -> bool:
    """
    Simple function to record audio and save it.
    
    Args:
        output_file: Output WAV file path
        
    Returns:
        bool: True if successful, False otherwise
    """
    processor = MP3Processor()
    return processor.record_audio(output_file)


# Example usage
if __name__ == "__main__":
    # Example of how to use the module
    processor = MP3Processor()
    
    print("🎵 MP3 Processor Module")
    print("======================")
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Record audio (speak and press Ctrl+C to stop)")
    print("2. Process existing MP3 file")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n🎤 Starting audio recording...")
        print("Speak into your microphone, then press Ctrl+C to stop recording")
        
        success = processor.record_audio("my_recording.wav")
        if success:
            print("✅ Recording completed successfully!")
        else:
            print("❌ Recording failed")
            
    elif choice == "2":
        # Example file path (replace with actual MP3 file)
        example_file = "example.mp3"
        
        # Check if example file exists (for demonstration)
        if os.path.exists(example_file):
            success = processor.absorb_mp3(example_file)
            print(f"Absorption result: {success}")
        else:
            print(f"Example file '{example_file}' not found")
            print("To test, place an MP3 file in the same directory and update the filename")
    
    else:
        print("Invalid choice. Please run again and select 1 or 2.") 