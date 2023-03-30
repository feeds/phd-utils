import os
import re
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Rename LaTeX figures that end in .pdf to have only ascii characters.")
    parser.add_argument("directory", type=str, help="The directory to the LaTeX project.")
    args = parser.parse_args()
    return args

def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            new_filename = re.sub(r"[^0-9a-zA-Z\.]+", "0", filename)
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

def update_tex_files(directory):
    tex_files = [filename for filename in os.listdir(directory) if filename.endswith(".tex")]
    for tex_file in tex_files:
        with open(os.path.join(directory, tex_file), "r") as f:
            content = f.read()
        new_content = re.sub(r"\\includegraphics(?:\[(.+?)\])?\{(.+?)\}", lambda match: r"\includegraphics"
                                            + (('[' + match.group(1) + ']') if match.group(1) else '')
                                            + r"{" + re.sub(r'[^0-9a-zA-Z\.]+', '0', match.group(2)) + r"}", content)
        with open(os.path.join(directory, tex_file), "w") as f:
            f.write(new_content)


def main():
    args = parse_arguments()
    directory = args.directory
    rename_files(directory)
    update_tex_files(directory)

if __name__ == "__main__":
    main()
