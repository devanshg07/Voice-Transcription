import os
import wave
import numpy as np
import time
import threading

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️  sounddevice not available. Install with: pip install sounddevice")


class AudioRecorder:
    """
    Simple audio recorder that records microphone input and replays it.
    """
    
    def __init__(self):
        self.audio_data = None
        self.sample_rate = 44100
        self.channels = 1
        self.recording = False
        self.frames = []
        
    def record_audio_interactive(self) -> bool:
        """
        Record audio from microphone until stopped by user.
        
        Returns:
            bool: True if recording was successful
        """
        if not AUDIO_AVAILABLE:
            print("❌ Audio recording not available. Install sounddevice: pip install sounddevice")
            return False
            
        try:
            print("🎤 Press Enter to start recording...")
            input()
            
            print("🎤 Recording started! Press Enter again to stop...")
            
            # Start recording in a separate thread
            self.recording = True
            self.frames = []
            
            # Start recording thread
            record_thread = threading.Thread(target=self._record_thread)
            record_thread.start()
            
            # Wait for user to press Enter to stop
            input()
            
            # Stop recording
            self.recording = False
            record_thread.join()
            
            if self.frames:
                # Convert frames to numpy array
                self.audio_data = np.concatenate(self.frames, axis=0)
                print("✅ Recording completed!")
                return True
            else:
                print("❌ No audio was recorded")
                return False
                    
        except Exception as e:
            print(f"❌ Error recording audio: {e}")
            return False
    
    def _record_thread(self):
        """Record audio in a separate thread."""
        try:
            with sd.InputStream(samplerate=self.sample_rate, 
                              channels=self.channels, 
                              dtype='int16',
                              blocksize=1024) as stream:
                
                while self.recording:
                    data, overflowed = stream.read(1024)
                    if overflowed:
                        print("⚠️  Audio buffer overflow")
                    self.frames.append(data)
                    
        except Exception as e:
            print(f"❌ Error in recording thread: {e}")
    
    def save_audio(self, filename: str = "recorded_audio.wav") -> bool:
        """
        Save recorded audio to WAV file (optional).
        
        Args:
            filename: Output WAV file path
            
        Returns:
            bool: True if save was successful
        """
        if self.audio_data is None:
            print("❌ No audio data to save. Record audio first.")
            return False
            
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(self.sample_rate)
                wf.writeframes(self.audio_data.tobytes())
            
            print(f"✅ Audio saved to: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving audio: {e}")
            return False
    
    def replay_audio(self) -> bool:
        """
        Replay the recorded audio directly from memory.
        
        Returns:
            bool: True if replay was successful
        """
        if self.audio_data is None:
            print("❌ No audio data to replay. Record audio first.")
            return False
            
        try:
            print("🔊 Replaying recorded audio...")
            
            # Play the recorded audio directly from memory
            sd.play(self.audio_data, self.sample_rate)
            sd.wait()  # Wait for playback to complete
            
            print("✅ Audio replay completed!")
            return True
            
        except Exception as e:
            print(f"❌ Error replaying audio: {e}")
            return False


def main():
    """Main function to record and replay audio."""
    
    print("🎵 Simple Audio Recorder")
    print("=======================")
    print("Press Enter to start recording, then press Enter again to stop.")
    
    recorder = AudioRecorder()
    
    # Record audio
    if recorder.record_audio_interactive():
        # Replay audio directly from memory
        print("\n" + "="*50)
        recorder.replay_audio()
        
        # Ask if user wants to save
        save_choice = input("\nDo you want to save the recording? (y/n): ").strip().lower()
        if save_choice in ['y', 'yes']:
            filename = input("Enter filename (default: my_recording.wav): ").strip() or "my_recording.wav"
            recorder.save_audio(filename)
        else:
            print("Recording not saved.")
    else:
        print("❌ Recording failed. Cannot proceed.")


if __name__ == "__main__":
    main() 