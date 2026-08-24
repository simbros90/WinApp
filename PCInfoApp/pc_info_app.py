#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PC Information Desktop Application for Windows
Displays all PC characteristics in a single window.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import platform
import socket
import psutil
import cpuinfo
from datetime import datetime


class PCInfoApp:
    """Main application class for displaying PC information."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Информация о системе ПК")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set icon (optional, will use default if not found)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text="Характеристики компьютера", 
            font=('Segoe UI', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.system_tab = ttk.Frame(self.notebook, padding="10")
        self.cpu_tab = ttk.Frame(self.notebook, padding="10")
        self.memory_tab = ttk.Frame(self.notebook, padding="10")
        self.disk_tab = ttk.Frame(self.notebook, padding="10")
        self.network_tab = ttk.Frame(self.notebook, padding="10")
        self.gpu_tab = ttk.Frame(self.notebook, padding="10")
        
        # Add tabs to notebook
        self.notebook.add(self.system_tab, text="Система")
        self.notebook.add(self.cpu_tab, text="Процессор")
        self.notebook.add(self.memory_tab, text="Оперативная память")
        self.notebook.add(self.disk_tab, text="Диски")
        self.notebook.add(self.network_tab, text="Сеть")
        self.notebook.add(self.gpu_tab, text="Видеокарта")
        
        # Configure tab grids
        for tab in [self.system_tab, self.cpu_tab, self.memory_tab, 
                    self.disk_tab, self.network_tab, self.gpu_tab]:
            tab.columnconfigure(0, weight=1)
            tab.columnconfigure(1, weight=2)
            tab.rowconfigure(0, weight=1)
        
        # Populate all tabs
        self.populate_system_tab()
        self.populate_cpu_tab()
        self.populate_memory_tab()
        self.populate_disk_tab()
        self.populate_network_tab()
        self.populate_gpu_tab()
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(10, 0), sticky=tk.E)
        
        # Refresh button
        refresh_btn = ttk.Button(
            button_frame, 
            text="Обновить", 
            command=self.refresh_all
        )
        refresh_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Copy button
        copy_btn = ttk.Button(
            button_frame, 
            text="Копировать всё", 
            command=self.copy_all_info
        )
        copy_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Exit button
        exit_btn = ttk.Button(
            button_frame, 
            text="Выход", 
            command=root.quit
        )
        exit_btn.grid(row=0, column=2)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(f"Загружено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.grid(row=3, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
    
    def get_system_info(self):
        """Collect system information."""
        info = {}
        
        # OS Information
        info['ОС'] = f"{platform.system()} {platform.release()} ({platform.version()})"
        info['Архитектура'] = platform.machine()
        info['Имя компьютера'] = socket.gethostname()
        info['Процессор (логический)'] = platform.processor()
        
        # Boot time
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        info['Время загрузки'] = boot_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Uptime
        uptime = datetime.now() - boot_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        info['Время работы'] = f"{days} дн., {hours} ч., {minutes} мин."
        
        return info
    
    def get_cpu_info(self):
        """Collect CPU information."""
        info = {}
        
        # Get detailed CPU info
        try:
            cpu_info_data = cpuinfo.get_cpu_info()
            info['Модель'] = cpu_info_data.get('brand_raw', 'N/A')
            info['Архитектура'] = cpu_info_data.get('arch_string_raw', 'N/A')
            info['Битность'] = f"{cpu_info_data.get('bits', 'N/A')} бит"
            info['Частота (макс.)'] = f"{cpu_info_data.get('hz_advertised_friendly', 'N/A')}"
            info['Ядра (физические)'] = str(psutil.cpu_count(logical=False))
            info['Ядра (логические)'] = str(psutil.cpu_count(logical=True))
        except:
            info['Модель'] = platform.processor()
            info['Ядра (логические)'] = str(psutil.cpu_count(logical=True))
        
        # Current CPU usage
        info['Загрузка CPU (текущая)'] = f"{psutil.cpu_percent(interval=0.5)}%"
        
        # Per-core usage
        per_core = psutil.cpu_percent(interval=0.5, percpu=True)
        info['Загрузка по ядрам'] = ', '.join([f"{p}%" for p in per_core[:8]])
        if len(per_core) > 8:
            info['Загрузка по ядрам'] += '...'
        
        return info
    
    def get_memory_info(self):
        """Collect memory information."""
        info = {}
        
        mem = psutil.virtual_memory()
        info['Всего'] = f"{mem.total / (1024**3):.2f} ГБ"
        info['Доступно'] = f"{mem.available / (1024**3):.2f} ГБ"
        info['Используется'] = f"{mem.used / (1024**3):.2f} ГБ"
        info['Процент использования'] = f"{mem.percent}%"
        
        # Swap memory
        swap = psutil.swap_memory()
        info['Swap (всего)'] = f"{swap.total / (1024**3):.2f} ГБ"
        info['Swap (используется)'] = f"{swap.used / (1024**3):.2f} ГБ"
        info['Swap (% использования)'] = f"{swap.percent}%"
        
        return info
    
    def get_disk_info(self):
        """Collect disk information."""
        info = {}
        
        partitions = psutil.disk_partitions()
        disk_usage_list = []
        
        for i, partition in enumerate(partitions[:10]):  # Limit to 10 partitions
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info = (
                    f"{partition.device}: {usage.total / (1024**3):.1f} ГБ "
                    f"(свободно: {usage.free / (1024**3):.1f} ГБ, "
                    f"{usage.percent}% заполнено)"
                )
                disk_usage_list.append(disk_info)
            except PermissionError:
                disk_usage_list.append(f"{partition.device}: Нет доступа")
        
        info['Разделы дисков'] = '\n'.join(disk_usage_list) if disk_usage_list else 'Нет данных'
        
        # Disk I/O counters
        try:
            io_counters = psutil.disk_io_counters()
            if io_counters:
                info['Чтение с диска'] = f"{io_counters.read_bytes / (1024**2):.2f} МБ"
                info['Запись на диск'] = f"{io_counters.write_bytes / (1024**2):.2f} МБ"
        except:
            pass
        
        return info
    
    def get_network_info(self):
        """Collect network information."""
        info = {}
        
        # Network interfaces
        net_if_addrs = psutil.net_if_addrs()
        interfaces = []
        
        for iface_name, addrs in net_if_addrs.items():
            addr_info = []
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    addr_info.append(f"IPv4: {addr.address}")
                elif addr.family == socket.AF_INET6:
                    addr_info.append(f"IPv6: {addr.address}")
            
            if addr_info:
                interfaces.append(f"{iface_name}: {', '.join(addr_info)}")
        
        info['Сетевые интерфейсы'] = '\n'.join(interfaces[:10]) if interfaces else 'Нет данных'
        
        # Network statistics
        try:
            net_io = psutil.net_io_counters()
            info['Отправлено данных'] = f"{net_io.bytes_sent / (1024**2):.2f} МБ"
            info['Получено данных'] = f"{net_io.bytes_recv / (1024**2):.2f} МБ"
            info['Всего пакетов отправлено'] = f"{net_io.packets_sent:,}"
            info['Всего пакетов получено'] = f"{net_io.packets_recv:,}"
        except:
            pass
        
        return info
    
    def get_gpu_info(self):
        """Collect GPU information."""
        info = {}
        
        # Try to get GPU info using different methods
        gpus = []
        
        # Method 1: Using psutil (limited support)
        try:
            # This works on some systems
            import subprocess
            result = subprocess.run(
                ['wmic', 'path', 'win32_VideoController', 'get', 'name'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                gpus = [line.strip() for line in lines if line.strip()]
        except:
            pass
        
        # Method 2: Using pywin32 if available
        if not gpus:
            try:
                import winreg
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"HARDWARE\DESCRIPTION\System\BIOS"
                )
                # This is a fallback, not reliable for GPU
                winreg.CloseKey(key)
            except:
                pass
        
        # Method 3: Display adapter info from platform
        if not gpus:
            try:
                import subprocess
                result = subprocess.run(
                    ['powershell', '-Command', 
                     'Get-WmiObject Win32_VideoController | Select-Object -ExpandProperty Name'],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
                if result.returncode == 0:
                    gpus = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            except:
                gpus = ['Информация недоступна']
        
        info['Видеокарты'] = '\n'.join(gpus) if gpus else 'Не определено'
        
        # Try to get GPU memory (if available)
        try:
            import subprocess
            result = subprocess.run(
                ['powershell', '-Command', 
                 'Get-WmiObject Win32_VideoController | Select-Object AdapterRAM'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            if result.returncode == 0:
                ram_lines = result.stdout.strip().split('\n')[1:]
                gpu_rams = []
                for line in ram_lines:
                    try:
                        ram = int(line.strip())
                        gpu_rams.append(f"{ram / (1024**3):.2f} ГБ")
                    except:
                        pass
                if gpu_rams:
                    info['Память GPU'] = ', '.join(gpu_rams)
        except:
            pass
        
        return info
    
    def populate_tab(self, tab, info_dict):
        """Populate a tab with information."""
        # Clear existing widgets
        for widget in tab.winfo_children():
            widget.destroy()
        
        # Create scrollable text area
        text_widget = scrolledtext.ScrolledText(
            tab, 
            wrap=tk.WORD, 
            font=('Consolas', 10),
            width=80,
            height=20
        )
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Configure grid weights
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)
        
        # Insert information
        for key, value in info_dict.items():
            text_widget.insert(tk.END, f"{key}:\n", 'heading')
            text_widget.insert(tk.END, f"  {value}\n\n", 'content')
        
        # Configure tags for formatting
        text_widget.tag_configure('heading', font=('Consolas', 10, 'bold'))
        text_widget.tag_configure('content', font=('Consolas', 10))
        
        # Make text read-only
        text_widget.config(state=tk.DISABLED)
    
    def populate_system_tab(self):
        """Populate system tab."""
        info = self.get_system_info()
        self.populate_tab(self.system_tab, info)
    
    def populate_cpu_tab(self):
        """Populate CPU tab."""
        info = self.get_cpu_info()
        self.populate_tab(self.cpu_tab, info)
    
    def populate_memory_tab(self):
        """Populate memory tab."""
        info = self.get_memory_info()
        self.populate_tab(self.memory_tab, info)
    
    def populate_disk_tab(self):
        """Populate disk tab."""
        info = self.get_disk_info()
        self.populate_tab(self.disk_tab, info)
    
    def populate_network_tab(self):
        """Populate network tab."""
        info = self.get_network_info()
        self.populate_tab(self.network_tab, info)
    
    def populate_gpu_tab(self):
        """Populate GPU tab."""
        info = self.get_gpu_info()
        self.populate_tab(self.gpu_tab, info)
    
    def refresh_all(self):
        """Refresh all tabs."""
        self.status_var.set("Обновление...")
        self.root.update()
        
        self.populate_system_tab()
        self.populate_cpu_tab()
        self.populate_memory_tab()
        self.populate_disk_tab()
        self.populate_network_tab()
        self.populate_gpu_tab()
        
        self.status_var.set(f"Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def copy_all_info(self):
        """Copy all information to clipboard."""
        all_info = []
        
        # Collect all info
        all_info.append("=" * 60)
        all_info.append("ИНФОРМАЦИЯ О СИСТЕМЕ")
        all_info.append("=" * 60)
        all_info.append("")
        
        for name, info_func in [
            ("Система", self.get_system_info),
            ("Процессор", self.get_cpu_info),
            ("Оперативная память", self.get_memory_info),
            ("Диски", self.get_disk_info),
            ("Сеть", self.get_network_info),
            ("Видеокарта", self.get_gpu_info)
        ]:
            all_info.append(f"\n### {name} ###\n")
            info = info_func()
            for key, value in info.items():
                all_info.append(f"{key}: {value}")
            all_info.append("")
        
        all_info.append("=" * 60)
        all_info.append(f"Дата отчета: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        all_info.append("=" * 60)
        
        # Copy to clipboard
        full_text = '\n'.join(all_info)
        self.root.clipboard_clear()
        self.root.clipboard_append(full_text)
        self.root.update()
        
        self.status_var.set("Информация скопирована в буфер обмена!")


def main():
    """Main entry point."""
    root = tk.Tk()
    
    # Set theme
    style = ttk.Style()
    try:
        style.theme_use('vista')  # Windows Vista theme
    except:
        try:
            style.theme_use('clam')  # Fallback theme
        except:
            pass
    
    app = PCInfoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
