# Virtual Mouse Using Hand Gesture Click

This project implements a simple virtual mouse controlled by your hand using a webcam. The mouse cursor follows your index finger, and a left-click is performed by touching your index finger and thumb tips together.

## Features

- **Mouse movement** mapped to a comfortable control zone mid-frame.
- **Single left-click gesture**: Triggered by touching your index and thumb tips together.
- **Prevents accidental double-clicking**: Must separate fingers before another click.
- **Prevents PyAutoGUI fail-safe errors** by keeping mouse inside safe bounds.
- Easy to use, with real-time webcam feedback.

## Requirements

- Python 3.x
- Webcam
- Python libraries:
  - `opencv-python`
  - `mediapipe`
  - `pyautogui`

## Installation

Install dependencies using pip:

```bash
pip install opencv-python mediapipe pyautogui
```

## Usage

1. Run the script:

    ```bash
    python hand_mouse.py
    ```

2. Move your index finger inside the webcam’s center region to control mouse cursor movement across the whole screen.
3. Click by bringing your index finger tip and thumb tip together.
4. Separate your fingers before clicking again to avoid multiple clicks.
5. Press `q` in the window to quit.

## How It Works

- Uses MediaPipe to detect hand landmarks in webcam video.
- Maps the normalized index fingertip position within a defined control zone to screen coordinates.
- Detects click gesture based on the distance between index and thumb finger tips.
- Triggers mouse click using PyAutoGUI when click gesture is detected.
- Displays the webcam feed, hand landmarks, and click indications.

## Customization

- Adjust the control zone by changing `ZONE_TOP`, `ZONE_BOTTOM`, `ZONE_LEFT`, and `ZONE_RIGHT` inside the script to fine-tune sensitivity or range.
- Modify the click distance threshold (`TOUCH_THRESHOLD`) or click cooldown time (`CLICK_DELAY`) in the script to suit your hand and gesture style.

## Troubleshooting

- If cursor moves erratically, make sure your webcam has a clear view of your hand.
- Avoid extreme lighting for better hand landmark detection.
- If the script stops with a fail-safe error, ensure the mouse isn't moved to a screen corner; the script clamps cursor position to help prevent this.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 
