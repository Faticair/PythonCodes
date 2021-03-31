import csv
import os

def read_csv_file(csvpath):
    hashdic = {}
    idlist = []
    with open(csvpath, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            hashdic[row[0]] = row[1:]
            idlist.append(row[0])
    return hashdic, idlist

def set_diff(leftset, rightset):
    return list(leftset.difference(rightset))

def is_list_diff(oldlist, newlist):
    different = False
    for (olditem, newitem) in zip(oldlist, newlist):
        if olditem != newitem:
            different = True
    return different

def item_print(printmode, items, referdic):
    for index in items:
        print('\n### ' + printmode + ' item: ' + format_value(referdic.pop(index)))

def format_value(originvalue):
    return str(originvalue).replace('\\t', '')

def output_to_file(filepath, text):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(text)

def file_compare(Oldfile, Newfile):
    ohashdic, oidlist = read_csv_file(Oldfile)
    nhashdic, nidlist = read_csv_file(Newfile)
    increaseitem = set_diff(set(nidlist), set(oidlist))
    decreaseitem = set_diff(set(oidlist), set(nidlist))
    if not increaseitem:
        print('### NO new item.')
    else:
        item_print('New', increaseitem, nhashdic)

    if not decreaseitem:
        print('### NO item miss.')
    else:
        item_print('Miss', decreaseitem, ohashdic)
    print('\n### Different item: ')
    count = 0
    for key in nhashdic.keys():
        if is_list_diff(ohashdic[key], nhashdic[key]):
            count += 1
            print('\n### ' + str(count))
            print('### New: ' + format_value(nhashdic[key]))
            print('### Old: ' + format_value(ohashdic[key]))

def main():
    rootpath = 'D:\\Files\\MyJob\\Wireless\\matter\\'
    oldfile = 'AC6805-apInfo-0322-all.csv'
    newfile = 'AC6805-apInfo-0329-all.csv'
    file_compare(rootpath + oldfile, rootpath + newfile)
    

if __name__ == '__main__':
    main()
    # o = [1,2,3,4,5]
    # n = [1,2,3,4,5]
    # print(is_list_diff(o,n))