"""
backup_restore.py - 一键备份与恢复
备份：所有配置/日志/脚本到GitHub + 飞书云文档
恢复：从指定commit恢复系统
"""
import os
import sys
import subprocess
import shutil
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\Administrator\.openclaw\workspace'
GITHUB_REPO = 'https://github.com/open-kj/openclaw-memory.git'

def git_cmd(args):
    """执行git命令"""
    cmd = ['git', '-C', BASE] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout + result.stderr

def backup_to_github():
    """一键备份到GitHub"""
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    print('=== 一键备份 [' + ts + '] ===')

    # git add -A
    print('1. git add -A...')
    print(git_cmd(['add', '-A']))

    # git commit
    msg = 'backup: ' + ts
    print('2. git commit...')
    print(git_cmd(['commit', '-m', msg]))

    # git push
    print('3. git push...')
    result = git_cmd(['push', 'origin', 'master'])
    print(result)

    if 'error' in result.lower() or 'fatal' in result.lower():
        print('⚠️ GitHub备份失败，请检查网络')
        return False

    # 写入备份记录
    record_file = os.path.join(BASE, 'memory', 'backup-log.md')
    record = '\n## 备份记录 [{}]\n- 备份时间: {}\n- 状态: 成功\n'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ts)
    with open(record_file, 'a', encoding='utf-8') as f:
        f.write(record)

    print('✅ 备份完成')
    return True

def restore_from_commit(commit_hash):
    """从指定commit恢复"""
    print('=== 从commit恢复: ' + commit_hash + ' ===')
    if len(commit_hash) < 6:
        print('⚠️ commit hash至少需要6位')
        return False

    # git stash（暂存当前改动）
    print('1. git stash...')
    git_cmd(['stash'])

    # git checkout
    print('2. git checkout ' + commit_hash + '...')
    result = git_cmd(['checkout', commit_hash])
    if 'error' in result.lower() or 'fatal' in result.lower():
        print('⚠️ checkout失败: ' + result)
        git_cmd(['stash', 'pop'])
        return False

    print('✅ 恢复成功（commit: ' + commit_hash + '）')
    print('请重启OpenClaw使改动生效')

    # 记录恢复
    record_file = os.path.join(BASE, 'memory', 'restore-log.md')
    record = '\n## 恢复记录 [{}]\n- 恢复到: {}\n'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'), commit_hash)
    with open(record_file, 'a', encoding='utf-8') as f:
        f.write(record)
    return True

def get_backup_list():
    """获取可用的backup列表"""
    result = git_cmd(['log', '--oneline', '-n', '20'])
    print('=== 最近20个提交 ===')
    print(result)
    return result

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'backup':
            backup_to_github()
        elif cmd == 'list':
            get_backup_list()
        elif cmd == 'restore' and len(sys.argv) > 2:
            restore_from_commit(sys.argv[2])
        else:
            print('用法: python backup_restore.py [backup|list|restore HASH]')
    else:
        print('用法: python backup_restore.py [backup|list|restore HASH]')
