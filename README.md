# SpongeWare

SpongeWare is an open-source PoC ransom malware payload generator. I initially developed this project during a cyber training exercise, but have since decided to opensource it because it is pretty cool and someone may be able to learn from it. It uses curve25519 elliptical curve cryptography with ephemeral keys to encrypt files. Read more about that [here](https://cr.yp.to/ecdh.html)

# **Warning**
This is script generates a live piece of malware that can permanently destroy your data and system. If you do not know what you're doing, please do not run this. I am pushing this code to the public domain with the intent to educate. I am **NOT** liable for any misuse, modification, or distribution of this script or any of its code.


# Dependencies

Executing the payload generation script requires a few dependencies:
- \>Python 3.6
- PyNacl 1.4.0
- Pathlib 1.0.1
- Pillow 9.0.0
- Pyinstaller LATEST

# Usage

The `ransomware.py` file alone is just an injectable template for the payload. To generate the payload, you must run the `init_malware.py` script. It will generate two files, both identified by a unique **UUID**. The files are in the format `UUID - ransomware.py` and `UUID.json`. Inside the `json` file you will find the `public key`, `private key`, `uuid`, and the `image data` for that specific instance of the payload. The `.py` file it generates will be the live payload.

This system was designed to be compiled and shaded into a binary executable for the target OS (preferrably using pyinstaller). You must shade the executable on the OS you will be targetting (so if you want to target windows, you must run pyinstaller on a windows host). As of now I have not found a workaround for the native libraries. Once you've got all dependencies and OS requirements, you can use the command `pyinstaller --icon sponge.ico --hidden-import=_cffi_backend --onefile 'UUID - ransomware.py'` to compile it into an executable.

The malware can be triggered a few ways. The first way is via double clicking or executing without arguments. This will trigger the malware in `encryption` mode starting on the `root` directory of your system (`/` if linux, `C:\` if windows).

You can also supply the following arguments:

`--path` Specify the hierarchial parent directory to start encrypting (recursively downards).

`--key` Input a matching private key to decrypt files. If the inputted key is incorrect, the program will exit.



*The sponge icon and skull gif do not belong to me. All credit goes to their original artists (I cannot find them)*

