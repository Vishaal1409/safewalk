import re
content = open('app.py', encoding='utf-8').read()
new_map = '    import tempfile, os\n    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=\".html\")\n    m.save(tmp.name)\n    with open(tmp.name, \"r\", encoding=\"utf-8\") as f:\n        html_content = f.read()\n    os.unlink(tmp.name)\n    st.components.v1.html(html_content, height=500, scrolling=False)'
content = re.sub(r'    try:\s+map_data = st_folium.*?scrolling=False\)', new_map, content, flags=re.DOTALL)
open('app.py', 'w', encoding='utf-8').write(content)
print('done')
