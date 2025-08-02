import os
import time
import wave
import numpy as np
from pathlib import Path
from typing import Union, Optional

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️  sounddevice not available. Install with: pip install sounddevice")


class MP3Processor:
    """
    Basic MP3 processor that can absorb MP3 input and record audio.
    """
    
    def __init__(self):
        self.supported_extensions = {'.mp3'}
        self.recording = False
        self.audio_data = None
        
    def record_audio(self, output_file: str = "recorded_audio.wav", 
                    sample_rate: int = 44100, channels: int = 1) -> bool:
        """
        Record audio from microphone until stopped.
        
        Args:
            output_file: Output WAV file path
            sample_rate: Audio sample rate
            channels: Number of audio channels (1=mono, 2=stereo)
            
        Returns:
            bool: True if recording was successful
        """
        if not AUDIO_AVAILABLE:
            print("❌ Audio recording not available. Install sounddevice: pip install sounddevice")
            return False
            
        try:
            print("🎤 Recording started... Speak now!")
            print("Press Ctrl+C to stop recording")
            
            # Record audio
            print("Recording... (Press Ctrl+C to stop)")
            
            try:
                # Record audio using sounddevice
                audio_data = sd.rec(int(sample_rate * 60), samplerate=sample_rate, 
                                  channels=channels, dtype='int16')
                sd.wait()  # Wait for recording to complete
                
                # Save the recorded audio
                self._save_audio_simple(output_file, audio_data, sample_rate, channels)
                print(f"✅ Audio saved to: {output_file}")
                return True
                
            except KeyboardInterrupt:
                print("\n⏹️  Recording stopped!")
                return False
                    
        except Exception as e:
            print(f"❌ Error recording audio: {e}")
            return False
    
    def _save_audio_simple(self, filename: str, audio_data, sample_rate: int, channels: int):
        """Save recorded audio to WAV file using numpy and wave."""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())
    
    def record_audio_interactive(self, output_file: str = "recorded_audio.wav", 
                               sample_rate: int = 44100, duration: int = 10) -> bool:
        """
        Record audio for a specified duration.
        
        Args:
            output_file: Output WAV file path
            sample_rate: Audio sample rate
            duration: Recording duration in seconds
            
        Returns:
            bool: True if recording was successful
        """
        if not AUDIO_AVAILABLE:
            print("❌ Audio recording not available. Install sounddevice: pip install sounddevice")
            return False
            
        try:
            print(f"🎤 Recording for {duration} seconds... Speak now!")
            print("Recording will stop automatically...")
            
            # Record audio for specified duration
            audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, 
                              channels=1, dtype='int16')
            sd.wait()  # Wait for recording to complete
            
            # Save the recorded audio
            self._save_audio_simple(output_file, audio_data, sample_rate, 1)
            print(f"✅ Audio saved to: {output_file}")
            return True
                    
        except Exception as e:
            print(f"❌ Error recording audio: {e}")
            return False
    
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


def record_and_save(output_file: str = "recorded_audio.wav", duration: int = 10) -> bool:
    """
    Simple function to record audio and save it.
    
    Args:
        output_file: Output WAV file path
        duration: Recording duration in seconds
        
    Returns:
        bool: True if successful, False otherwise
    """
    processor = MP3Processor()
    return processor.record_audio_interactive(output_file, duration=duration)


# Example usage
if __name__ == "__main__":
    # Example of how to use the module
    processor = MP3Processor()
    
    print("🎵 MP3 Processor Module (Simple Version)")
    print("=======================================")
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Record audio (10 seconds)")
    print("2. Record audio (custom duration)")
    print("3. Process existing MP3 file")
    
    choice = input("Enter your choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        print("\n🎤 Starting audio recording...")
        print("Speak into your microphone for 10 seconds")
        
        success = processor.record_audio_interactive("my_recording.wav", duration=10)
        if success:
            print("✅ Recording completed successfully!")
        else:
            print("❌ Recording failed")
            
    elif choice == "2":
        try:
            duration = int(input("Enter recording duration in seconds: "))
            print(f"\n🎤 Starting audio recording for {duration} seconds...")
            print("Speak into your microphone")
            
            success = processor.record_audio_interactive("my_recording.wav", duration=duration)
            if success:
                print("✅ Recording completed successfully!")
            else:
                print("❌ Recording failed")
        except ValueError:
            print("❌ Invalid duration. Please enter a number.")
            
    elif choice == "3":
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
        print("Invalid choice. Please run again and select 1, 2, or 3.") 