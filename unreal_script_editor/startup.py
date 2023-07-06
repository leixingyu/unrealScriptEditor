import os
import sys

import unreal


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
UPPER_PATH = os.path.join(MODULE_PATH, '..')

sys.path.append(UPPER_PATH)


def create_script_editor_button():
    """
    Start up script to add script editor button to tool bar
    """

    section_name = 'Plugins'
    se_command = (
        'from unrealScriptEditor import main;'
        'global editor;'
        'editor = main.show()'
    )

    menus = unreal.ToolMenus.get()
    level_menu_bar = menus.find_menu('LevelEditor.LevelEditorToolBar.PlayToolBar')
    level_menu_bar.add_section(section_name=section_name, label=section_name)

    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label('Script Editor')
    entry.set_tool_tip('Unreal Python Script Editor')
    entry.set_icon('EditorStyle', 'DebugConsole.Icon')
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),
        string=se_command
    )
    level_menu_bar.add_menu_entry(section_name, entry)
    menus.refresh_all_widgets()


if __name__ == "__main__":
    create_script_editor_button()
