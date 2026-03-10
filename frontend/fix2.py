import re
content = open('app.py', encoding='utf-8').read()
old = 'os.unlink(tmp.name)'
new = 'try:\n        os.unlink(tmp.name)\n    except: pass'
content = content.replace(old, new)
open('app.py', 'w', encoding='utf-8').write(content)
print('done')
