"""
Test Voice Transcription Endpoint
"""
import requests
import wave
import os
from reportlab.pdfgen import canvas

BASE_URL = "http://localhost:8000"

def create_silent_wav(filename="verify_audio.wav", duration=1):
    """Create a short silent WAV file"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(44100)
        # Write silence
        data = b'\x00\x00' * 44100 * duration
        wav_file.writeframes(data)
    print(f"Created silent WAV: {filename}")
    return filename

def create_test_pdf(filename="verify_assignment.pdf"):
    """Create a simple test PDF"""
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Voice Test Assignment")
    c.drawString(100, 700, "Please explain the concept of recursion.")
    c.save()
    print(f"Created test PDF: {filename}")
    return filename

def test_voice_endpoint():
    print("\nTesting Voice Analysis Endpoint...")
    
    audio_file = create_silent_wav()
    pdf_file = create_test_pdf()
    
    try:
        files = {
            'file': (pdf_file, open(pdf_file, 'rb'), 'application/pdf'),
            'voice_file': (audio_file, open(audio_file, 'rb'), 'audio/wav')
        }
        
        # Note: Since we are sending silence, we don't expect a specific response to the audio,
        # but we expect the API to process it without error and answer based on the PDF/Prompt.
        
        response = requests.post(
            f"{BASE_URL}/api/v1/assignment/analyze-with-voice",
            files=files,
            data={'use_research': 'false'}
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"Response: {result.get('response')}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Test Error: {e}")
    finally:
        # Cleanup
        if os.path.exists(audio_file):
            os.remove(audio_file)
        if os.path.exists(pdf_file):
            os.remove(pdf_file)

if __name__ == "__main__":
    test_voice_endpoint()
