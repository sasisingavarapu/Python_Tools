
import sys
from PySide6 import QtWidgets
from shiboken6 import wrapInstance
from maya import OpenMayaUI as omui
import maya.cmds as cmds

# Import the correct UI module — match actual filename
from UI import ShotNote_ui as ui

  # Ensure this file is in the same folder or PYTHONPATH

# Global state
frame_notes: dict[int, str] = {}
_script_job_id: int | None = None
shotnotes_ui_instance: QtWidgets.QDialog | None = None


def get_maya_main_window() -> QtWidgets.QWidget:
    """Get Maya's main window as a Qt widget."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def update_hud():
    """Update the HUD with the current frame's note."""
    current_frame = int(cmds.currentTime(q=True))
    note = frame_notes.get(current_frame, "")
    if cmds.headsUpDisplay("frameNoteHUD", exists=True):
        cmds.headsUpDisplay("frameNoteHUD", edit=True, label=note)


def create_hud():
    """Create the custom heads-up display."""
    if cmds.headsUpDisplay("frameNoteHUD", exists=True):
        cmds.headsUpDisplay("frameNoteHUD", remove=True)
    cmds.headsUpDisplay(
        "frameNoteHUD",
        section=5,
        block=1,
        blockSize="medium",
        label="",
        labelFontSize="large",
        command=update_hud,
        event="timeChanged"
    )


def kill_script_job():
    """Kill any active scriptJob for HUD updates."""
    global _script_job_id
    if _script_job_id and cmds.scriptJob(exists=_script_job_id):
        cmds.scriptJob(kill=_script_job_id, force=True)
        _script_job_id = None


def store_script_job_id(job_id: int):
    """Store the scriptJob ID so it can be killed later."""
    global _script_job_id
    _script_job_id = job_id


def launch_shotnotes_ui():
    """Launch the ShotNotes UI window."""
    global shotnotes_ui_instance

    # Cleanup existing instance
    if shotnotes_ui_instance:
        try:
            shotnotes_ui_instance.close()
            shotnotes_ui_instance.deleteLater()
        except Exception:
            pass

    callbacks = {
        "create_hud": create_hud,
        "update_hud": update_hud,
        "kill_script_job": kill_script_job,
        "store_script_job_id": store_script_job_id,
    }

    shotnotes_ui_instance = ui.ShotNotesUI(frame_notes, callbacks, parent=get_maya_main_window())
    shotnotes_ui_instance.show()
