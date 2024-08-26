import re
import maya.cmds as cmds

asset_count = {}

def rename_asset(asset):
    global asset_count

    match = re.match(r'([^\d]+)(\d*)', asset)
    if match:
        asset_name = match.group(1)
        instance = match.group(2)

        if not instance:
            instance = '0'

        if asset_name not in asset_count:
            asset_count[asset_name] = 1

        new_major_version = asset_count[asset_name]
        asset_count[asset_name] += 1

        new_asset = "{}01x{:02d}".format(asset_name, new_major_version)
        return new_asset
    else:
        print("Invalid asset name: {}".format(asset))
        return None


def custom_rename_selected_assets():
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        print("No objects selected. Please select the objects you want to rename.")
        return

    # Get the user-provided prefix and suffix directly from the UI elements
    Prefix_input = cmds.textField("Rename_Tool_rowColumnLayout164_textField417", query=True, text=True)
    Suffix_input = cmds.textField("Rename_Tool_rowColumnLayout162_textField414", query=True, text=True)

    # Initialize a counter to append a numeric value after the suffix
    suffix_counter = 1

    for obj in selected_objects:
        try:
            # Construct the new name with the user-provided prefix, suffix, and numeric value
            new_name = "{}_{}{:02d}".format(Prefix_input, Suffix_input, suffix_counter)

            # Increment the counter for the next object
            suffix_counter += 1

            # Rename the object using the new name
            cmds.rename(obj, new_name)
        except RuntimeError as e:
            # Handle the read-only node error
            print(f"Error renaming {obj}: {str(e)}")

def change_version_selected_assets():
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        print("No objects selected. Please select the objects you want to change version.")
        return

    for obj in selected_objects:
        try:
            # Get the current name of the object
            current_name = cmds.ls(obj, long=True)[0]

            # Increment the version
            new_version = rename_asset(current_name)

            # Rename the object using the new versioned name
            cmds.rename(obj, new_version)
        except RuntimeError as e:
            # Handle the read-only node error
            print(f"Error changing version of {obj}: {str(e)}")

def create_window():
    if cmds.window("Rename Tool", exists=True):
        print("Window already exists.")
        return

    mywindow = cmds.window("Rename Tool")
    cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 100), (2, 250)])
    
    cmds.text(label='Prefix')
    Prefix_input = cmds.textField("Rename_Tool_rowColumnLayout164_textField417")
    cmds.text(label='Suffix')
    Suffix_input = cmds.textField("Rename_Tool_rowColumnLayout162_textField414")

    cmds.textField(Prefix_input, edit=True, enterCommand=('cmds.setFocus(\"' + Suffix_input + '\")'))
    cmds.textField(Suffix_input, edit=True, enterCommand=('custom_rename_selected_assets()'))

    cmds.button(label='Rename Selected', command=('custom_rename_selected_assets()'))
    cmds.button(label='Change Version', command=('change_version_selected_assets()'))

    cmds.text(label='')
    cmds.button(label='Close', command=('cmds.deleteUI(\"' + mywindow + '\", window=True)'))
    cmds.setParent('..')

    cmds.showWindow(mywindow)

create_window()
