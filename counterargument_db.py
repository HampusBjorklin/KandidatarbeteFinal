import sys, time, re
import json
import pickle
import pandas as pd
from os import listdir
from os.path import isfile, join
from text_cleaning import clean_string

# Read .txt and save as pickled dataframe...
# Get list of all files in directory
def create_dataframe():
    files_list = [f for f in listdir('TextFiles/text_files') if isfile(join('TextFiles/text_files', f))]
    for files in files_list:
        input_name = files

        '''PREPARE TEXTFILE BY REMOVING WHITESPACE, LINEBREAK IN CLAIMS ETC'''
        # Choose input .txt file...
        input_path = "TextFiles/text_files/"
        input_text = input_path+input_name


        # Chose output.txt filename, path...
        output_name = input_name[:-4] + '_prep.txt'
        output_path = "TextFiles/prepared_text_files/"
        output_text = output_path + output_name
        # Load input
        text = open(input_text, "r", encoding='UTF-8')
        lines = text.readlines()
        text.close()

        # Create output.txt
        newfile = open(output_text, 'w', encoding='UTF-8')

        #Clean up
        for i, line in enumerate(lines):
            lines[i] = line
            if line == "" or line == '\n':
                lines.pop(i)

        for i, line in enumerate(lines):
            if line[0] != '1':
                lines[i-1] = (lines[i-1]+ ", " + line).replace('\n','')
                lines.pop(i)

        for i, line in enumerate(lines):
            if i == 0:
                line_tree = line[0:2]
                line_text = line[3:]
                line_fixed = line_tree + ' Pro: ' + line_text
                newfile.write(line_fixed)
            else:
                newfile.write(line)

        newfile.close()

        """RUN THE KIALO-PARSER"""
        #
        #if len(sys.argv) < 3:
        #    print "Not enough arguments. Aborting..."
        #    sys.exit()
        #
        #elif len(sys.argv) > 3:
        #    print "Too many arguments. Aborting..."
        #    sys.exit()

        input_file_json = output_text
        output_path = 'jsonFiles/original_json_files/'
        output_file_json = output_path + input_name[:-4]+'.json'

        with open(input_file_json, 'r', encoding='UTF-8') as fi:
            lines = []
            for line in fi:
                lines.append(line)

            # list containing each parsed comment
            result = []

            # # TO-DO: use discussion title as first entry
            # title = re.search(r"(Discussion Title: )(.*)", lines[0])
            # result.append({
            #     "Title": title.group(2)
            # })

            # we remove the first two lines of the text
            # as we don't need the header

            ##                                            ##
            ##                 REGEDITS                   ##
            ##                                            ##
            # iterate every row in the text file
            for line in lines:
                try:
                    #if line[0].isnumeric() is not True:
                    #    continue

                    # find the tree position the comment is in
                    tree = re.search(r"^(\d{1,}.)+", line)
                    # find if the comment is Pro or Con
                    stance = re.search(r"(Con|Pro)(?::)", line)

                    # find the text of the comment
                    content = re.search(r"((Con|Pro)(?::\s))(.*)", line)
                    # make a dictionary with the single entry
                    # and put it at the end of the list
                    result.append({
                        "Tree": tree.group(),
                        "Stance": stance.group(1),
                        "ToneInput": content.group(3)
                        })
                except:
                    continue

            to_write = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

        with open(output_file_json, 'w') as fo:
            # print to_write
            fo.write(to_write)
            output_message = "Operation completed. Wrote " + str(len(result)) + " entries in " + str(output_file_json)
            print
            print("=" * len(output_message))
            print(output_message)
            print("=" * len(output_message))
            print


        '''PREPARE THE JSON FILE, PUT ALL OBJECTS ON SINGLE LINES ETC'''

        # Load input file, define output file name...
        input_json = output_file_json
        output_path = "jsonFiles/prepared_json_files/"
        output_json_prep = output_path + input_name[:-4]+'_prep.json'
        json_file = open(input_json, "r")

        # Clean up...
        temp = ''
        lines = json_file.readlines()
        lines.pop(0)
        lines.pop(-1)
        json_file.close()

        newfile = open(output_json_prep, 'w')

        for line in lines:
            line = line.strip()
            if line[0] != '}':
                temp = temp + line.replace('\n','')

            else:
                newfile.write(temp + '}\n')
                temp = ''
        newfile.close()

        """CREATE PANDAS DATAFRAME, PICKLE IT"""

        input_json = output_json_prep

        output_path = "Pickles/"
        output_pickle = output_path + input_name[:-4]+'.pkl'

        claims = []
        pro_arguments = []
        con_arguments = []

        current_parent_tree = ''
        current_parent_claim = ''

        def find_parent_claim(parent_tree):
            with open(input_json, buffering=1000) as f:
                parent_claim = ''
                for row in f:
                    row = json.loads(row)
                    if row['Tree'] == parent_tree:
                        parent_claim = row['ToneInput']
                        break
            return parent_claim

        def find_pro_argument(tree):
            with open(input_json, buffering=1000) as f:
                pro_claim = ''
                i = 1
                done = False
                while not done:
                    found = False
                    child_tree = tree + '{}.'.format(i)
                    i += 1
                    for row in f:
                        row = json.loads(row)
                        if row['Tree'] == child_tree:
                            if row['Stance'] == 'Pro':
                                pro_claim = (row['ToneInput'])
                                done = True
                            found = True
                            break
                    if not found:
                        done = True
            return pro_claim

        def find_con_argument(tree):
            with open(input_json, buffering=1000) as f:
                pro_claim = ''
                i = 1
                done = False
                while not done:
                    found = False
                    child_tree = tree + '{}.'.format(i)
                    i += 1
                    for row in f:
                        row = json.loads(row)
                        if row['Tree'] == child_tree:
                            if row['Stance'] == 'Con':
                                pro_claim = (row['ToneInput'])
                                done = True
                            found = True
                            break
                    if not found:
                        done = True
            return pro_claim


        with open(input_json, buffering=1000) as f:
            for row in f:
                row = json.loads(row)
                tree = row['Tree']
                claim = clean_string(row['ToneInput'])
                pro_argument = clean_string(find_pro_argument(tree))
                con_argument = clean_string(find_con_argument(tree))
                stance = row['Stance']
                pro_arguments.append(pro_argument)
                con_arguments.append(con_argument)
                claims.append(claim)

        discussion_dict = {'claim':claims, 'pro_arguments':pro_arguments, 'con_arguments':con_arguments}
        discussion_df = pd.DataFrame(discussion_dict)
        pd.to_pickle(discussion_df, output_pickle)
        print('Successfully created pickled dataframe :-)')
