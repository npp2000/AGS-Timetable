import os
import re
 
# Folder path and search/replace strings
folder_path = "C:\\Github\\AGS-Timetable"  # change to your folder
old_text = "ICT  A Teacher"                  # text to find
new_text = "Emmanuel Akrofi"               # text to replace with

# Walk through the folder (can be recursive)
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".html"):  # filter by extension
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                new_content = re.sub(old_text, new_text, content)  # regex replace
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path}")
            except Exception as e:
                print(f"Error updating {file_path}: {e}")
