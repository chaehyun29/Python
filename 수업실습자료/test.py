#HWPythonEx03_03_WriteExam02_이채현.py

menuNum=[1,2,3,4,5,9]
menu = ['회원가입','로그인','회원목록','정보수정','회원탈퇴','메뉴종료'] 
itemList = ['ID','PWD','NAME','EMAIL','PHONE','ADDRESS']
userInfo = ['']*len(itemList)
thisUser = '' #현재 로그인 한 유저


def uploadUserFile(): # 기존 유저 파일 불러오기
	with open('MemV01.txt','r') as userFile:
		return userFile.readlines()

def updapteUserFile(userList): # 유저파일 새로 갈기
	with open('MemV01.txt','w') as userFile:
		for i in userList:
			userFile.write(i)


def userDataToStr(userInfo): # 리스트인 유저데이터를 스트링으로
	str = ''
	for i in range(len(userInfo)):
		str += userInfo[i]
		if i+1 != len(userInfo):
			str += ','
		else :
			str += '\n'
	return str
			

def memIns(): #회원가입
	userList = uploadUserFile()
	print("{:^64}".format("Sign Up!"))

	for idx in range(len(itemList)) :
		userInfo[idx] = (input(f"{itemList[idx]:<10}"))
	print(userInfo)
	userList.append(userInfo)

	#유저파일생성

	with open ('MemV01.txt','a') as userFile:
		userFile.write(userDataToStr(userInfo))




def memLog(): #로그인
	userList = uploadUserFile()
	userID = input(f"{'ID':<10}")
	userPW = input(f"{'PW':<10}")

	countset = 1	
	for i in userList:
		if i.split(',')[0].strip() == userID and i.split(',')[1].strip() == userPW :
			print()
			nstr = f"{i.split(',')[0]}님 로그인성공"
			print(f"{nstr:^90}")
			print()
			return True, i.split(',')

		elif i.split(',')[0].strip() == userID and i.split(',')[1].strip() != userPW:
			print()
			print(f"{'패스워드를 확인해주세요':^90}")
			print()
			return False, None

		elif countset == len(userList):
			print()
			print(f"{'로그인 정보를 확인하세요':^90}")
			print()
			return False, None

		countset+=1


def memSel(): #유저리스트 확인
	userList = uploadUserFile()
	print()
	print("{:^105}".format("User List!"))
	print()
	
	#정보
	print(f'\t{"":=^95}')
	print('\t',end="")
	for i in itemList:
		print(f"{i}\t\t",end="")
		if i == 'EMAIL':
			print('\t',end="")
	print()
	print(f'\t{"":=^95}')

	# 유저정보 뿌리기
	for i in userList:
		print('\t',end="")
		singleData = i.split(',')
		for j in singleData:
			print(j.strip(),end='\t\t')
		print()
	print()



def memUpd(): # 회원 정보 수정

	userList = uploadUserFile()

	print("{:^105}".format("Edit!"))
	print()
	print(f"{'수정할 회원 정보를 입력하세요':^90}")
	isLogChk, theUser = memLog()

	if isLogChk:
		print(f'{theUser[0]}님 회원 정보')
		for i in theUser:
			print(i.strip(),end='\t')
		print()

		# 정보 수정
		for i in range(1,len(theUser)):
			print(itemList[i],end='\t')
			if (input('수정 (y/n) :') == 'y'):
				print(itemList[i],end='\t')
				if i == len(theUser):
					theUser[i] = input()+'\n'
				else:
					theUser[i] = input()

		#수정한 싱글 유저 데이터 str형변환 하여 보여주기
		
		for i in range(len(userList)):
			if userList[i].split(',')[0] == theUser[0]:
				userList[i] = userDataToStr(theUser)
		updapteUserFile(userList)
		'''
		strUser = ''
		for i in range(len(theUser)):
			if i == 0:
				strUser +=theUser[i]
			else:
				strUser +=','+theUser[i]
		print(strUser)
		
		#싱글 유저 데이터를 기존 유저 데이터에 추가하여 파일 업로드
		for i in range(len(userList)):
			if userList[i].split(',')[0] == theUser[0]:
				userList[i] = strUser
		updapteUserFile(userList)
		'''
		return theUser


	else:
		return



def memDel(): # 회원 정보 삭제
	print("{:^105}".format("Delete!"))
	print()
	print(f"{'탈퇴할 회원 정보를 입력하세요':^90}")
	isLogChk, logID = memLog()
	if isLogChk:
		print(f'{logID}님 Update Chk!')
		print()
	else:
		return


def uploadMenu(): # 메뉴 띄우기
	print("{:=^100}".format('메뉴선택'))
	print('\t',end="")
	for idx in menu:
		if idx =='메뉴종료':
			print(9,idx,end='\t')
		else:
			print(menu.index(idx)+1,idx,end='\t')
	print()

	print("{:=^104}".format(""))







while True :

	uploadMenu() # 메뉴 띄우기

	num = int(input(f"{'메뉴의 번호를 입력해주세요':>50}"))
	if not(num in menuNum):
		num = 0


	#메뉴 선택
	if num == 1:
		memIns() #회원가입
		
	elif num == 2:		# 로그인
		print("{:^105}".format("Log In!"))
		val, thisUser = memLog()

	elif num == 3:		# 유저 리스트 확인 또는 불러오기
		memSel()

	elif num == 4:		# 정보 수정
		memUpd()

	elif num == 5:		#유저 삭제
		memDel()

	elif num == 9:		#시스템 종료
		print(f"{'시스템을 종료합니다.':^64}")
		break

	else:			#메뉴 번호 out range
		print('메뉴 번호를 확인해주세요')
	print()

