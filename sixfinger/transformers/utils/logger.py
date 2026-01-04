"""
Progress logging with colors and emojis
"""

import sys
import time
from typing import Optional, Dict, Any
from contextlib import contextmanager


class ProgressLogger:
    """
    Colorful console logger with progress tracking
    
    Example:
        >>> logger = ProgressLogger()
        >>> logger.section("Training")
        >>> logger.info("Starting...")
        >>> logger.success("Done!")
    """
    
    # ANSI color codes
    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'reset': '\033[0m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'underline': '\033[4m',
    }
    
    # Emojis
    ICONS = {
        'rocket': '🚀',
        'fire': '🔥',
        'star': '⭐',
        'check': '✅',
        'cross': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'folder': '📂',
        'file': '📄',
        'chart': '📊',
        'brain': '🧠',
        'lightning': '⚡',
        'hourglass': '⏳',
        'clock': '🕐',
        'save': '💾',
        'load': '📥',
        'book': '📚',
        'write': '✍️',
        'gear': '⚙️',
        'test': '🧪',
        'package': '📦',
    }
    
    def __init__(self, enabled: bool = True, use_color: bool = True):
        """
        Args:
            enabled: Enable/disable logging
            use_color: Use ANSI colors (auto-detected for terminals)
        """
        self.enabled = enabled
        self.use_color = use_color and sys.stdout.isatty()
        self._start_time = time.time()
    
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text"""
        if not self.use_color:
            return text
        color_code = self.COLORS.get(color, '')
        reset = self.COLORS['reset']
        return f"{color_code}{text}{reset}"
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds to human readable"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
    
    # ===== Core logging methods =====
    
    def section(self, title: str, char: str = '='):
        """Print a section header"""
        if not self.enabled:
            return
        
        width = 60
        print(f"\n{char * width}")
        print(f"  {self._colorize(title, 'bold')}")
        print(f"{char * width}\n")
    
    def subsection(self, title: str):
        """Print a subsection"""
        if not self.enabled:
            return
        print(f"\n{self._colorize(title, 'cyan')}")
        print(f"{'-' * len(title)}")
    
    def info(self, message: str, icon: str = 'info'):
        """Info message"""
        if not self.enabled:
            return
        emoji = self.ICONS.get(icon, '')
        print(f"{emoji} {message}")
    
    def success(self, message: str, icon: str = 'check'):
        """Success message"""
        if not self.enabled:
            return
        emoji = self.ICONS.get(icon, '')
        colored = self._colorize(message, 'green')
        print(f"{emoji} {colored}")
    
    def warning(self, message: str, icon: str = 'warning'):
        """Warning message"""
        if not self.enabled:
            return
        emoji = self.ICONS.get(icon, '')
        colored = self._colorize(message, 'yellow')
        print(f"{emoji} {colored}")
    
    def error(self, message: str, icon: str = 'cross'):
        """Error message"""
        if not self.enabled:
            return
        emoji = self.ICONS.get(icon, '')
        colored = self._colorize(message, 'red')
        print(f"{emoji} {colored}", file=sys.stderr)
    
    def debug(self, message: str):
        """Debug message (dimmed)"""
        if not self.enabled:
            return
        colored = self._colorize(message, 'dim')
        print(f"  {colored}")
    
    # ===== Progress tracking =====
    
    def progress(
        self,
        current: int,
        total: int,
        prefix: str = '',
        suffix: str = '',
        length: int = 40
    ):
        """
        Print progress bar
        
        Args:
            current: Current progress
            total: Total items
            prefix: Prefix string
            suffix: Suffix string
            length: Bar length in characters
        """
        if not self.enabled:
            return
        
        percent = current / max(total, 1)
        filled = int(length * percent)
        bar = '█' * filled + '░' * (length - filled)
        
        print(f"\r{prefix} |{bar}| {percent*100:.1f}% {suffix}", end='', flush=True)
        
        if current >= total:
            print()  # New line when complete
    
    @contextmanager
    def progress_context(self, total: int, desc: str = "Progress"):
        """
        Context manager for progress tracking
        
        Example:
            >>> with logger.progress_context(100, "Processing") as update:
            >>>     for i in range(100):
            >>>         update(i)
        """
        class ProgressUpdater:
            def __init__(self, logger, total, desc):
                self.logger = logger
                self.total = total
                self.desc = desc
                self.current = 0
                
            def update(self, n: int = 1):
                self.current += n
                self.logger.progress(self.current, self.total, prefix=self.desc)
        
        updater = ProgressUpdater(self, total, desc)
        try:
            yield updater.update
        finally:
            if updater.current < total:
                self.progress(total, total, prefix=desc)
    
    # ===== Special formats =====
    
    def table(self, data: Dict[str, Any], title: str = None):
        """Print key-value table"""
        if not self.enabled:
            return
        
        if title:
            print(f"\n{self._colorize(title, 'bold')}")
        
        max_key_len = max(len(str(k)) for k in data.keys())
        
        for key, value in data.items():
            key_str = str(key).ljust(max_key_len)
            key_colored = self._colorize(key_str, 'cyan')
            print(f"  {key_colored} : {value}")
        
        print()
    
    def metric(self, name: str, value: Any, unit: str = ''):
        """Print metric"""
        if not self.enabled:
            return
        
        name_colored = self._colorize(name, 'bright_blue')
        value_colored = self._colorize(str(value), 'bold')
        print(f"  • {name_colored}: {value_colored} {unit}")
    
    def header(self, text: str):
        """Print large header"""
        if not self.enabled:
            return
        
        width = 60
        print()
        print('█' * width)
        print('█' + ' ' * (width - 2) + '█')
        centered = text.center(width - 4)
        print(f"█  {self._colorize(centered, 'bold')}  █")
        print('█' + ' ' * (width - 2) + '█')
        print('█' * width)
        print()
    
    def elapsed(self, prefix: str = "Elapsed"):
        """Print elapsed time since logger creation"""
        if not self.enabled:
            return
        
        elapsed = time.time() - self._start_time
        formatted = self._format_time(elapsed)
        self.info(f"{prefix}: {formatted}", icon='clock')
    
    # ===== Spinners and animations =====
    
    @contextmanager
    def spinner(self, message: str):
        """
        Animated spinner (simple version)
        
        Example:
            >>> with logger.spinner("Loading..."):
            >>>     time.sleep(2)
        """
        if not self.enabled:
            yield
            return
        
        import threading
        
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        stop_spinner = threading.Event()
        
        def animate():
            idx = 0
            while not stop_spinner.is_set():
                char = spinner_chars[idx % len(spinner_chars)]
                print(f"\r{char} {message}...", end='', flush=True)
                idx += 1
                time.sleep(0.1)
        
        thread = threading.Thread(target=animate, daemon=True)
        thread.start()
        
        try:
            yield
        finally:
            stop_spinner.set()
            thread.join(timeout=0.5)
            print(f"\r{self.ICONS['check']} {message}... Done!")


# ===== Singleton instance =====
default_logger = ProgressLogger()


# ===== Convenience functions =====
def info(msg: str): default_logger.info(msg)
def success(msg: str): default_logger.success(msg)
def warning(msg: str): default_logger.warning(msg)
def error(msg: str): default_logger.error(msg)
def section(title: str): default_logger.section(title)