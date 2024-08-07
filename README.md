
# YouTube Downloader

A Python application to download YouTube videos and their transcripts. The application provides a GUI built with `tkinter` and `customtkinter`, and uses `pytube` for downloading videos and `youtube-transcript-api` for fetching video transcripts.

## Features

- Download YouTube videos in various resolutions
- Fetch and display video transcripts
- Save transcripts to a text file
- Delete downloaded videos and transcripts
- Automatically populate the URL input box when a YouTube video is opened in the browser

## Requirements

- Python 3.6 or higher
- `pip` package manager

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Create a virtual environment:**

   - On Windows:
     ```sh
     python -m venv venv
     .env\Scriptsctivate
     ```
   - On macOS and Linux:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Flask server:**

   The Flask server is integrated with the main application. It will start automatically when you run the application.

2. **Run the application:**

   ```sh
   python YoutubeDownloader.py
   ```

3. **Using the Application:**

   - **Enter YouTube URL:** Enter the URL of the YouTube video you wish to download in the input box.
   - **Download Video:** Select the desired resolution from the dropdown and click the `Download` button.
   - **View Transcript:** After the download completes, the transcript will be displayed in the text box.
   - **Save Transcript:** Click the `SAVE` button to save the transcript to a text file.
   - **Delete Files:** Use the `DELETE Video` button to delete the downloaded video and the `DELETE Transcript` button to delete the saved transcript.

## Browser Extension (Optional)

To automatically populate the URL input box with the URL of the currently opened YouTube video in your browser, you can use a browser extension.

1. **Create a browser extension:**

   - **manifest.json:**
     ```json
     {
       "manifest_version": 3,
       "name": "YouTube URL Capturer",
       "version": "1.0",
       "permissions": ["activeTab", "scripting"],
       "background": {
         "service_worker": "background.js"
       }
     }
     ```

   - **background.js:**
     ```javascript
     chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
       if (changeInfo.status === 'complete' && tab.url.includes('youtube.com/watch')) {
         chrome.scripting.executeScript({
           target: {tabId: tab.id},
           func: sendUrlToApp,
           args: [tab.url]
         });
       }
     });

     function sendUrlToApp(url) {
       fetch('http://localhost:5000/url', {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
         },
         body: JSON.stringify({ url: url }),
       });
     }
     ```

2. **Load the extension in your browser:**

   - Open `chrome://extensions/` in Google Chrome.
   - Enable `Developer mode` in the top right corner.
   - Click `Load unpacked` and select the directory containing your extension files (`manifest.json` and `background.js`).

## Creating an Executable (.exe) File

You can create an executable (.exe) file from your Python script using `PyInstaller`.

### Step 1: Install PyInstaller

First, ensure you have `PyInstaller` installed in your virtual environment:

pip install pyinstaller
```
### Step 2: Create the Executable

Navigate to your project directory and run `PyInstaller`:

```sh
cd path/to/your/project
```

This will generate a `dist` directory containing the `main.exe` file.
### Customizing the Spec File

If your project has multiple dependencies or files, you might need to customize the `.spec` file generated by `PyInstaller`. Here’s an example of a customized `.spec` file:

```python
# main.spec

# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['YoutubeDownloader.py'],
    pathex=['/path/to/your/project'],
    binaries=[],
    datas=[('path/to/your/resource/folder', 'resource')],
    hiddenimports=['pytube', 'customtkinter', 'youtube_transcript_api', 'flask'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Youtube Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon='path/to/your/icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Youtube Downloader'
)
```

### Building the Executable with Spec File

If you need to use a `.spec` file, run:
```sh
pyinstaller main.spec
```

This will generate an executable with the configurations specified in the `.spec` file.


After building the executable, you can find it in the `dist` directory. Run the `.exe` file to ensure it works as expected.
## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
