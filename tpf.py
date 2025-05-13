import config

def parse_v6(letter):
    cf = config.ConfigFile()
    v6_files_path = cf.configfile[cf.computername]['v6_files_path']
    new_v6_files_path = cf.configfile[cf.computername]['new_v6_files_path']

    # Open the specific HTML file
    file_name = letter + ".html"
    text_file_path = v6_files_path + file_name
    with open(text_file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, "lxml")

    print(soup.get_text())

    # Find all <b> tags
    b_tags = soup.find_all('b')

    # Loop through each <b> tag
    for b_tag in b_tags:
        if b_tag.string and b_tag.string.isdigit():
            tree_tag = soup.new_tag('tree')
            tree_tag.string = b_tag.string
            b_tag.replace_with(tree_tag)

    output_file_path = Path(new_v6_files_path, file_name)

    with open(output_file_path, "w", encoding='utf-8') as file:
        file.write(str(soup))

if __name__ == '__main__':
    parse_v6("E")