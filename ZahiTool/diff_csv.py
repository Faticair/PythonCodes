import csv
import os
import datetime

def read_csv_file(csvpath): # read csv file, return a hashdic and a idlist(id is the key of hashdic)
    hashdic = {}
    idlist = []
    with open(csvpath, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            hashdic[row[0]] = row[1:]
            idlist.append(row[0])
    return hashdic, idlist

def set_diff(leftset, rightset): # return the leftset - rightset
    return list(leftset.difference(rightset))

def is_list_diff(oldlist, newlist): # compare the old list and the new list, return whether they are different 
    different = False
    for (olditem, newitem) in zip(oldlist, newlist):
        if olditem != newitem:
            different = True
    return different

def item_print(printmode, items, referdic): # print items
    for index in items:
        # print('\n### ' + printmode + ' item: ' + format_value(referdic.pop(index)))
        mytext = '\n\n### ' + printmode + ' item: ' + format_value(referdic.pop(index))
        output_to_file(mytext)

def format_value(originvalue): # remove the '\t' of origin string 
    return str(originvalue).replace('\\t', '')

def output_to_file(text): # write the output to the designated file
    filepath = 'D:\\Files\\MyJob\\Wireless\\matter\\diff_' + datetime.date.today().isoformat() + '.txt'
    with open(filepath, 'a+', encoding='utf-8') as f:
        f.write(text)

def file_compare(Oldfile, Newfile): # 
    ohashdic, oidlist = read_csv_file(Oldfile)
    nhashdic, nidlist = read_csv_file(Newfile)
    increaseitem = set_diff(set(nidlist), set(oidlist))
    decreaseitem = set_diff(set(oidlist), set(nidlist))
    if not increaseitem:
        # print('### NO new item.')
        output_to_file('\n\n### NO new item.')
    else:
        item_print('New', increaseitem, nhashdic)
    if not decreaseitem:
        # print('### NO item miss.')
        output_to_file('\n\n### NO item miss.')
    else:
        item_print('Miss', decreaseitem, ohashdic)
    # print('\n### Different item: ')
    output_to_file('\n\n### Different item: ')
    count = 0
    for key in nhashdic.keys():
        if is_list_diff(ohashdic[key], nhashdic[key]):
            count += 1
            # print('\n### ' + str(count))
            # print('### New: ' + format_value(nhashdic[key]))
            # print('### Old: ' + format_value(ohashdic[key]))
            mytext = '\n\n### ' + str(count) + '\n### New: ' + format_value(nhashdic[key]) + '\n### Old: ' + format_value(ohashdic[key])
            output_to_file(mytext)
def main():
    rootpath = 'D:\\Files\\MyJob\\Wireless\\matter\\'
    oldfile = input('Old file name: ')
    newfile = input('New file name: ')
    mytext = '\n\n###################\nOld file: ' + oldfile + '\nNew file: ' + newfile + '\n###################'
    output_to_file(mytext)
    file_compare(rootpath + oldfile, rootpath + newfile)
    

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    runningtime = (end_time - start_time)
    print('Task finished. Time used: ' + str(runningtime))