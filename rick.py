import os
import random
import string
import shutil
import colorama
from colorama import Fore, Back, Style

colorama.init()

class DiskCleaner:
    def __init__(self):
        self.disks = self.get_all_disks()

    def get_all_disks(self):
        disks = []
        if os.name == 'nt':
            import win32api # type: ignore
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            for drive in drives:
                if os.path.exists(drive):
                    disks.append(drive)
        else:
            with os.popen('lsblk -o NAME,MOUNTPOINT') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 2 and parts[1] != '/':
                        disks.append(parts[0])
        return disks

    def display_disks(self):
        print(Fore.CYAN + "Mövcud Disklər:")
        for idx, disk in enumerate(self.disks):
            print(f"{Fore.GREEN}{idx + 1}. {disk}{Style.RESET_ALL}")

    def get_free_space(self, disk_path):
        total, used, free = shutil.disk_usage(disk_path)
        return free

    def generate_random_data(self, size):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

    def write_random_data(self, disk_path, block_size=1024 * 1024):
        free_space = self.get_free_space(disk_path)
        print(f"{Fore.YELLOW}{disk_path} üzərindəki boş sahə: {free_space} bytes{Style.RESET_ALL}")
        
        num_blocks = free_space // block_size
        print(f"{Fore.YELLOW}{num_blocks} ədəd data bloku yazılacaq.{Style.RESET_ALL}")
        
        with open(disk_path + 'tempfile', 'wb') as f:
            for _ in range(num_blocks):
                random_data = self.generate_random_data(block_size)
                f.write(random_data.encode('utf-8'))
                f.flush()  # Veriyi diske yaz
        print(Fore.CYAN + "data diske yazıldı. İndi silinir..." + Style.RESET_ALL)

        # Şimdi yazılan dosyayı sil
        os.remove(disk_path + 'tempfile')
        print(Fore.RED + "Bütün silinmiş data yox edildi!" + Style.RESET_ALL)

    def show_warning(self):
        print(Fore.RED + "\nDiqqət! Bu proses diskinizdəki əvvəl silinmiş olan şeyləri qalıcı olaraq yox edəcəkdir." +
              "\nProses uzun çəkə bilər. xahiş edirik program çalışarkən cihazı söndürməyin!" + 
              "\nHərhansı bir kəsintidə dikiniz qalıcı zərər görə bilər." + Style.RESET_ALL)
        print(Fore.YELLOW + "Devam etmək üçün 'razıyam', dayandırmaq üçün 'ləğv et' yazın:" + Style.RESET_ALL)

if __name__ == "__main__":
    cleaner = DiskCleaner()
    
    cleaner.display_disks()
    
    disk_choice = int(input("Diski seçin (sıra nömrəsi): ")) - 1
    
    if 0 <= disk_choice < len(cleaner.disks):
        cleaner.show_warning()
        user_input = input().strip().lower()
        
        if user_input == 'razıyam':
            disk_path = cleaner.disks[disk_choice]
            cleaner.write_random_data(disk_path)
        else:
            print(Fore.RED + "Proses ləğv edildi" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Keçərsiz seçim!" + Style.RESET_ALL)
