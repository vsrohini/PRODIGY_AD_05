import tkinter as tk
import cv2
import webbrowser
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk

class QRCodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")

        # Initialize video capture (camera)
        self.video_source = 0  # Default webcam
        self.cap = cv2.VideoCapture(self.video_source)

        # Canvas to display the camera feed
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

        # Label to display QR code result
        self.result_label = tk.Label(self.root, text="Scanned Result: ", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.result_display = tk.Label(self.root, text="", font=("Arial", 12), fg="blue")
        self.result_display.pack(pady=10)

        # Start scanning the QR code
        self.update_frame()

    def update_frame(self):
        # Capture a frame from the webcam
        ret, frame = self.cap.read()

        if ret:
            # Decode any QR codes present in the frame
            decoded_qrs = decode(frame)

            # Process each detected QR code
            if decoded_qrs:
                for qr in decoded_qrs:
                    qr_data = qr.data.decode("utf-8")
                    self.result_display.config(text=qr_data)

                    # If the QR code contains a URL, open it in the browser
                    if qr_data.startswith("http"):
                        webbrowser.open(qr_data)
                    break  # Stop after detecting the first QR code in the frame

            # Convert the frame to RGB (for tkinter compatibility)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(img)

            # Update the canvas with the new frame
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk

        # Continue capturing frames
        self.root.after(10, self.update_frame)

    def on_close(self):
        # Release the video capture on app close
        self.cap.release()
        self.root.quit()

# Create the main window
root = tk.Tk()

# Create the QRCodeScannerApp
app = QRCodeScannerApp(root)

# Handle the window close event properly
root.protocol("WM_DELETE_WINDOW", app.on_close)

# Start the GUI event loop
root.mainloop()

