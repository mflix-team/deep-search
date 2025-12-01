import os
import json
import sys
import argparse
import logging
from pathlib import Path
from tqdm import tqdm
from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=True)

# 配置日志
logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """配置日志系统"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def count_items(path):
    """预先计算目录中的项目总数，用于进度条"""
    total = 0
    try:
        for root, dirs, files in os.walk(path):
            total += len(files) + len(dirs)
    except Exception as e:
        logger.error(f"计算项目总数时出错: {e}")
    return total


def scan_directory(path, pbar=None):
    """
    递归扫描目录，返回所有文件和文件夹的结构
    """
    result = {
        'name': os.path.basename(path) or path,
        'path': str(path),
        'type': 'directory' if os.path.isdir(path) else 'file'
    }
    
    if pbar:
        pbar.update(1)
    
    if os.path.isdir(path):
        result['children'] = []
        try:
            entries = sorted(os.listdir(path))
            logger.debug(f"扫描目录: {path} (包含 {len(entries)} 个项目)")
            
            for entry in entries:
                # 跳过隐藏文件（可选）
                # if entry.startswith('.'):
                #     continue
                    
                full_path = os.path.join(path, entry)
                try:
                    result['children'].append(scan_directory(full_path, pbar))
                except Exception as e:
                    logger.error(f"扫描 {full_path} 时出错: {e}")
                    result['children'].append({
                        'name': entry,
                        'path': full_path,
                        'error': str(e)
                    })
        except PermissionError as e:
            result['error'] = 'Permission denied'
            logger.warning(f"权限被拒绝: {path}")
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"扫描目录 {path} 时出错: {e}")
    else:
        # 如果是文件，添加文件大小信息
        try:
            result['size'] = os.path.getsize(path)
            logger.debug(f"处理文件: {path} ({result['size']} bytes)")
        except OSError as e:
            result['error'] = 'Cannot get file size'
            logger.warning(f"无法获取文件大小: {path} - {e}")
    
    return result


def scan_directory_flat(path, show_progress=True):
    """
    递归扫描目录，返回所有文件的平面列表
    """
    files = []
    errors = []
    
    try:
        # 预计算总数用于进度条
        if show_progress:
            logger.info("正在计算文件总数...")
            total_files = sum([len(filenames) for _, _, filenames in os.walk(path)])
            pbar = tqdm(total=total_files, desc="扫描文件", unit="个文件", 
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
        else:
            pbar = None
        
        for root, dirs, filenames in os.walk(path):
            # 排除隐藏文件夹（可选）
            # dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            logger.debug(f"进入目录: {root} (包含 {len(filenames)} 个文件)")
            
            for filename in filenames:
                try:
                    full_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(full_path, path)
                    file_size = os.path.getsize(full_path) if os.path.exists(full_path) else 0
                    
                    files.append({
                        'name': filename,
                        'path': full_path,
                        'relative_path': relative_path,
                        'size': file_size
                    })
                    
                    if pbar:
                        pbar.update(1)
                        pbar.set_postfix_str(f"当前: {filename[:30]}...")
                    
                    logger.debug(f"已添加: {relative_path} ({file_size} bytes)")
                    
                except Exception as e:
                    error_msg = f"处理文件 {filename} 时出错: {e}"
                    errors.append(error_msg)
                    logger.error(error_msg)
        
        if pbar:
            pbar.close()
            
    except Exception as e:
        logger.error(f"扫描目录时出错: {e}")
        errors.append(f"扫描目录时出错: {e}")
    
    if errors:
        logger.warning(f"扫描过程中遇到 {len(errors)} 个错误")
    
    return files


if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description='递归扫描目录并生成JSON格式的文件路径信息',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python app.py                          # 扫描当前目录
  python app.py /path/to/directory       # 扫描指定目录
  python app.py ~/Documents              # 扫描用户文档目录
  python app.py . --output myfiles.json  # 自定义输出文件名
        '''
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default=os.getcwd(),
        help='要扫描的目录路径（默认为当前目录）'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='file',
        help='输出文件名前缀（默认为 "file"，生成 file_tree.json 和 file_list.json）'
    )
    
    parser.add_argument(
        '--tree-only',
        action='store_true',
        help='只生成树状结构'
    )
    
    parser.add_argument(
        '--list-only',
        action='store_true',
        help='只生成平面列表'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细日志信息'
    )
    
    parser.add_argument(
        '--no-progress',
        action='store_true',
        help='不显示进度条'
    )
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.verbose)
    
    # 设置日志
    setup_logging(args.verbose)
    
    # 处理路径
    scan_path = os.path.abspath(os.path.expanduser(args.path))
    
    # 验证路径是否存在
    if not os.path.exists(scan_path):
        print(f"{Fore.RED}✗ 错误: 路径不存在: {scan_path}{Style.RESET_ALL}")
        sys.exit(1)
    
    if not os.path.isdir(scan_path):
        print(f"{Fore.RED}✗ 错误: 不是有效的目录: {scan_path}{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ 正在扫描目录: {Fore.YELLOW}{scan_path}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
    
    logger.info(f"开始扫描目录: {scan_path}")
    
    # 方式1: 树状结构
    if not args.list_only:
        print(f"{Fore.MAGENTA}{'=' * 60}")
        print(f"📊 方式1: 树状结构")
        print(f"{'=' * 60}{Style.RESET_ALL}")
        
        logger.info("开始生成树状结构...")
        
        # 计算总数用于进度条
        if not args.no_progress:
            total_items = count_items(scan_path)
            pbar = tqdm(total=total_items, desc="构建树结构", unit="项", 
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
        else:
            pbar = None
        
        tree_structure = scan_directory(scan_path, pbar)
        
        if pbar:
            pbar.close()
        
        tree_json = json.dumps(tree_structure, indent=2, ensure_ascii=False)
        
        if args.verbose:
            print(tree_json)
        
        # 保存树状结构到文件
        tree_filename = f'{args.output}_tree.json'
        with open(tree_filename, 'w', encoding='utf-8') as f:
            f.write(tree_json)
        
        file_size = os.path.getsize(tree_filename)
        print(f"{Fore.GREEN}✓ 树状结构已保存到: {Fore.YELLOW}{tree_filename}{Style.RESET_ALL} ({file_size:,} bytes)")
        logger.info(f"树状结构已保存: {tree_filename} ({file_size} bytes)")
    
    # 方式2: 平面列表
    if not args.tree_only:
        print(f"\n{Fore.MAGENTA}{'=' * 60}")
        print(f"📋 方式2: 文件平面列表")
        print(f"{'=' * 60}{Style.RESET_ALL}")
        
        logger.info("开始生成平面列表...")
        
        flat_list = scan_directory_flat(scan_path, show_progress=not args.no_progress)
        flat_json = json.dumps(flat_list, indent=2, ensure_ascii=False)
        
        if args.verbose:
            print(flat_json)
        
        # 保存平面列表到文件
        list_filename = f'{args.output}_list.json'
        with open(list_filename, 'w', encoding='utf-8') as f:
            f.write(flat_json)
        
        file_size = os.path.getsize(list_filename)
        print(f"{Fore.GREEN}✓ 文件列表已保存到: {Fore.YELLOW}{list_filename}{Style.RESET_ALL} ({file_size:,} bytes)")
        logger.info(f"文件列表已保存: {list_filename} ({file_size} bytes)")
        
        # 统计信息
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"📈 统计信息")
        print(f"{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}总文件数:{Style.RESET_ALL} {Fore.YELLOW}{len(flat_list):,}{Style.RESET_ALL}")
        
        total_size = sum(f['size'] for f in flat_list)
        print(f"{Fore.CYAN}总大小:{Style.RESET_ALL} {Fore.YELLOW}{total_size:,}{Style.RESET_ALL} bytes "
              f"({Fore.YELLOW}{total_size / 1024 / 1024:.2f}{Style.RESET_ALL} MB)")
        
        # 文件类型统计
        extensions = {}
        for f in flat_list:
            ext = os.path.splitext(f['name'])[1] or '(无扩展名)'
            extensions[ext] = extensions.get(ext, 0) + 1
        
        print(f"\n{Fore.CYAN}文件类型分布 (前10种):{Style.RESET_ALL}")
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {Fore.YELLOW}{ext:20s}{Style.RESET_ALL}: {count:,} 个")
        
        logger.info(f"扫描完成: {len(flat_list)} 个文件, 总大小 {total_size} bytes")
    
    print(f"\n{Fore.GREEN}{'=' * 60}")
    print(f"✓ 扫描完成!")
    print(f"{'=' * 60}{Style.RESET_ALL}")
    logger.info("所有操作已完成")

