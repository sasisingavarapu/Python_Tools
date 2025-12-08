import os
import json
import re
from PySide6 import QtWidgets
from maya import cmds


def parse_custom_notes(raw_text: str) -> dict[int, str]:
    """Parse notes in format: frame/total Some note text"""
    frame_notes_local = {}
    pattern = re.compile(r"(\d+)\s*/\s*\d+\s+(.*)")
    matches = pattern.findall(raw_text)

    for frame_str, note in matches:
        try:
            frame = int(frame_str)
            clean_note = note.strip(",. \n\t")
            if clean_note:
                frame_notes_local[frame] = clean_note
        except ValueError:
            continue

    return frame_notes_local


class ShotNotesUI(QtWidgets.QDialog):
    def __init__(self, frame_notes: dict[int, str], callbacks: dict[str, callable], parent=None):
        super().__init__(parent)
        self.setWindowTitle("ShotNotes HUD")
        self.setMinimumSize(480, 320)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.frame_notes = frame_notes
        self.callbacks = callbacks

        self.file_line = QtWidgets.QLineEdit()
        self.file_line.setPlaceholderText("Select .json or .txt note file")
        self.layout().addWidget(self.file_line)

        browse_btn = QtWidgets.QPushButton("Browse File")
        browse_btn.clicked.connect(self.browse_file)
        self.layout().addWidget(browse_btn)

        self.load_btn = QtWidgets.QPushButton("Start HUD")
        self.load_btn.clicked.connect(self.start_system)
        self.layout().addWidget(self.load_btn)

        self.jump_combo = QtWidgets.QComboBox()
        self.layout().addWidget(self.jump_combo)

        jump_btn = QtWidgets.QPushButton("Jump to Frame")
        jump_btn.clicked.connect(self.jump_to_frame)
        self.layout().addWidget(jump_btn)

    def browse_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Notes File", "", "JSON or Text Files (*.json *.txt)"
        )
        if not file_path:
            return

        self.file_line.setText(file_path)
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".json":
            self.load_notes_from_json(file_path)
        elif ext == ".txt":
            self.load_notes_from_custom_text(file_path)
        else:
            cmds.warning("Unsupported file type. Use .json or .txt")

    def load_notes_from_json(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.frame_notes.clear()
            self.frame_notes.update({int(k): str(v) for k, v in data.items() if str(k).isdigit()})
            if self.frame_notes:
                self.populate_combo()
                cmds.inViewMessage(amg="Loaded JSON notes.", pos="midCenter", fade=True)
            else:
                cmds.warning("No valid notes in JSON.")
        except Exception as e:
            cmds.warning(f"JSON load failed: {e}")

    def load_notes_from_custom_text(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            self.frame_notes.clear()
            self.frame_notes.update(parse_custom_notes(raw_text))
            if self.frame_notes:
                self.populate_combo()
                cmds.inViewMessage(amg="Loaded text notes.", pos="midCenter", fade=True)
            else:
                cmds.warning("No valid notes found in text file.")
        except Exception as e:
            cmds.warning(f"Text load failed: {e}")

    def populate_combo(self):
        self.jump_combo.clear()
        for frame in sorted(self.frame_notes.keys()):
            label = f"{frame}: {self.frame_notes[frame][:60]}"
            self.jump_combo.addItem(label)

    def start_system(self):
        if not self.frame_notes:
            cmds.warning("Load a notes file first.")
            return

        self.callbacks["create_hud"]()
        self.callbacks["kill_script_job"]()
        job_id = cmds.scriptJob(event=["timeChanged", self.callbacks["update_hud"]], protected=True)
        self.callbacks["store_script_job_id"](job_id)
        cmds.inViewMessage(amg="ShotNotes HUD started.", pos="midCenter", fade=True)

    def jump_to_frame(self):
        text = self.jump_combo.currentText()
        if text:
            try:
                frame = int(text.split(":")[0])
                cmds.currentTime(frame)
            except Exception:
                cmds.warning("Failed to jump to frame.")
