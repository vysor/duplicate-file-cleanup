import os

extension = [
    "png", "tiff", "bmp", "jpg",
    "jpeg", "gif", "eps", "raw",
    "mp4", "mov", "avi", "mp3"
]

# Check for temporary file names this script uses
def startup():
    os.system("cp ./files.txt ./files.txt.old")
    os.system("cp ./hash.csv ./hash.csv.old")

# Clean up temporary files
def garbage():
    os.system("cp ./files.txt ./files.txt.tmp")
    os.system("cp ./files.txt.old ./files.txt")
    os.system("cp ./hash.csv ./hash.csv.old")


# Find all images and save the filenames
def find_media():
    print("Looking for media on the laptop...")
    for filetype in extension:
        os.system(f"find /usr/share/icons -name *.{filetype} >> files.txt")
        print(f"Found all .{filetype} files")

    print("*** All media thata will be checked for duplicates, had been found ***")
    print("*** Confirming the list ***")

    # Check that all files are unique and remove dirs that shouldn't be checked
    os.system("mv files.txt files.check.txt")
    os.system("sort files.check.txt | uniq > files.txt")
    os.system("rm files.check.txt")
    os.system("cat files.txt | grep -v \"/usr/share\" > files.out.txt")
    os.system("rm files.txt")
    os.system("mv files.out.txt files.txt")

    print("*** Confirmed! ***")


# Get hashes for all files
def get_hash():
    f = open("files.txt", "r")
    out = open("hash.csv", "w+")
    for path in f.readlines():
        out.write(f"{hash(path)},{path}")

    f.close()
    out.close()

    print("*** Hashes have been written to file ***")


# Remove duplicate hashes
def rem_dups():
    print("Runing: rem_dups")
    media = {}
    hash_file = open("hash.csv", "r")
    
    for line in hash_file.readlines():
        key, path = line.split(",")
        if key in media:
            tmp = media[key]
            tmp.append(path)
            media[key] = tmp
        else:
            media[key] = list(path)

    hash_file.close()
    print("MEDIA")
    l = len(media.keys())
    print(f"{l} files to check")
    if l == 0:
        exit(0)

startup()
find_media()
get_hash()
rem_dups()
garbage()
print("Done! Exiting program")
