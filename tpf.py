# Test python file
import config
from bs4 import BeautifulSoup
from pathlib import Path


def parse_v6(letter):

    cf = config.ConfigFile()
    v6_files_path = (cf.configfile[cf.computername]['v6_files_path'])
    new_v6_files_path = (cf.configfile[cf.computername]['new_v6_files_path'])

    # open the specific html file
    file_name = letter + ".html"
    text_file_path = v6_files_path + file_name
    with open(text_file_path, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")

    output_file_path = Path(new_v6_files_path, file_name)

    with open(output_file_path, "w") as file:
        file.write(str(soup))

if __name__ == '__main__':
    parse_v6("E")