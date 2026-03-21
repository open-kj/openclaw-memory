"""
exception_handler.py v2.0 - 全局异常装饰器 + 熔断逻辑
同一模块1小时内报错≥3次触发熔断，暂停10分钟
"""
import functools
import time
import os
from datetime import datetime
from config.settings import CIRCUIT_BREAKER_ERRORS, CIRCUIT_BREAKER_WINDOW

LOG_FILE = r'C:\Users\Administrator\.openclaw\workspace\logs\exception.log'
BREAKER_FILE = r'C:\Users\Administrator\.openclaw\workspace\logs\circuit_breaker.log'

# 熔断状态
_circuit_breaker = {}  # module_name -> [(timestamp, error_msg), ...]

def is_breaker_open(module_name):
    """检查熔断是否开启"""
    if module_name not in _circuit_breaker:
        return False
    now = time.time()
    # 清理超过1小时的记录
    _circuit_breaker[module_name] = [
        (ts, msg) for ts, msg in _circuit_breaker[module_name]
        if now - ts < CIRCUIT_BREAKER_WINDOW
    ]
    if len(_circuit_breaker[module_name]) >= CIRCUIT_BREAKER_ERRORS:
        return True
    return False

def trip_breaker(module_name, error_msg):
    """触发熔断"""
    now = time.time()
    if module_name not in _circuit_breaker:
        _circuit_breaker[module_name] = []
    _circuit_breaker[module_name].append((now, error_msg))
    msg = '[{}] CIRCUIT_BREAKER_TRIP: {} (errors={})'.format(
        datetime.now().strftime('%H:%M:%S'), module_name, CIRCUIT_BREAKER_ERRORS)
    print(msg)
    log_error(msg)
    try:
        with open(BREAKER_FILE, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except:
        pass
    return True

def check_and_trip(module_name, error_msg):
    """检查并触发熔断"""
    if is_breaker_open(module_name):
        return True
    if module_name not in _circuit_breaker:
        _circuit_breaker[module_name] = []
    _circuit_breaker[module_name].append((time.time(), error_msg))
    if len(_circuit_breaker[module_name]) >= CIRCUIT_BREAKER_ERRORS:
        trip_breaker(module_name, error_msg)
    return False

def exception_handler(func=None, *, silent=False, module_name=None):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            mod = module_name or fn.__module__
            # 熔断检查
            if is_breaker_open(mod):
                return {'error': 'CIRCUIT_BREAKER_OPEN', 'module': mod}
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                now = time.time()
                err_str = str(e)
                # 记录并检查熔断
                breaker_will_trip = check_and_trip(mod, err_str)
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                msg = '[{}] {}.{}: {}'.format(ts, mod, fn.__name__, err_str)
                log_error(msg)
                if breaker_will_trip:
                    breaker_msg = '[{}] 熔断触发: {} 已暂停运行'.format(
                        datetime.now().strftime('%H:%M:%S'), mod)
                    print(breaker_msg)
                    log_error(breaker_msg)
                if not silent:
                    print('[ERROR] ' + msg[:100])
                return {'error': err_str, 'module': mod}
        return wrapper
    if func is not None:
        return decorator(func)
    return decorator

def log_error(msg):
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except:
        pass

def get_breaker_status():
    """获取熔断状态"""
    now = time.time()
    status = {}
    for mod, entries in _circuit_breaker.items():
        active = [(ts, msg) for ts, msg in entries if now - ts < CIRCUIT_BREAKER_WINDOW]
        if active:
            status[mod] = {'count': len(active), 'open': len(active) >= CIRCUIT_BREAKER_ERRORS}
    return status

def reset_breaker(module_name=None):
    """重置熔断"""
    if module_name:
        _circuit_breaker.pop(module_name, None)
    else:
        _circuit_breaker.clear()
    print('[OK] 熔断已重置')

if __name__ == '__main__':
    print('=== 熔断状态 ===')
    print(get_breaker_status())
    print()
    # 测试
    @exception_handler(module_name='test_module')
    def failing_func():
        raise ValueError('test error')
    for i in range(4):
        r = failing_func()
        print('Call {}: {}'.format(i+1, r.get('error') if isinstance(r, dict) else r))
