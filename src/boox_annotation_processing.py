import os
import regex as re
import sys


def format_boox_annotations(raw_file):
    # replace all lines like "-------------------" with newline character to tidy code
    raw_file = [
        line if line.strip() != "-------------------" else "\n" for line in raw_file
    ]

    new_file = []
    group_lines = []

    for i, line in enumerate(raw_file):
        # store previous line if it exists
        if i > 0:
            previous_line = raw_file[i - 1].strip()
        else:
            # Make a placeholder for the first line...
            previous_line = "None"
            line = "# " + line.strip()

        next_line = raw_file[i + 1].strip() if i < len(raw_file) - 1 else ""

        if re.search(r"\d{4}-\d{2}-\d{2}", line):
            # If a date line is found, join the group of lines and add them to 'new_file'
            if group_lines:
                new_line = " ".join(group_lines)
                new_file.append(new_line)
                group_lines = []
            # take the page number from the date line
            page = re.search(r"Page No.: (\d+)", line).group(1)
            # Add the page number to the group of lines
            group_lines.append(f"- Pg{page}.")

        # If a line is empty and the next is a date line join the group of lines and add them to 'new_file'
        elif line.strip() == "" and re.search(r"\d{4}-\d{2}-\d{2}", next_line):
            if group_lines:
                new_line = " ".join(group_lines)
                new_file.append(new_line)
                group_lines = []
                new_file.append("\n\n")  # Append an empty line

        # If line is empty and the next is not a date line, add the line to new file (Chapter in second line)
        elif line.strip() == "" and not re.search(r"\d{4}-\d{2}-\d{2}", next_line):
            if group_lines:
                new_line = " ".join(group_lines)
                new_file.append(new_line)
                group_lines = []
                new_file.append("\n\n")  # Append an empty line

        # If previous line is empty and the next is not a date line, add the line to new file (Chapter title)
        elif previous_line.strip() == "" and re.search(r"\d{4}-\d{2}-\d{2}", next_line):
            new_file.append("## " + line.strip())
            new_file.append("\n\n")
            continue

        elif i == 0:
            new_file.append(line)
            new_file.append("\n\n")  # Append an empty line

        else:
            if i == 1:
                new_file.append("## " + line.strip())
                new_file.append("\n\n")
                continue
            # Add non-empty lines to the group
            group_lines.append(line.strip())
            # new_file.append('\n')  # Append an empty line

    # Join any remaining lines in the group (if not followed by a date or empty line)
    if group_lines:
        new_line = " ".join(group_lines)
        new_file.append(new_line)

    return new_file


def read_input_file(input_file):
    with open(input_folder + "\\" + input_file, "r", encoding="utf-8") as f:
        raw_file = f.readlines()

    # extract the first_line
    first_line = raw_file[0].strip()
    # title is between <<>>, use regex to extract
    title = re.search(r"<<(.*)>>", first_line).group(1)
    # replace the first line with the title
    raw_file[0] = title + "\n"

    return raw_file, title


if __name__ == "__main__":
    # check for system arguments
    if len(sys.argv) == 3:
        input_folder, output_folder = sys.argv[1], sys.argv[2]
        # check if the input and output folders are correctly specified with a trailing slash
        if input_folder[-1] != "\\":
            input_folder += "\\"
        if output_folder[-1] != "\\":
            output_folder += "\\"

        print(f"Input folder: {input_folder}")
        print(f"Output folder: {output_folder}\n")
    else:
        print(
            "Usage: python boox_annotation_processing.py <input_folder> <output_folder>"
        )
        print("Check system arguments are correctly specified, exiting.")
        exit()

    # Get all the files in the input folder
    try:
        input_files = os.listdir(input_folder)
    except FileNotFoundError:
        print(f"Directory '{input_folder}' not found, exiting.")
        print("Check that the given directory is correctly specified.\n")
        exit()

    # loop through the exported annotations in the input folder
    for file in input_files:
        # read the input file
        input_file, title = read_input_file(file)

        # format the file
        new_file = format_boox_annotations(input_file)

        # check if the file exists in the output folder already
        if os.path.exists(output_folder + title + ".md"):
            print(
                f"The file '{title}' already exists in the output folder and has not been saved.\n"
            )
            continue
        print(f"Saving '{title}' to the output folder '{output_folder}'.\n")
        # save the new file as .md with the title as the filename
        try:
            with open(output_folder + title + ".md", "w", encoding="utf-8") as f:
                f.writelines(new_file)
        except FileNotFoundError:
            print(f"Directory '{output_folder}' not found, exiting.")
            print("Check that the given directory is correctly specified.\n")
            exit()
