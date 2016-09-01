import re
import codecs
import os
from pythonds.basic.stack import Stack

"""
[1] Main Function
"""
def main():
    directory = os.getcwd() + '/InputDataType2'
    filename = 'BGHO0437.txt'
    filename = os.path.join(directory, filename)

    f = open(filename, 'r', encoding='utf-16')
    is_inside = False
    line_counter = 0
    OUT_FILENAME = "OutputDataType2\kr-ud-dev.conllu"

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
        sniparrayOrigin = []
        posarray = []

        # 괄호 처리 관련 자료구조 init
        stack = Stack()
        stackLevel = [1] # for Call By Reference
        totalCount = [1]
        currentLevel = [1]
        levelCountArray = []
        wordDic = dict()
        numDic = dict()

        split_sentence = ""
        num_word_in_sentence = 0
        which_word_in_sentence =0
        word = ""
        special_characters = "'", "-", '"', "Q"
        special_character = False

        for line in f:
            #print (line)
            #break
            chomped_line = line
            # print(chomped_line)
            if chomped_line[0] ==";" :
                numDic = wordDicToNumDic(wordDic, levelCountArray)
                """
                # For Debug . 이 부분을 풀면 많은 정보를 볼 수 있음.
                print("[Last Result for dubg]")
                print(sniparray)
                print(sniparrayOrigin)
                print(numDic)
                print(wordDic)
              """
                for i in range (0, len(sniparrayOrigin)):
                    print (i+1
                           , "\t", getFormStr("".join(sniparray[i]))
                           , "\t", getLemmaStr(sniparrayOrigin[i][0])
                           , "\t", getUpostagStr("+".join(posarray[i]))
                           , "\t", getXpostagStr("+".join(posarray[i]))
                           , "\t", getFeatsStr("")
                           , "\t" , getHeadStr(numDic[wordDic[sniparrayOrigin[i][0]] - 2])
                           , "\t", getDeprelStr("")
                           , "\t", getDepsStr("")
                           , "\t", getMiscStr(wordDic[sniparrayOrigin[i][0]] - 1)
                           )
                print()

                split_sentence = chomped_line.split(' ')
                # print(split_sentence)
                sniparray = []
                sniparrayOrigin = []
                posarray = []
                which_word_in_sentence =0

                # 괄호 처리 관련 자료구조 reset
                stack = Stack()
                stackLevel[0] = 0
                totalCount[0] = 0
                currentLevel[0] = 0
                levelCountArray = []
                wordDic = dict()
                numDic = dict()


                #any(x in a for x in b)
                if any(x in special_characters for x in chomped_line):
                    special_character = True
                    print(chomped_line.replace("; ", ""))
                    print("This sentence contains special_character")
                else:
                    special_character = False

            elif special_character == True:
                continue


            elif ("(" in chomped_line) and ("\t" in chomped_line):
                m1 = re.match('(.*)(\([A-Z_]+ *\t*)+([^\(\)]+)([\)]+)', chomped_line)

                if m1:
                    #print ("features_of_previous_parsed_words", m1.group(1))
                    #print ("feature_of_current_parsed_word", m1.group(2))
                    #print ("parsed", m1.group(3))
                    parsed = m1.group(3)
                    previousStr = m1.group(1) + m1.group(2)
                    lastStr = m1.group(4)
                    #print ("last_parenthesis", m1.group(4))
                    snip_pairs = re.split(' \+ ', parsed)  # +sign needs to be escaped in regex #던지/VV + 어/EC

                    snip_pairs_2d = []

                    parenthesesChecker(previousStr, stack, stackLevel, totalCount, levelCountArray, wordDic, currentLevel)
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
                            parenthesesChecker(snip_pair, stack, stackLevel, totalCount, levelCountArray, wordDic, currentLevel, m2)
                            snip_pairs_2d.append([snip, pos])
                    parenthesesChecker(lastStr, stack, stackLevel, totalCount, levelCountArray, wordDic, currentLevel)
                    which_word_in_sentence +=1
                    # print(which_word_in_sentence)
                    try:
                        word = split_sentence[which_word_in_sentence]
                    except IndexError:
                        print("Indexerror, pass")

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
                            sniparrayOrigin.append([snip_pair[0]])
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
                            sniparrayOrigin.append([snip_pair[0]])
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
                                sniparrayOrigin.append([snip_pair[0]])

                                posarray.append([snip_pair[1]])

                                word_counter +=1

                            else:
                                # print("3-2")
                            # Buffer Start!
                            # snip buffer will be formed right before when buffer is eliminated
                            # just don't change buffer_start
                                posbuffer=[]
                                posbuffer.append(snip_pair[1])
                                #sniparrayOrigin.append(snip_pair[0])
                                sniparrayOrigin.append([snip_pair[0]])
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
                                #sniparrayOrigin.append(snip_pair[0])

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
[2] 괄호를 Depth & Count 로 변환한 정보를 넘겨 받아, Depth 별 카운트를 누적하여 수치화 한다.
"""
def wordDicToNumDic(wordDic, levelCountArray):
    resultDic = dict()
    sumResult = 0
    for levelIndex in range(0, len(levelCountArray)) :
        if (levelIndex == 0 ):
            resultDic[levelIndex] = levelCountArray[levelIndex]
        else:
            resultDic[levelIndex] = resultDic[levelIndex - 1] + levelCountArray[levelIndex]
    return  resultDic

"""
[3] 괄호를 Stack 에 넣어 Depth 정보와 Depth 별 Count 로 리턴. ( call by reference 로 결과 리턴 )
"""
def parenthesesChecker(lineString, stack, stackLevel , totalCount, levelCountArray, wordDic , currentLevel, m2 = None) :
    localIndex = 0
    while localIndex < len(lineString):
        symbol = lineString[localIndex]
        localIndex += 1
        if symbol != "(" and symbol != ")" and symbol != "/":
            continue
        else:
            if symbol == "/" and m2 != None :
                wordDic[m2.group(1)] = currentLevel[0] # 해당 단어의 current Level을 기억. 갯수는 나중에 알수 있음.
                                                    # 아직은 갯수를 모르므로, 갯수를 leveCountDic 에서 1씩 누적.(아래)
            elif symbol == "/":
                print("[ERR]" + lineString)
                continue
            elif symbol == "(":
                stack.push(symbol)
                if ( currentLevel[0] < len(levelCountArray) ):
                    levelCountArray[currentLevel[0]] += 1
                else:
                    levelCountArray.append(1)
                totalCount[0] += 1
                stackLevel[0] += 1
                currentLevel[0] += 1
            else:
                try: # traing 문서에 Tree 구문에 괄호 갯수가 오류인 데이타가 있음.
                    stack.pop()
                    currentLevel[0] -= 1
                except IndexError:
                    print("parentheses error, pass")

"""
[4] CoNLL-U Format Function
1.ID: Word index, integer starting at 1 for each new sentence; may be a range for tokens with multiple words.
2.FORM: Word form or punctuation symbol.
3.LEMMA: Lemma or stem of word form.
4.UPOSTAG: Universal part-of-speech tag drawn from our revised version of the Google universal POS tags.
5.XPOSTAG: Language-specific part-of-speech tag; underscore if not available.
6.FEATS: List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available.
7.HEAD: Head of the current token, which is either a value of ID or zero (0).
8.DEPREL: Universal Stanford dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one.
9.DEPS: List of secondary dependencies (head-deprel pairs).
10.MISC: Any other annotation. 우리 소스에서는 이곳에 Tree 의 Depth 를 넣어 놓았음.
"""
# 2.FORM - 영어 참고. 형태소 분석 전 원문을 넘김.
def getFormStr(snip):
    return snip

# 3.LEMMA - 영어 참고. 형태소 분석 된 가공된 기본어휘를 넘김.
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

# 7.HEAD : 현재 Tree Depth 를 동일 Depth 의 Count를 고려하여 누적 값을 보여주고 있음.
def getHeadStr(pos):
    return pos

# 8.DEPREL
def getDeprelStr(pos):
    return "_"

# 9.DEPS
def getDepsStr(pos):
    return "_"

# 10.ETC : 현재 Tree depth 를 넘기고 있음.
def getMiscStr(pos):
    return pos

if __name__ == "__main__":
    main()