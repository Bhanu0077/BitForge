with open('/home/bhanu/apache-tomcat-11.0.27/conf/context.xml', 'r') as f:
    content = f.read()

if 'allowLinking' not in content:
    content = content.replace('<Context>', '<Context allowLinking="true">')
    with open('/home/bhanu/apache-tomcat-11.0.27/conf/context.xml', 'w') as f:
        f.write(content)
    print("Updated conf/context.xml with allowLinking='true'")
else:
    print("allowLinking is already configured.")
