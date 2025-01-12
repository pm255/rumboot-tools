import serial
import sys
import os
from parse import parse
import time
import io
from tqdm import tqdm
from rumboot.OpFactory import OpFactory
from rumboot.chips.base import chipBase
from rumboot.ImageFormatDb import ImageFormatDb
from rumboot.xfer import xferManager
from serial.serialutil import to_bytes
import socket
import select

if sys.platform != "win32":
	import tty
	import termios
else:
    import codecs
    import ctypes

class terminal:
        verbose=True
        logstream=None
        plusargs={}
        initial_loop_done = False
        runlist = []
        formats = ImageFormatDb("rumboot.images")
        chip = chipBase()
        dumps = {}
        curbin = "bootrom"
        progress = tqdm(disable=True)
        replay = False
        replay_till_the_end = False
        ser = None
        cmdline = None
        xfer = None
        xferparams = None
        desc_widget = None
        prog_widget = None
        shell_prompt = None

        def __fixCodePage(self):
            if sys.__stdout__.encoding != 'cp65001':
                os.system("echo off")
                os.system("chcp 65001") # Change active page code
                sys.__stdout__.write("\x1b[A") # Removes the output of chcp command
                sys.__stdout__.flush()
            LF_FACESIZE = 32
            STD_OUTPUT_HANDLE = -11
    
            class COORD(ctypes.Structure):
                _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
    
            class CONSOLE_FONT_INFOEX(ctypes.Structure):
                _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]
    
            font = CONSOLE_FONT_INFOEX()
            font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
            font.nFont = 12
            font.dwFontSize.X = 7
            font.dwFontSize.Y = 12
            font.FontFamily = 54
            font.FontWeight = 400
            font.FaceName = "Lucida Console"
            handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font))

        def __init__(self, port, speed, xferparams = None):
            if sys.platform == 'win32':
                self.__fixCodePage()
            self.port = port
            self.speed = speed
            self.reopen(port, speed, xferparams)

        def serial(self):
            return self.ser

        def reopen(self, port=None, speed=None, xferparams = None):
            if port != None:
                self.port = port
            if speed != None:
                self.speed = speed
            if xferparams != None:
                self.xferparams = xferparams

            if self.xfer != None:
                self.xfer.close()

            self.xfer = xferManager(self, self.xferparams)

            if self.ser != None:
                self.ser.close()
                self.ser = None

            if self.port.find("file://") == 0:
                self.ser = open(self.port.replace("file://",""), "rb+")
                self.replay = True
            elif self.port.find("://") < 0:
                self.ser = serial.Serial(self.port, self.speed, timeout=5)
            else:
                self.ser = serial.serial_for_url(self.port, timeout=5)
            self.opf = OpFactory("rumboot.ops", self) 

        def close(self):
            self.ser.close()
            self.ser = None
            self.progress.close()

        def hack_enable_serial_delay(self, delay):
            if hasattr(self.ser,"__write_orig"):
                raise("INTERNAL ERROR: serial delay hack already applied")

            def write_delayed(data):
                data = to_bytes(data)
                data = [bytes([b]) for b in data]
                for b in data:
                    self.ser.__write_orig(b)
                    time.sleep(delay)


            if not hasattr(self.ser, '__write_orig'):
                self.ser.__write_orig = self.ser.write
                self.ser.write = write_delayed

        def set_chip(self, chip):
            self.chip = chip
            self.xfer.setChip(chip)
            if self.hack("serial_delay"):
                self.hack_enable_serial_delay(0.00005)

        def tqdm(self, *args, **kwargs):
            self.progress.close()
            self.progress = tqdm(*args, **kwargs)

        def add_binaries(self, path):
            if type(path) is list:
                for p in path:
                    self.runlist.append(p[0])
            else:
                self.runlist.append(path)

        def load_binaries(self, path, use_stdin=False, break_after_uploads=True, timeout=-1):
            self.add_binaries(path)
            return terminal.loop(use_stdin, break_after_uploads, timeout)

        def add_dumps(self, dumps):
            self.dumps.update(dumps)

        def next_binary(self, peek=False):
            if len(self.runlist) > 0:
                ret = self.runlist[0]
                if not peek:
                    self.runlist.pop(0)
                    self.curbin = ret
                return ret
            return None

        def current_binary(self):
            return self.curbin

        def current_dump(self):
            if self.curbin == "bootrom":
                return self.dumps["rom"]
            if self.curbin.name in self.dumps:
                return self.dumps[self.curbin.name]

        def log(self, skipecho, *args, **kwargs):
            # Sometimes we get a weird exception on certain windows systems/setups
            # Try to catch any exceptions and dispose of them here
            try:
                if not skipecho and self.verbose:
                    self.progress.write(*args, **kwargs)
                    sys.stdout.flush()
                if not self.logstream == None:
                    self.logstream.write(*args)
                    self.logstream.write("\n")
            except:
                pass


        def sync(self):
            if not self.replay:
                self.ser.reset_input_buffer()
            c1 = b'a'
            c2 = b'd'
            while True:
                c2 = self.ser.read(1)
                if c1 == b'U' and c2 == b'\r':
                    break
                if c1 == b'U' and c2 == b'\n':
                    break
                c1 = c2

        def hack(self, name):
            if name in self.chip.hacks and self.chip.hacks[name]:
                return True
            return False

        def set_progress_widgets(self, desc_widget = None, prog_widget = None):
            self.desc_widget = desc_widget
            self.prog_widget = prog_widget

        def progress_start(self, description, total):
            if self.prog_widget == None:
                self.tqdm(desc=description, total=total, unit_scale=True, unit_divisor=1024, unit='B', disable=False)
            else:
                pass

        def progress_update(self, total, position, increment):
            self.progress.update(increment)

        def progress_end(self):
            self.tqdm(disable=True)

        def wait(self, format, timeout=1000):
            while True:
                line = self.ser.read_until()
                line = line.decode(errors="replace").rstrip()
                self.log(False, line, end='\n')
                ret = parse(format, line)
                if ret != None:
                    return ret

        def shell_mode(self, prompt):
            self.shell_prompt = prompt

        def wait_prompt(self, initial=False):
            if initial:
                self.ser.write(b"\r\n")
            found = False
            data = b""
            while True:
                ret = self.ser.read_until(self.shell_prompt.encode())
                data = data + ret
                ret = ret.decode(errors="replace")
                self.log(False, ret, end='\n')
                if ret.find(self.shell_prompt) > -1:
                    found = True
                    if not initial:
                        break
                if found and len(ret) == 0:
                    break
            return data

        def shell_cmd(self, cmd, timeout=10, initial=False):
            if initial:
                self.wait_prompt(initial)
            cmd = cmd.encode() + b"\r"
            self.ser.write(cmd)
            ret = self.wait_prompt(False).decode(errors="replace")
            ret = ret[len(cmd):] 
            ret = ret[:-len(self.shell_prompt)-2]
            return ret                  

        def loop(self, use_stdin=False, break_after_uploads=False, timeout=-1):
            if not self.initial_loop_done:
                self.initial_loop_done = True
                self.opf.on_start()

            return_code = 0
            time_start = time.time()
            if use_stdin:
                old_settings = termios.tcgetattr(sys.stdin)
            try:
                if use_stdin:
                    tty.setcbreak(sys.stdin.fileno())

                if not self.hack("skipsync"):
                    self.sync()
                while True:
                    ret = None
                    if use_stdin : 
                        line = b''
                        sym = b''
                        while sym != b'\n':
                            if select.select([self.ser], [], [], 0) == ([self.ser], [], []):
                                sym = self.ser.read(1)
                                line = line + sym
                                sys.stdout.write(str(sym, 'utf-8', errors='replace'))
                                sys.stdout.flush()
                            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                                insym = sys.stdin.read(1)
                                self.ser.write(insym.encode())
                    else:
                        line = self.ser.readline()

                    if timeout >= 0 and time.time() - time_start > timeout:
                        return_code = 5
                        break

                    if line == b'':
                        continue
                    try: 
                        line = line.decode().rstrip()
                    except:
                        continue

                    ret = self.opf.handle_line(line, use_stdin)
                    if type(ret) is int:
                        if not self.replay_till_the_end:
                            return ret
                        else:
                            return_code = ret
                    
                    if break_after_uploads and len(self.runlist) == 0:
                        break

                    if self.replay:
                        if (self.ser.tell() == os.fstat(self.ser.fileno()).st_size):
                            print("== END OF LOG REACHED ==")
                            break
            finally:
                if use_stdin:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    return return_code
