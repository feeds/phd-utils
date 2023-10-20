import os
import re
import argparse
import hashlib

def parse_arguments():
    parser = argparse.ArgumentParser(description="Rename LaTeX figures that end in .pdf to have only ascii characters.")
    parser.add_argument("directory", type=str, help="The directory to the LaTeX project.")
    args = parser.parse_args()
    return args
fig_i = 0
def rename_and_replace(match):
    global fig_i
    file_name = match.group(2)
    file_name_hash = hashlib.md5(file_name.encode()).hexdigest()

    # Get the file's extension (e.g., .txt, .jpg)
    _, file_extension = os.path.splitext(file_name)

    # Construct the new filename as the hash value with the original extension
    new_file_name = f"Fig{fig_i}Fig" + file_name_hash + file_extension
    fig_i += 1
    # Rename the file
    if not os.path.exists(new_file_name) and os.path.exists(file_name):
        os.rename(file_name, new_file_name)
    tex_new = r"\includegraphics"  + (('[' + match.group(1) + ']') if match.group(1) else '') + r"{" + new_file_name + r"}"
    return tex_new

def update_tex_files(directory,tex_file):

    with open(os.path.join(directory, tex_file), "r") as f:
        content = f.read()

    new_content = re.sub(r"\\includegraphics(?:\[(.+?)\])?\{(.+?)\}", rename_and_replace, content)

    
    with open(os.path.join(directory, tex_file), "w") as f:
       f.write(new_content)


def main():
    args = parse_arguments()
    directory = args.directory
    #rename_files(directory)
    update_tex_files(directory,'main.tex')

if __name__ == "__main__":
    main()
