import ast
import pkgutil
import subprocess

def get_imported_modules(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    imported_modules = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module
            if node.names:
                for alias in node.names:
                    imported_modules.add(f"{module_name}.{alias.name}")
            else:
                imported_modules.add(module_name)

    return sorted(imported_modules)

def get_installed_versions():
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
    return [line.strip() for line in result.stdout.split('\n')]

# Example usage
file_path = "Newton_AI.py"  # Replace with the path to your Python script

script_modules = get_imported_modules(file_path)
installed_versions = get_installed_versions()

print("Modules used in the script with versions:")
for module in script_modules:
    for line in installed_versions:
        if line.startswith(module + "=="):
            print(line)
            break
    else:
        print(f"{module} (version not found)")
