import speech_recognition as sr
import subprocess
import time
import os

# --- CONFIGURATION ---
ADB_PATH = r"C:\Users\Jahan\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def run_adb(command):
    full_cmd = f'"{ADB_PATH}" {command}'
    subprocess.run(full_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def open_maps_search(food_type):
    print(f"[*] Command received: '{food_type}'")
    print(f"[*] Opening Maps for: 'Best {food_type} near me'")
    
    # Smart Search Intent
    formatted_query = f"Best {food_type} near me".replace(" ", "+")
    cmd = f"shell am start -a android.intent.action.VIEW -d \"https://www.google.com/maps/search/{formatted_query}\""
    run_adb(cmd)

def listen_for_command():
    recognizer = sr.Recognizer()
    
    # Use the default microphone
    with sr.Microphone() as source:
        print("\n" + "="*40)
        print("🎤 LISTENING... (Speak now: 'Pizza', 'Biryani')")
        print("="*40)
        
        # Adjust for background noise automatically
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            # Listen for 5 seconds max
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("[*] Processing voice...")
            
            # Convert speech to text (requires internet)
            text = recognizer.recognize_google(audio)
            print(f"✅ You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("[-] No speech detected.")
            return None
        except sr.UnknownValueError:
            print("[-] Could not understand audio.")
            return None
        except Exception as e:
            print(f"[-] Error: {e}")
            return None

def main():
    print("========================================")
    print("   🎙️ GOURMET VOICE AGENT (PC)        ")
    print("========================================")
    
    # Connect to phone
    print("[*] Connecting to phone...")
    run_adb("devices")

    while True:
        input("\nPress ENTER to start listening (or Ctrl+C to quit)...")
        
        # 1. Listen to Voice
        command = listen_for_command()
        
        # 2. Execute on Phone
        if command:
            open_maps_search(command)
        else:
            print("[-] Try again.")

if __name__ == "__main__":
    main()