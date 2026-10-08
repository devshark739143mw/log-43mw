"""
Log parsing helper: extracts timestamps from lines like '[YYYY-MM-DD HH:MM:SS] message'.
"""
import argparse, re, sys
from datetime import datetime

LOG_RE = re.compile(r'^\[(?P<ts>[^]]+)\]\s*(?P<msg>.*)$')

def parse_line(line):
    m = LOG_RE.match(line.rstrip())
    if not m:
        return None
    ts_str = m.group('ts')
    try:
        ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        ts = None
    return ts, m.group('msg')

def main():
    parser = argparse.ArgumentParser(description='Parse log file and display entries.')
    parser.add_argument('file', help='Path to log file')
    parser.add_argument('-d', '--datetime', action='store_true',
                        help='Show full datetime instead of default')
    args = parser.parse_args()
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f:
                res = parse_line(line)
                if res:
                    ts, msg = res
                    if ts:
                        out_ts = ts.strftime('%Y-%m-%d %H:%M:%S') if not args.datetime else ts.isoformat(sep=' ')
                    else:
                        out_ts = 'UNKNOWN'
                    print(f'{out_ts} - {msg}')
                else:
                    print(f'UNPARSED: {line.rstrip()}')
    except FileNotFoundError:
        sys.exit(f'File not found: {args.file}')

if __name__ == '__main__':
    main()