import os

file_path = "frontend/src/App.jsx"
if not os.path.exists(file_path):
    print("Error: App.jsx not found")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace typos
old_regex = 'const regex = /(\{\{[A-Za-z0-9_]+\}\}|\[[A-Za-55-9_]+\])/g;'
new_regex = 'const regex = /(\{\{[A-Za-z0-9_]+\}\}|\[[A-Za-z0-9_]+\])/g;'
content = content.replace(old_regex, new_regex)

old_curly = 'part.match(/^\{\{([A-Za-50-9_]+)\}\}$/)'
new_curly = 'part.match(/^\{\{([A-Za-z0-9_]+)\}\}$/)'
content = content.replace(old_curly, new_curly)

old_bracket = 'part.match(/^\[([A-Za-50-9_]+)\]$/)'
new_bracket = 'part.match(/^\[([A-Za-z0-9_]+)\]$/)'
content = content.replace(old_bracket, new_bracket)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("App.jsx regex typos fixed successfully!")
