import re

file_names = [
    "core/building.py",
    "core/callback.py",
    "core/decorators.py",
    "core/mixins.py",
    "core/state.py",
    "core/army.py",
    "core/game.py",
    "main.py",
]

with open("new.py", "w") as new_file:
    for file_name in file_names:
        with open(file_name, "r") as file:
            lines = file.readlines()
            filtered_lines = [
                line
                for line in lines
                if not (
                    re.match(r"logging.*\(\)", line)
                    or re.match(r"from\s\..*\simport\s*", line)
                )
            ]
            content = "".join(filtered_lines)
            new_file.write(content)
            new_file.write("\n\n")
