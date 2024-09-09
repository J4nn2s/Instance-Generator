import os
import glob

def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for _ in file)

def count_lines_in_directory(directory, file_extension="*.py"):
    total_lines = 0
    for file_path in glob.glob(os.path.join(directory, '**', file_extension), recursive=True):
        total_lines += count_lines_in_file(file_path)
    return total_lines

def count_lines_in_project(project_directory):
    total_lines = 0
    subdirectories = ['main', 'lib', 'gui']
    for subdirectory in subdirectories:
        dir_path = os.path.join(project_directory, subdirectory)
        if os.path.exists(dir_path):
            lines = count_lines_in_directory(dir_path)
            print(f"Zeilen im Verzeichnis '{subdirectory}': {lines}")
            total_lines += lines
        else:
            print(f"Verzeichnis '{subdirectory}' existiert nicht.")
    return total_lines

if __name__ == "__main__":
    project_directory = os.path.dirname(os.path.abspath(__file__))
    total_lines_of_code = count_lines_in_project(project_directory)
    print(f"Die Gesamtanzahl der Codezeilen im Projekt beträgt: {total_lines_of_code}")