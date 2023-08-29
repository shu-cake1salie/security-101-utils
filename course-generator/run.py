import os
import csv

def deduce_course_type(type: str, selective: str) -> str:
    """ deduce the course type to HTML code

    Args:
        type (str): only '计算机' or '网安'
        selective (str): only '必修' or '选修'

    Returns:
        str: the return HTML code
    """
    if type not in ('计算机', '网安'):
        raise ValueError(f"Unknown course type: {type}")
    if selective not in ('必修', '选修'):
        raise ValueError(f"Unknown course selective: {selective}")
    
    if type == '计算机':
        return f'<span class="badge cs-badge">计算机 <{selective}></span>'
    else:
        return f'<span class="badge is-badge">网安 <{selective}></span>'


def deduce_folder_name(code: str, name: str) -> str:
    """ deduce the folder name, cut the code after '~'

    Args:
        code (str): the course code
        name (str): the course name

    Returns:
        str: the folder name
        
    Examples:
        >>> deduce_folder_name('08305009~010', '数据结构')
        '08305009_数据结构'
    """
    if '~' not in code:
        return f"{code}_{name}"
    else: # 08305009-010 -> 08305009
        return f"{code.split('~')[0]}_{name}"


def generator():
    """ generate the course folder and index.md file
    """
    os.makedirs('outputs', exist_ok=True)

    # read the template file
    with open('template.md', 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    with open('courses.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            folder_name = deduce_folder_name(row[0], row[1])
            output_folder = os.path.join('outputs', folder_name)
            os.makedirs(output_folder, exist_ok=True)

            _1_course_name = row[2] # 高级语言程序设计
            _2_course_code = row[0] # 08304135
            _3_course_type = deduce_course_type(row[3], row[4])


            filled_template = template_content\
                                .replace('$1', _1_course_name)\
                                .replace('$2', _2_course_code)\
                                .replace('$3', _3_course_type)


            with open(os.path.join(output_folder, 'index.md'), 'w', encoding='utf-8') as index_file:
                index_file.write(filled_template)

            print(f"Created folder: {output_folder}")

    print("Batch processing completed.")


def mkdocs_helper():
    """ generate the mkdocs.yml helper
    """
    
    with open('courses.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            folder_name = deduce_folder_name(row[0], row[1])
            
            if row[3] == '计算机':
                print(f"- {row[2]}: 1_course_computer/{folder_name}/index.md")
            else:
                print(f"- {row[2]}: 2_course_security/{folder_name}/index.md")
                
    print("Batch processing completed.")

if __name__ == '__main__':
    generator()
    mkdocs_helper()