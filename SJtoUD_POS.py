import re
import codecs
import os

"""
[1] Main Function
"""
def main():
    directory = os.getcwd() + '/InputDataType1'
    filename = 'BTHO0437.txt'
    filename = os.path.join(directory, filename)

    f = open(filename, 'r', encoding='utf-16')
    is_inside = False
    line_counter = 0
    OUT_FILENAME = "OutputDataType1\kr-ud-dev.conllu"

    with codecs.open(OUT_FILENAME, "w", "utf-8") as file:
        """
        한 줄을 읽을 때마다 그 결과를 sniparray, posarray에 저장합니다.

        한 줄에서 형태소를 읽을 때마다 바로바로 출력하지 않고
        다 읽고 난 다음 그 결과를 출력하는데 그 이유는 다음과 같습니다.

        '옮겨졌다.' 의 경우
        옮기/VV + 어/EC + 지/VX + 었/EP + 다/EF + ./SF
        로 분리되어 원 단어(옮겨졌다)에서 실제로 보존된 형태소는 '다', '.'만 남게 되므로
        옮기/VV + 어/EC + 지/VX + 었/EP + 다/EF + ./SF
        로 분리하는 대신
        옮겨졌/VV + EC + VX + EP + 다/EF + ./SF
        로 분리합니다.

        이 때 원 단어가 형태소 기본형들의 조합인지 아니면 변형되었는지를 파악하기 위해
        버퍼를 사용했습니다 (snipbuffer, posbuffer)
        이에 따라 각 읽어들일 때의 상황을 4가지로 구분하고
        현재 읽고 있는 위치를 파악하기 위해 wordcount를 도입하고
        문장의 끝인지를 파악하기 위해 end_of_sequence 를 도입했습니다.
        """

        sniparray = []
        posarray = []

        for line in f:
            #print (line)
            #break
            chomped_line = line.rstrip()
            if chomped_line == "<p>":
                pass
                # is_inside = True
                #print ("inside")
            elif chomped_line == "</p>":
                #print()
                # is_inside = False

                for i in range (0, len(sniparray)):
                    print (i+1,"\t", "".join(sniparray[i]),"\t", "+".join(posarray[i]))

                sniparray = []
                posarray = []
            else:
                m1 = re.match('^([^\t]+)\t([^\t]+)\t([^\t]+)$', chomped_line)
                if m1:
                    #print ("linenumber", m1.group(1))
                    #print ("word", m1.group(2))
                    word = m1.group(2)
                    #print ("parsed", m1.group(3))
                    parsed = m1.group(3)
                    snip_pairs = re.split(' \+ ', parsed)  # +sign needs to be escaped in regex #던지/VV + 어/EC

                    # split_word = m1.group(2)
                    snip_pairs_2d = []

                    for snip_pair in snip_pairs:
                        # line_counter += 1
                        # print ("snip_pair = ", snip_pair) #던지/VV
                        m2 = re.match('^([^\/]+)\/([^\/]+)$', snip_pair)
                        if m2:
                            snip = m2.group(1)
                            pos = m2.group(2)
                            #print ("line", line_counter)
                            #print ("snip", snip)
                            #print ("pos", pos)
                            #print (line_counter,"\t",snip,"\t",pos)

                            snip_pairs_2d.append([snip, pos])

                    #print (snip_pairs_2d)
                    #print (word)

                    buffer_start = 0
                    bufer_end = len(snip_pairs_2d)-1
                    snipbuffer = []
                    posbuffer = []

                    word = list(word)
                    #print(word)
                    word_counter = 0

                    end_of_sequence = False
                    buffer = False
                    for snip_pair in snip_pairs_2d:

                        if snip_pairs_2d[-1] == snip_pair:
                            end_of_sequence = True

                        # 4 cases
                            # 1) if snippet is inside the word & no buffer
                            # 2) if snippet is inside the word & there is buffer
                            # 3) if snippet is NOT inside the word & no buffer
                            # 4) if snippet is NOT inside the word & there is buffer

                        # 1) if snippet is inside the word & no buffer
                            # => Print current word
                        if (snip_pair[0] in word[word_counter:]) and (buffer == False):
                            # print(1)
                            sniparray.append([snip_pair[0]])
                            posarray.append([snip_pair[1]])

                            buffer_start += len(snip_pair[0])
                            buffer = False

                            word_counter +=1

                        # 2) if snippet is inside the word & there is buffer
                            # => Print Buffer and Print current word
                        elif (snip_pair[0] in word[word_counter:]) and (buffer == True):
                            # print(2)
                            #print("Where is corresponding word:" word.index(snip_pair[0]))
                            buffer_end = word.index(snip_pair[0])
                            snipbuffer = word[buffer_start:buffer_end]

                            sniparray.append(snipbuffer)
                            posarray.append(posbuffer)

                            buffer_start +=len(snip_pair[0])

                            sniparray.append([snip_pair[0]])
                            posarray.append([snip_pair[1]])

                            buffer = False

                            word_counter +=1

                        # 3) if snippet is NOT inside the word & no buffer
                            # if End of Sequence => Print current word
                            # if not end of sequence => Do Not Print Buffer, Buffer Start
                        elif not (snip_pair[0] in word[word_counter:]) and (buffer == False):

                            if end_of_sequence == True:
                                # print("3-1")
                            # Print Current word(=remaining part in the 'word')
                                snipbuffer = word[buffer_start:]
                                sniparray.append(snipbuffer)

                                posarray.append([snip_pair[1]])

                                word_counter +=1

                            else:
                                # print("3-2")
                            # Buffer Start!
                            # snip buffer will be formed right before when buffer is eliminated
                            # just don't change buffer_start
                                posbuffer=[]
                                posbuffer.append(snip_pair[1])

                                buffer = True

                                word_counter +=1

                        # 4) if snippet is NOT inside the word & there is buffer
                            # if End of Sequence => Print Buffer and print current word
                            # if not end of sequence => Add buffer
                        else:
                            if end_of_sequence == True:
                                # print("4-1")
                            # Print Buffer and print current word
                                # buffer_end = len(word)-1
                                snipbuffer = word[buffer_start:]
                                sniparray.append(snipbuffer)

                                posbuffer.append(snip_pair[1])
                                posarray.append(posbuffer)

                                word_counter +=1
                            else:
                                # print("4-2")
                            # Add buffer
                                posbuffer.append(snip_pair[1])

                                word_counter +=1

                        if end_of_sequence == True:
                            continue

"""
아래 General Function, CoNLL-U Function 은 건드리지 않았습니다.
어떻게 합칠 수 있을까요?
"""

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
