import re
import codecs

# "ㄴ       ETM", "ㄹ     ETM" 처리.. 결과를 list 에 store 했다가, </p> 테그에서 고치고, output
"""
[1] Main Function
"""
def main():

    f = open('InputDataType1\BTHO0437.txt', 'r', encoding='utf-16')
    is_inside = False
    line_counter = 0
    OUT_FILENAME = "OutputData\kr-ud-dev.conllu"

    with codecs.open(OUT_FILENAME, "w", "utf-8") as file:
        for line in f:
            # print (line)
            chomped_line = line.rstrip()
            if chomped_line == "<p>":
                is_inside = True
                # print ("inside")
            elif chomped_line == "</p>":
                print()
                file.write("\r\n")
                is_inside = False
                line_counter = 0
                # print ("outside")
            else:
                m1 = re.match('^([^\t]+)\t([^\t]+)\t([^\t]+)$', chomped_line)
                if m1:
                    # print("linenumber", m1.group(1))
                    # print("word" , m1.group(2))
                    # print("parsed", m1.group(3))
                    parsed = m1.group(3)
                    snip_pairs = re.split(' \+ ', parsed)  # +sign needs to be escaped in regex #던지/VV + 어/EC

                    for snip_pair in snip_pairs:
                        line_counter += 1
                        # print ("snip_pair = ", snip_pair) #던지/VV
                        m2 = re.match('^([^\/]+)\/([^\/]+)$', snip_pair)
                        if m2:
                            snip = m2.group(1)
                            pos = m2.group(2)
                            # print(line_counter, "\t", snip, "\t", pos)
                            doPrintAndWrite(line_counter, snip, pos , file)


"""
[2] General Function
"""
def retOutputStr(line_counter, snip, pos):
    returnStr = str(line_counter) + "\t" + getFormStr(snip) + "\t" + getLemmaStr(snip) + "\t" + getUpostagStr(pos) + "\t" + \
                getXpostagStr(pos) + "\t" + getFeatsStr(pos) + "\t" + getHeadStr(pos) + "\t" + getDeprelStr(pos) + "\t" + \
                getDepsStr(pos)
    return returnStr

def doPrintAndWrite(line_counter, snip, pos, file):
    outputStr = retOutputStr(line_counter, snip, pos)
    print(outputStr)
    file.write(outputStr + "\r\n")


"""
[3] CoNLL-U Format Function
1.ID: Word index, integer starting at 1 for each new sentence; may be a range for tokens with multiple words.
2.FORM: Word form or punctuation symbol.
3.LEMMA: Lemma or stem of word form.
4.UPOSTAG: Universal part-of-speech tag drawn from our revised version of the Google universal POS tags.
5.XPOSTAG: Language-specific part-of-speech tag; underscore if not available.
6.FEATS: List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available.
7.HEAD: Head of the current token, which is either a value of ID or zero (0).
8.DEPREL: Universal Stanford dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one.
9.DEPS: List of secondary dependencies (head-deprel pairs). i.MISC: Any other annotation.
"""
# 2.FORM - FORM 이 필수는 아님. Japna 참고. 현재 snip_pairs 에 의해 한 행이 복수 행으로 분리 되므로, Form 을 비워두었음.
def getFormStr(snip):
    return "_"

# 3.LEMMA
def getLemmaStr(snip):
    return snip

# 4.UPOSTAG - 이 부분 좀더 Dictionary 에 맵핑 규칙을 보충해 넣어야 함.
def getUpostagStr(pos):
    tagDic = dict()
    tagDic['NNG'] = 'NOUN'
    tagDic['VV'] = 'VERB'
    tagDic['MM'] = 'DET'
    tagDic['SF'] = 'PUNCT'
    if pos in tagDic.keys():
        return tagDic[pos]
    else :
        return pos

# 5.XPOSTAG
def getXpostagStr(pos):
    return pos

# 6.FEATS
def getFeatsStr(pos):
    return "_"

# 7.HEAD
def getHeadStr(pos):
    return "_"

# 8.DEPREL
def getDeprelStr(pos):
    return "_"

# 9.DEPS
def getDepsStr(pos):
    return "_"


"""
[4] Main Function Call
"""
if __name__ == "__main__":
    main()