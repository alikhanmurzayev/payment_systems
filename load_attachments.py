import gmail
import read_files


def load():
    attached_files = gmail.parse_gmail()
    read_files.files_into_database(attached_files)
    if attached_files:
        print('saved files:\n' + '\n'.join(attached_files))
    else:
        print('no saved files')



