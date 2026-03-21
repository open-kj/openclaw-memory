"""
exception_handler.py - 全局异常装饰器
为所有核心函数自动添加 @exception_handler 装饰器
"""
import functools
import sys
import traceback
from datetime import datetime

LOG_FILE = r'C:\Users\Administrator\.openclaw\workspace\logs\exception.log'

def exception_handler(func=None, *, silent=False):
    """
    异常处理装饰器
    用法: @exception_handler() 或 @exception_handler(silent=True)
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                error_msg = f'[{ts}] {fn.__name__}: {str(e)}'
                log_error(error_msg)
                if not silent:
                    print(f'[ERROR] {error_msg}')
                return {'error': str(e), 'function': fn.__name__}
        return wrapper

    if func is not None:
        return decorator(func)
    return decorator

def log_error(msg):
    """写入异常日志"""
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except:
        pass

def log_info(msg):
    """写入信息日志"""
    try:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f'[{ts}] INFO: {msg}\n')
    except:
        pass

# 示例：如何使用装饰器
if __name__ == '__main__':
    @exception_handler
    def test_function():
        print('正常执行')
        return 'success'

    @exception_handler
    def test_error():
        raise ValueError('测试异常')

    r1 = test_function()
    print(f'Result: {r1}')
    r2 = test_error()
    print(f'Error result: {r2}')
