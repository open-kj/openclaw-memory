import os
path = os.path.join(r'C:\Users\Administrator\.openclaw\workspace', 'utils', 'daily_logger.py')
content = open(path, encoding='utf-8').read()
content = content.replace('sys.path_insert = sys.path.insert', 'sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))')
open(path, 'w', encoding='utf-8').write(content)
print('fixed')
