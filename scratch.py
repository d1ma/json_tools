import json
import os

def special_case(special_id):
    return {'32010-457': ('2010', '00457'),
     '210-1626' : ('2010', '01626'),
     '201-107'  : ('2010', '00107'),
     '201-464'  : ('2010', '00464'),
     '201-545'  : ('2010', '00545'),
     '20112-1004': ('2012', '01004'),
     '20112-1938': ('2012', '01938'),
     '20113-176' : ('2013', '00176'),
     '20113-1135': ('2013', '01135'),
     '203-1675'  : ('2013', '01675'),
     '337500'    : ('2011', '00532'),
     }.get(special_id, (special_id, None, None))

def get_id(full_id):
    ##  09-1234 -> 2009
    ##  2010-1222 -> 2010

    if "-" in full_id:
        split_id = full_id.split("-")
        split_id = [x for x in split_id if len(x) > 0]
        if len(split_id) >= 3:
            # handle unusual case of having letters
            print "Do not support", full_id
            return (full_id, None, None)
        elif len(split_id) < 2:
            print "Do not support", full_id
            return (full_id, None, None)
        else:
            year, order_id = split_id
            if len(year) == 2:
                return (full_id, "20" + year, order_id.zfill(5))
            elif len(year) == 4:
                return (full_id, year, order_id.zfill(5))
    else:
        # no dash in the full_id
        try:
            potential_year = int(full_id[:4])
            if (potential_year > 2000 and potential_year <= 2016):
                year = str(potential_year)
                order_id = full_id[4:]
                return (full_id, year, order_id.zfill(5))
        except ValueError as e:
            pass

    return special_case(full_id)


ROOT = "/Volumes/Seagate Backup Plus Drive/dfl scanned files/"
SCAN = os.path.join(ROOT, "scanned_files")
REPORT = os.path.join(ROOT, "reports")
SCANNED_DIRS = os.listdir(SCAN)
REPORT_DIRS = os.listdir(REPORT)

def get_matching_dirname(dirs, year, order):

    match = [dir_name for dir_name in dirs if dir_name[:4] == year and dir_name[-5:] == order]
    
    if len(match) > 1:
        print "too many matches", year, order
        print match
        return None
    elif len(match) == 0:
        return None
    else:
        return match[0]

def get_files_inside(base_dir, child_dir):
    if child_dir:
        full_dir = os.path.join(base_dir, child_dir)
        files_inside = os.listdir(full_dir)

        return [os.path.join(full_dir, filename) for filename in files_inside if filename_ok(filename)]
    else:
        return []

def filename_ok(f):
    # TODO return False on file formats we don't want
    return True

def id_tuple_to_filesys_path(id_tuple):
    year = id_tuple[1]
    order_id = id_tuple[2]
    if (year and order_id):
        matching_scan_dir = get_matching_dirname(SCANNED_DIRS, year, order_id)
        matching_report_dir = get_matching_dirname(REPORT_DIRS, year, order_id)

        return get_files_inside(SCAN, matching_scan_dir) + get_files_inside(REPORT, matching_report_dir)



    # produce [matching paths]
