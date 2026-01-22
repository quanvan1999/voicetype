import base64
import os

# Function to encode image to base64 to embed directly in HTML
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

# Load images
img_dropdown = get_base64_image("dropdown-menu.png")
img_recording = get_base64_image("start-recording.png")
img_transcribing = get_base64_image("start-transcribing.png")
img_general = get_base64_image("general-setting.png")
img_history = get_base64_image("history-setting.png")

# HTML Content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LocalTranscript (VoiceType) Manual</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .container {{
            background: #ffffff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ border-bottom: 2px solid #eaeaea; padding-bottom: 10px; color: #1a1a1a; }}
        h2 {{ color: #2c3e50; margin-top: 30px; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
        h3 {{ color: #444; margin-top: 25px; }}
        code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 4px; font-family: monospace; color: #d63384; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; border: 1px solid #ddd; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 8px; }}
        .img-container {{ text-align: center; margin: 20px 0; }}
        img {{ max-width: 100%; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.15); border: 1px solid #ddd; }}
        .flex-imgs {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }}
        .caption {{ font-size: 0.9em; color: #666; margin-top: 5px; font-style: italic; text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f8f9fa; font-weight: bold; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.85em; font-weight: bold; color: white; }}
        .badge-red {{ background-color: #e74c3c; }}
        .badge-blue {{ background-color: #3498db; }}
    </style>
</head>
<body>

<div class="container">
    <h1>LocalTranscript (VoiceType)</h1>
    <p><strong>macOS menu bar app for Vietnamese/English speech-to-text dictation.</strong> Hold a hotkey, speak, release — text appears at your cursor. Runs 100% offline using WhisperKit on Apple Silicon.</p>

    <h2>Features</h2>
    <ul>
        <li><strong>Hold-to-talk</strong>: Hold Option+Space to record, release to transcribe</li>
        <li><strong>Toggle mode</strong>: Press to start recording, press again to stop</li>
        <li><strong>Universal text insertion</strong>: Works in any app via Accessibility API</li>
        <li><strong>100% offline</strong>: All processing on-device with CoreML-optimized Whisper models</li>
        <li><strong>Vietnamese + English</strong>: Supports both languages with automatic detection</li>
        <li><strong>Menu bar app</strong>: Minimal UI, always accessible from menu bar</li>
        <li><strong>Floating indicator</strong>: Visual feedback during recording/transcription</li>
        <li><strong>Transcription history</strong>: Review, copy, or delete past transcriptions</li>
    </ul>

    <h2>Installation</h2>
    <h3>Download Release</h3>
    <p>Download the latest <code>.dmg</code> from Releases and drag to Applications.</p>

    <h3>Build from Source</h3>
    <pre>
# Clone the repository
git clone https://github.com/vulh1209/local-transcript.git
cd local-transcript

# Open in Xcode
open LocalTranscript/LocalTranscript.xcodeproj
    </pre>

    <h2>Usage</h2>
    
    <div class="img-container">
        <img src="data:image/png;base64,{img_dropdown}" alt="Main Interface" style="max-width: 300px;">
        <div class="caption">Main Interface on Menu Bar</div>
    </div>

    <ol>
        <li><strong>Launch the app</strong> — appears in menu bar with microphone icon.</li>
        <li><strong>Grant permissions</strong> when prompted (Microphone & Accessibility).</li>
        <li><strong>Hold Option+Space</strong> and speak.</li>
        <li><strong>Release</strong> — text is inserted at cursor.</li>
    </ol>

    <h3>Visual Feedback</h3>
    <div class="flex-imgs">
        <div style="text-align:center">
            <img src="data:image/png;base64,{img_recording}" alt="Recording" style="height: 60px;">
            <div class="caption"><span class="badge badge-red">Recording</span> Recording in progress</div>
        </div>
        <div style="text-align:center">
            <img src="data:image/png;base64,{img_transcribing}" alt="Transcribing" style="height: 60px;">
            <div class="caption"><span class="badge badge-blue">Transcribing</span> Transcribing to text</div>
        </div>
    </div>

    <h2>Configuration</h2>
    
    <h3>Hotkeys</h3>
    <table>
        <tr>
            <th>Hotkey</th>
            <th>Action</th>
        </tr>
        <tr>
            <td><code>Option + Space</code></td>
            <td>Hold to record, release to transcribe</td>
        </tr>
        <tr>
            <td><code>Option + L</code></td>
            <td>Cycle language mode (Auto → Vietnamese → English)</td>
        </tr>
    </table>

    <h3>Settings</h3>
    <p>Click the menu bar icon → <strong>Settings</strong> to configure hotkeys, modes, and models.</p>
    <div class="img-container">
        <img src="data:image/png;base64,{img_general}" alt="General Settings">
        <div class="caption">General Settings: Hotkeys, Modes, Languages</div>
    </div>

    <h3>Transcription History</h3>
    <p>You can review, copy, or delete past transcriptions in the History tab.</p>
    <div class="img-container">
        <img src="data:image/png;base64,{img_history}" alt="History">
        <div class="caption">Transcription History</div>
    </div>

    <h2>Troubleshooting</h2>
    <ul>
        <li><strong>Text not inserting (VS Code, Slack)</strong>: These apps don't fully support Accessibility API. The app automatically falls back to clipboard paste (Cmd+V).</li>
        <li><strong>Model download stuck</strong>: Check internet connection. Try a smaller model first (tiny/base).</li>
        <li><strong>Hotkey not working</strong>: Go to System Settings → Privacy & Security → Input Monitoring and ensure LocalTranscript is enabled.</li>
    </ul>
    
    <hr>
    <p style="text-align: center; color: #888; font-size: 0.9em;">Generated for LocalTranscript User Guide</p>
</div>

</body>
</html>
"""

# Save to file
filename = "LocalTranscript_Manual.html"
with open(filename, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"File created: {filename}")
