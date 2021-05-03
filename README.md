# Running gait analysis
Desktop application for evaluating your running technique from videos.

## Installation
```powershell
python3.exe -m pip install -r requirements.txt
```
### Windows:
```powershell
./setup.ps1
```
### Linux/MacOS:
```powershell
TBD
```

## Run
From root directory:
```powershell
python3.exe src/run.py
```

## Demo
To try the application, just upload the directories stored in `examples\` or upload the video and wait for the estimator to render the outputs.

![Camera position](/src/images/demo.gif)

## Usage
Uploading a video calls a pose estimator and the rendered results are saved to `uploads\` directory of the app's root folder.

One directory in this folder represents one video and should be uploaded if it already exists.

For optimal environment, follow the camera position guidelines that are demonstrated below.
![Camera position](/src/images/camera_position.png)

## License

GNU General Public License v3.0

## Contact
In case of any bugs or problems, do not hesitate to contact me.

email: radoslave0@gmail.com
