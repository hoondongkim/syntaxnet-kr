import re

# "ㄴ       ETM", "ㄹ     ETM" 처리.. 결과를 list 에 store 했다가, </p> 테그에서 고치고, output

f = open('Data\BTHO0437.txt', 'r', encoding='utf-16')  #

# line = f.readline()
# print (line)

is_inside = False
line_counter = 0

for line in f:
    # print (line)
    chomped_line = line.rstrip()
    if chomped_line == "<p>":
        is_inside = True
        # print ("inside")
    elif chomped_line == "</p>":
        print()
        is_inside = False
        line_counter = 0
        # print ("outside")
    else:
        m1 = re.match('^([^\t]+)\t([^\t]+)\t([^\t]+)$', chomped_line)
        if m1:
            # print ("linenumber", m1.group(1))
            # print ("word", m1.group(2))
            # print ("parsed", m1.group(3))
            parsed = m1.group(3)
            snip_pairs = re.split(' \+ ', parsed)  # +sign needs to be escaped in regex #던지/VV + 어/EC

            for snip_pair in snip_pairs:
                line_counter += 1
                # print ("snip_pair = ", snip_pair) #던지/VV
                m2 = re.match('^([^\/]+)\/([^\/]+)$', snip_pair)
                if m2:
                    snip = m2.group(1)
                    pos = m2.group(2)
                    # print ("line", line_counter)
                    # print ("snip", snip)
                    # print ("pos", pos)
                    print(line_counter, "\t", snip, "\t", pos)
