with open("script.js", "r") as f:
    code = f.read()

# Make sure API_URL dynamically reads current origin hostname
if 'const API_URL =' in code:
    lines = code.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith('const API_URL'):
            new_lines.append('const API_URL = window.location.origin + "/BitForge/api";')
        else:
            new_lines.append(line)
    code = "\n".join(new_lines)

with open("script.js", "w") as f:
    f.write(code)

print("script.js updated with dynamic host origin!")
