import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Hamster Desktop Pet - Windows
# Right-click the hamster for options. Drag with the left mouse button to move it.

BASE = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE, "assets")
POSE_COUNT = 12
TICK_MS = 180

class HamsterPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("햄찌")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#ff00ff")
        try:
            self.root.wm_attributes("-transparentcolor", "#ff00ff")
        except tk.TclError:
            pass

        self.images = []
        for i in range(POSE_COUNT):
            im = Image.open(os.path.join(ASSET_DIR, f"pose_{i:02d}.png")).convert("RGBA")
            self.images.append(ImageTk.PhotoImage(im))

        self.label = tk.Label(self.root, image=self.images[0], bg="#ff00ff", bd=0, highlightthickness=0)
        self.label.pack()
        self.root.geometry(f"120x120+220+180")

        self.x = 220
        self.y = 180
        self.dx = 2
        self.pose = 0
        self.mode = "wander"
        self.dragging = False
        self.drag_offset = (0, 0)
        self.frame = 0
        self.pause_until = 0

        for widget in (self.root, self.label):
            widget.bind("<ButtonPress-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.drag)
            widget.bind("<ButtonRelease-1>", self.stop_drag)
            widget.bind("<Double-Button-1>", self.toggle_wander)
            widget.bind("<Button-3>", self.popup)
            widget.bind("<Button-2>", self.popup)
            widget.bind("<Enter>", self.on_hover)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<Control-q>", lambda e: self.root.destroy())
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="🐹 잠깐 쉬기", command=self.rest)
        self.menu.add_command(label="✨ 돌아다니기", command=self.wander)
        self.menu.add_command(label="💤 잠자기", command=self.sleep)
        self.menu.add_separator()
        self.menu.add_command(label="종료", command=self.root.destroy)
        self.animate()

    def popup(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def start_drag(self, event):
        self.dragging = True
        self.drag_offset = (event.x_root - self.x, event.y_root - self.y)
        self.mode = "drag"
        self.set_pose(0)

    def drag(self, event):
        if self.dragging:
            self.x = event.x_root - self.drag_offset[0]
            self.y = event.y_root - self.drag_offset[1]
            self.root.geometry(f"+{self.x}+{self.y}")

    def stop_drag(self, event):
        self.dragging = False
        if self.mode == "drag":
            self.mode = "wander"

    def toggle_wander(self, event=None):
        if self.mode == "wander":
            self.rest()
        else:
            self.wander()

    def rest(self):
        self.mode = "rest"
        self.set_pose(5)

    def sleep(self):
        self.mode = "sleep"
        self.set_pose(5)

    def wander(self):
        self.mode = "wander"

    def on_hover(self, event):
        # Small reaction when the cursor approaches.
        if not self.dragging and self.mode == "wander" and random.random() < 0.45:
            self.set_pose(7)

    def set_pose(self, idx):
        self.pose = idx % POSE_COUNT
        self.label.configure(image=self.images[self.pose])

    def animate(self):
        if not self.dragging:
            if self.mode == "wander":
                self.frame += 1
                # Mostly walking, with occasional grooming / waving / resting poses.
                if self.frame % random.randint(16, 24) == 0:
                    self.set_pose(random.choice([3, 6, 7, 9, 11]))
                    self.pause_until = self.frame + random.randint(5, 12)
                elif self.frame < self.pause_until:
                    pass
                else:
                    self.set_pose(random.choice([0, 1, 2]))
                    sw = self.root.winfo_screenwidth()
                    sh = self.root.winfo_screenheight()
                    self.x += self.dx * random.choice([1, 1, 1, 2])
                    if self.x <= 0:
                        self.x = 0; self.dx = abs(self.dx)
                    elif self.x >= sw - 120:
                        self.x = sw - 120; self.dx = -abs(self.dx)
                    # Gentle bobbing movement
                    self.y = max(0, min(sh - 120, self.y + random.choice([-1, 0, 0, 1])))
                    self.root.geometry(f"+{self.x}+{self.y}")
            elif self.mode == "sleep":
                self.frame += 1
                if self.frame % 8 == 0:
                    self.set_pose(random.choice([5, 11]))
            elif self.mode == "rest":
                self.frame += 1
                if self.frame % 10 == 0:
                    self.set_pose(random.choice([3, 5, 6, 11]))
        self.root.after(TICK_MS, self.animate)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    HamsterPet().run()
