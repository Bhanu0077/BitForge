with open("html/transactions.html", "r") as f:
    html = f.read()

# Replace type="email" with type="text" and change labels to Username
html = html.replace('type="email"', 'type="text"')
html = html.replace('Receiver Account Email', 'Receiver Username')
html = html.replace('placeholder="Select a contact above or type email..."', 'placeholder="Select a contact above or type username..."')
html = html.replace('Scanned Target Email', 'Scanned Target Username')
html = html.replace('Scanned recipient email appear here...', 'Scanned recipient username appears here...')

with open("html/transactions.html", "w") as f:
    f.write(html)

print("html/transactions.html updated to type='text' for usernames!")
