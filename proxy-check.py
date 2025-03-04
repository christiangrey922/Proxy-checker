import requests
import json
from datetime import datetime
from colorama import Fore, Back, Style, init

# Khởi tạo colorama
init(autoreset=True)

CoderMarkPrinted = False

def CoderMark(CoderMarkPrinted):
    if not CoderMarkPrinted:
        print(f"""
@Christian-Grey-922""")
        CoderMarkPrinted = True

def check_proxy(proxy_line):
    try:
        parts = proxy_line.split('://')
        if len(parts) != 2:
            raise Exception('Invalid proxy format')
        
        protocol, rest = parts
        
        proxies = {
            'http': f'{protocol}://{rest}',
            'https': f'{protocol}://{rest}'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
        
        response = requests.get('https://ipinfo.io/json', proxies=proxies, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            'proxy': proxy_line,
            'success': True,
            'ip': data['ip'],
            'country': data['country'],
            'region': data['region'],
            'city': data['city']
        }
    except Exception as error:
        return {
            'proxy': proxy_line,
            'success': False,
            'error': str(error)
        }

def check_proxy_list():
    try:
        with open('proxy.txt', 'r') as file:
            proxy_list = [line.strip() for line in file if line.strip()]
        
        print(f"Loading {len(proxy_list)} proxies...\n")
        
        results = []
        for proxy in proxy_list:
            result = check_proxy(proxy)
            
            if result['success']:
                # Proxy tốt: màu xanh nước biển
                print(f"{Fore.BLUE}{proxy}{Style.RESET_ALL} -> IP: {Fore.GREEN}{result['ip']}{Style.RESET_ALL} ({result['country']})")
            else:
                # Proxy lỗi: màu đỏ
                print(f"{Fore.RED}{proxy}{Style.RESET_ALL} -> Error: {Fore.LIGHTRED_EX}{result['error']}{Style.RESET_ALL}")
            
            results.append(result)
        
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        output_file = f"proxy_check_results_{timestamp}.json"
        
        with open(output_file, 'w') as file:
            json.dump(results, file, indent=4)
        print(f"\nResults saved to {output_file}\n")
        
        working = sum(1 for r in results if r['success'])
        print("\nSummary:")
        print(f"Total proxies: {len(results)}")
        print(f"Working: {working}")
        print(f"Failed: {len(results) - working}")
        
    except Exception as error:
        print(f'{Fore.RED}Error reading proxy file: {error}{Style.RESET_ALL}\n')

# Run the checker
CoderMark(CoderMarkPrinted)
check_proxy_list()
