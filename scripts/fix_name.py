content = open(r'C:\Users\Administrator\.openclaw\workspace\scripts\premarket_analysis.py', encoding='utf-8').read()
content = content.replace("'\u6e90\u6770\u80a1\u4efd'", "'\u82af\u539f\u80a1\u4efd'")
open(r'C:\Users\Administrator\.openclaw\workspace\scripts\premarket_analysis.py', 'w', encoding='utf-8').write(content)
print('done')
