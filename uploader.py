import os
import winreg
import sys
import subprocess


def create_reg_key(program_path, menu_name, command):
    key_path = r"\*\shell"
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path, 0, winreg.KEY_WRITE)
    new_key_path = winreg.CreateKey(key, menu_name)
    winreg.CloseKey(new_key_path)
    command_key_path = winreg.CreateKey(key, menu_name + r"\command")
    winreg.SetValueEx(command_key_path, "", 0, winreg.REG_SZ, command)
    winreg.CloseKey(command_key_path)
    winreg.CloseKey(key)


def delete_reg_key(key_path):
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
    except Exception:
        pass


def add_context_menu_script(script_path):
    program_path = r"C:\Uploader\upload.exe"
    menu_name = "Upload file to fu.andcool.ru"
    command = f'"{program_path}""%1"'
    create_reg_key(program_path, menu_name, command)


def remove_context_menu_script():
    key_path = r"*\shell\Upload"
    delete_reg_key(key_path)


def install_library(*libraries):
    for library in libraries:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
            print(f"{library} package installed successfully.")
        except Exception as e:
            print(f"Error installing {library} package: {str(e)}")


def create_code_file(file_path, code_content):
    with open(file_path, "w") as file:
        file.write(code_content)
    print(f"Code file created at {file_path}")


uploader_code = """
import fileuploader
import asyncio
import sys
import pyperclip


async def upload_files(file_paths):
    for file_path in file_paths:
        try:
            with open(file_path, "rb") as file:
                response = await fileuploader.upload(file.read(), file.name)
                print(
                    f"File {file.name} uploaded successfully. URL: {response.file_url_full}"
                )
                pyperclip.copy(response.file_url_full)
        except Exception as e:
            print(f"Error uploading file {file_path}: {str(e)}", repr(e))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(upload_files(sys.argv[1:]))
    input("Press Enter to continue...")
"""


if __name__ == "__main__":
    install_library("fileuploader", "pyperclip", "pyinstaller", "elevate")

    from elevate import elevate

    elevate()

    upload_dir = "C:/Uploader"
    script_path = "/upload.py"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        print("Directory C:/Upload created.")
        create_code_file(upload_dir + script_path, uploader_code)
        os.system(
            f"pyinstaller --onefile --distpath {upload_dir} {upload_dir + script_path}"
        )
        os.remove(upload_dir + script_path)

    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "add":
            add_context_menu_script(upload_dir + script_path)
            print("Context menu script added successfully.")
        elif action == "remove":
            remove_context_menu_script()
            print("Context menu script removed successfully.")
        else:
            print("Invalid action. Please use 'add' or 'remove'.")
    else:
        add_context_menu_script(upload_dir + script_path)
        print("Context menu script added successfully.")
