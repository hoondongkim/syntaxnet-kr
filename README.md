# syntaxnet-kr

## 1. Our First Goal.
We will make the Generator Tool for the korean UniversalDependency Files.(<http://universaldependencies.org>)
That UD files will be uesd to train the korean version of Google Syntaxnet.

(<https://github.com/tensorflow/models/tree/master/syntaxnet>)

### 1. Input File Format
; 친구 딸의 결혼식 구경으로 일이 끝난 게 아니라 또 딴 친구 남편의 개인전을 구경하고 나서 다시 딴 친구 딸이 참가하는 음악회 구경을 가야 된다는 약간 문화적인 구경거리가 그날의 스케줄로 우리 앞에 남아 있었다.

* (S 	(NP_SBJ 	(VP_MOD 	(VP_CMP 	(NP_CMP 	(S_MOD 	(NP_AJT 	(NP 	(NP_MOD 	(NP_MOD 친구/NNG)
								* (NP_MOD 딸/NNG + 의/JKG))
							* (NP 결혼식/NNG))
						* (NP_AJT 구경/NNG + 으로/JKB))
					* (S_MOD 	(NP_SBJ 일/NNG + 이/JKS)
						* (VP_MOD 끝나/VV + ᆫ/ETM)))
				* (NP_CMP 것/NNB + 이/JKC))
			* (VP 아니/VCN + 라/EC))
      *	(VP_MOD 	(VP 	(AP 또/MAG)
				* (VP 	(NP_OBJ 	(NP_MOD 	(NP_MOD 	(DP_MOD 딴/MM)
								* (NP_MOD 친구/NNG))
							* (NP_MOD 남편/NNG + 의/JKG))
						* (NP_OBJ 개인전/NNG + 을/JKO))
					* (VP 	(VP 구경/NNG + 하/XSV + 고/EC)
						* (VP 나/VX + 아서/EC))))
			* (VP_MOD 	(AP 다시/MAG)
				* (VP_MOD 	(VP 	(NP_OBJ 	(NP 	(S_MOD 	(NP_SBJ 	(NP 	(DP_MOD 딴/MM)
											* (NP 친구/NNG))
										* (NP_SBJ 딸/NNG + 이/JKS))
									* (VP_MOD 참가/NNG + 하/XSV + 는/ETM))
								* (NP 음악회/NNG))
							* (NP_OBJ 구경/NNG + 을/JKO))
						* (VP 가/VV + 아야/EC))
					* (VP_MOD 되/VV + ᆫ다는/ETM)))))
	* (NP_SBJ 	(VNP_MOD 	(AP 약간/MAG)
			* (VNP_MOD 문화/NNG + 적/XSN + 이/VCP + ᆫ/ETM))
		* (NP_SBJ 구경거리/NNG + 가/JKS)))
* (VP 	(NP_AJT 	(NP_MOD 그날/NNG + 의/JKG)
		* (NP_AJT 스케줄/NNG + 로/JKB))
	* (VP 	(NP_AJT 	(NP 우리/NP)
			* (NP_AJT 앞/NNG + 에/JKB))
		* (VP 	(VP 남/VV + 아/EC)
			* (VP 있/VX + 었/EP + 다/EF + ./SF)))))

### 2. Output File Format (English Example)
  * 1	Bush	Bush	PROPN	NNP	Number=Sing	3	nsubj	_	_
  * 2	also	also	ADV	RB	_	3	advmod	_	_
  * 3	nominated	nominate	VERB	VBD	Mood=Ind|Tense=Past|VerbForm=Fin	0	root	_	_
  * 4	A.	A.	PROPN	NNP	Number=Sing	7	name	_	_
  * 5	Noel	Noel	PROPN	NNP	Number=Sing	7	name	_	_
  * 6	Anketell	Anketell	PROPN	NNP	Number=Sing	7	name	_	_
  * 7	Kramer	Kramer	PROPN	NNP	Number=Sing	3	dobj	_	_
  * 8	for	for	ADP	IN	_	13	case	_	_
  * 9	a	a	DET	DT	Definite=Ind|PronType=Art	13	det	_	_
  * 10	15	15	NUM	CD	NumType=Card	12	nummod	_	SpaceAfter=No
  * 11	-	-	PUNCT	HYPH	_	12	punct	_	SpaceAfter=No
  * 12	year	year	NOUN	NN	Number=Sing	13	compound	_	_
  * 13	term	term	NOUN	NN	Number=Sing	3	nmod	_	_
  * 14	as	as	ADP	IN	_	16	case	_	_
  * 15	associate	associate	ADJ	JJ	Degree=Pos	16	amod	_	_
  * 16	judge	judge	NOUN	NN	Number=Sing	13	nmod	_	_
  * 17	of	of	ADP	IN	_	19	case	_	_
  * 18	the	the	DET	DT	Definite=Def|PronType=Art	19	det	_	_
  * 19	District	District	PROPN	NNP	Number=Sing	16	nmod	_	_
  * 20	of	of	ADP	IN	_	22	case	_	_
  * 21	Columbia	Columbia	PROPN	NNP	Number=Sing	22	compound	_	_
  * 22	Court	Court	PROPN	NNP	Number=Sing	19	nmod	_	_
  * 23	of	of	ADP	IN	_	24	case	_	_
  * 24	Appeals	Appeals	PROPN	NNPS	Number=Plur	22	nmod	_	SpaceAfter=No
  * 25	,	,	PUNCT	,	_	3	punct	_	_
  * 26	replacing	replace	VERB	VBG	VerbForm=Ger	3	advcl	_	_
  * 27	John	John	PROPN	NNP	Number=Sing	29	name	_	_
  * 28	Montague	Montague	PROPN	NNP	Number=Sing	29	name	_	_
  * 29	Steadman	Steadman	PROPN	NNP	Number=Sing	26	dobj	_	SpaceAfter=No
  * 30	.	.	PUNCT	.	_	3	punct	_	_  
