# Test python file
import config
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from pathlib import Path


def parse_v6(letter):

    cf = config.ConfigFile()
    v6_files_path = (cf.configfile[cf.computername]['v6_files_path'])
    new_v6_files_path = (cf.configfile[cf.computername]['new_v6_files_path'])

    # open the specific html file


    file_name = letter + ".html"
    text_file_path = v6_files_path + file_name
    with open(text_file_path, 'r') as f:
        soup = BeautifulSoup(f, 'html5lib')

    with open(text_file_path) as fp:
        data = fp.read()
    print(diagnose(data))

    # Alternative using pathlib
    output_file_path = Path(new_v6_files_path, "bad-html-parser.html")

    with open(output_file_path, "w") as file:
        pass
        # file.write(str(soup.prettify()))

if __name__ == '__main__':
    parse_v6("E")