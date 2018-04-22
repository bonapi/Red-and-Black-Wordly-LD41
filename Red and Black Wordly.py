instructions='''You lose if one player is 4 or more points ahead of another (2 to 6 => OK;  2 to 7 => GAME OVER).
You lose if any player has more than 4 Red and Black tokens together in their hand (3R and 1B => OK;  3R and 2B => GAME OVER).
You lose if words clock runs down to 0. You lose if you make 3 wrong guesses.

If your player doesn`t have exact number of tokens needed by button clicked on that players loses all tokens and gains nothing.
When text prompt appears on screen you have to guess the word from letters on the screen by using 2 less letters than offered.
Every correct guess gives 1 victory point to each player. When you make a guess timer is reset.

Goal of the game is to get both players to 10 victory points, how? press the buttons and you'll find out.

Or if you`re not a fan of trial and error here is a description of how all the buttons work:
Button 1 = lose all cards of your player in exchange for +30 seconds on the clock(cost player1:3R, 1B, player2 1R, 3B).
Button 2 = place red or black token, 3 tokens give victory point to player1(red tokens) or player2(black tokens).
Button 3 = draw one red token. 1/4 chance that player2(black player) gains victory point.
Button 4 = draw one black token. 1/4 chance that player1(red player) gains victory point.
Button 5 = remove one letter from available letters(cost 2R, 2B).
'''
#compiled with python 3.6.4, graphic elements created with built-in python3 library tkinter (not tested with python2)
try:
	# for Python2
	from Tkinter import *
except ImportError:
	# for Python3
	from tkinter import *
try:
	import ttk
	import tkFont as font
except ImportError: # Python 2
	import tkinter.ttk as ttk
	import tkinter.font as font
import winsound
import math
import copy
import random

#dbg_disable = False
dbg_disable = True

if dbg_disable == True:
	print = lambda *s: ''

def playButtonSound(s=''):
	if s=='': winsound.Beep(300, 120)
	elif s=='vp': winsound.Beep(800, 160)
	else: winsound.Beep(300, 120)
def playWinSound():
	d = 270
	for freq in [216, 332, 597, 204, 829, 603, 512, 598, 204, 440, 569, 3000]:
		winsound.Beep(freq, d)
		d+=20
def playDefeatSound():
	d = 290
	for freq in [1100, 1000, 800, 600, 400, 200, 216,  200, 400, 600, 800]:
		winsound.Beep(freq, d)
		d+=30

move = 'p1'
def nextMove():
	global move
	if move == 'p1':
		move = 'p2'
	else: move = 'p1'
	
	if move == 'p1':
		move_stringVar.set('Move: player1')
	else:
		move_stringVar.set('Move: player2')

p1_score = 0
p2_score = 0
def p1_score_token():
	global p1_score
	global p2_score
	global tokens_on_board
	if tokens_on_board[1][0] >= 2:
		p1_score+=1
		tokens_on_board[1][0] = 0
	else: tokens_on_board[1][0]+=1
def p2_score_token():
	global p1_score
	global p2_score
	global tokens_on_board
	if tokens_on_board[1][1] >= 2:
		p2_score+=1
		tokens_on_board[1][1] = 0
	else: tokens_on_board[1][1]+=1
	

'''[[p1, p2], [p1, p2], [p1, p2], [p1, p2], [p1, p2], [p1, p2]]'''
array6 = [[0]*2] * 6
tokens_on_board = []
for i in array6:
	tokens_on_board.append(copy.copy(i))
	
#				p1(R,B), p2(R,B)
tokens_in_hand = [[2,1], [2,1]]
	
tokens_on_board[1][0]=0
tokens_on_board[1][1]=0

active_bg_color = '#96A882'
active_bg_color2 = '#A6A882'

def button1_click():
	global countdown_sec
	global move
	global tokens_in_hand
	playButtonSound()

	if move == 'p1':
		if tokens_in_hand[0][0] == 3 and tokens_in_hand[0][1] == 1:
			countdown_sec += 30
		tokens_in_hand[0][0] = 0
		tokens_in_hand[0][1] = 0
	else:
		if tokens_in_hand[1][0] == 1 and tokens_in_hand[1][1] == 3:
			countdown_sec += 30
		tokens_in_hand[1][0] = 0
		tokens_in_hand[1][1] = 0
	nextMove()
	updateScreen()
	
	button1.config(state="disabled")
	button1.config(bg='grey')
	button2.config(state="normal")
	button2.config(bg=active_bg_color)
	button3.config(state="normal")
	button3.config(bg=active_bg_color)
	button4.config(state="normal")
	button4.config(bg=active_bg_color)
	button5.config(state="normal")
	button5.config(bg=active_bg_color)
	
def button2_click():
	global p1_score
	global p2_score
	global tokens_on_board
	global tokens_in_hand
	global move
	global button2_StringVar
	playButtonSound()
	if Red_Blue_dialog_onClick():
		if move == 'p1':
			if tokens_in_hand[0][0] > 0:
				tokens_in_hand[0][0]-=1
				p1_score_token()
		else:
			if tokens_in_hand[1][0] > 0:
				tokens_in_hand[1][0]-=1
				p1_score_token()
	else:
		if move == 'p1':
			if tokens_in_hand[0][1] > 0:
				tokens_in_hand[0][1]-=1
				p2_score_token()
		else:
			if tokens_in_hand[1][1] > 0:
				tokens_in_hand[1][1]-=1
				p2_score_token()
	p1_score_stringVar.set('player1 victory points:'+str(p1_score))
	p2_score_stringVar.set('player2 victory points:'+str(p2_score))
	print('tokens_on_board:'+str(tokens_on_board)+', p1='+str(p1_score)+', p2='+str(p2_score))
	print('tokens_in_hand:'+str(tokens_in_hand))
	nextMove()
	updateScreen()
	
	if score_not_more_than_four_off(): pass
	else: game_over('score')
	
	button1.config(state="normal")
	button1.config(bg=active_bg_color)
	button2.config(state="disabled")
	button2.config(bg='grey')
	button3.config(state="normal")
	button3.config(bg=active_bg_color)
	button4.config(state="normal")
	button4.config(bg=active_bg_color)
	button5.config(state="normal")
	button5.config(bg=active_bg_color)
	
def button3_click():#draw Red token
	global p1_score
	global p2_score
	global tokens_on_board
	global tokens_in_hand
	global move
	global button2_StringVar
	playButtonSound()
	if move == 'p1': tokens_in_hand[0][0]+=1
	else: tokens_in_hand[1][0]+=1

	if move == 'p1':
		if random.randint(1,4) == 1:
			p2_score+=1
	else:
		if random.randint(1,4) == 1:
			p2_score+=1
			
	p1_score_stringVar.set('player1 victory points:'+str(p1_score))
	p2_score_stringVar.set('player2 victory points:'+str(p2_score))
	
	if number_of_tokens_in_hand_not_exceed():
		nextMove()
		updateScreen()
	else: game_over('tokens')
	
	if score_not_more_than_four_off(): pass
	else: game_over('score')

	button1.config(state="normal")
	button1.config(bg=active_bg_color)
	button2.config(state="normal")
	button2.config(bg=active_bg_color)
	button3.config(state="disabled")
	button3.config(bg='grey')
	button4.config(state="normal")
	button4.config(bg=active_bg_color)
	button5.config(state="normal")
	button5.config(bg=active_bg_color)

def button4_click():#draw Black token
	global p1_score
	global p2_score
	global tokens_on_board
	global tokens_in_hand
	global move
	global button2_StringVar
	playButtonSound()
	if move == 'p1': tokens_in_hand[0][1]+=1
	else: tokens_in_hand[1][1]+=1

	if move == 'p1':
		if random.randint(1,4) == 1:
			playButtonSound('vp')
			p1_score+=1
	else:
		if random.randint(1,4) == 1:
			playButtonSound('vp')
			p1_score+=1
			
	p1_score_stringVar.set('player1 victory points:'+str(p1_score))
	p2_score_stringVar.set('player2 victory points:'+str(p2_score))
	
	if number_of_tokens_in_hand_not_exceed():
		nextMove()
		updateScreen()
	else: game_over('tokens')
	
	if score_not_more_than_four_off(): pass
	else: game_over('score')
		

	button1.config(state="normal")
	button1.config(bg=active_bg_color)
	button2.config(state="normal")
	button2.config(bg=active_bg_color)
	button3.config(state="normal")
	button3.config(bg=active_bg_color)
	button4.config(state="disabled")
	button4.config(bg='grey')
	button5.config(state="normal")
	button5.config(bg=active_bg_color)
	
def button5_click():#-2R, -2B, remove one letter
	global possible_word
	global tokens_in_hand
	global current_word_len
	global current_letters_to_guess
	global given_letters_stringVar
		
	print('current_letters_to_guess:'+current_letters_to_guess)
		
	found_char_to_remove = ''
	if move == 'p1':
		if tokens_in_hand[0][0] == 2 and tokens_in_hand[0][1] == 2:
			for c in current_letters_to_guess:
				if c not in possible_word:
					found_char_to_remove = c
		tokens_in_hand[0][0] = 0
		tokens_in_hand[0][1] = 0
	else:
		if tokens_in_hand[1][0] == 2 and tokens_in_hand[1][1] == 2:
			for c in current_letters_to_guess:
				if c not in possible_word:
					found_char_to_remove = c
		tokens_in_hand[1][0] = 0
		tokens_in_hand[1][1] = 0
	
	if len(current_letters_to_guess)-1 < current_word_len:
		return#removing more letters would make word unguessable
	
	playButtonSound()
	
	if found_char_to_remove == '':
		for c in current_letters_to_guess:
			if current_letters_to_guess.count(c) > 1:#double char
				current_letters_to_guess = current_letters_to_guess.replace(c,'',1)
				break
				
	else:
		print('remove:'+found_char_to_remove+', removing:'+found_char_to_remove)
		current_letters_to_guess = current_letters_to_guess.replace(found_char_to_remove, '')
	
	given_letters_stringVar.set('Letters:'+current_letters_to_guess)
	
	nextMove()
	updateScreen()

	button1.config(state="normal")
	button1.config(bg=active_bg_color)
	button2.config(state="normal")
	button2.config(bg=active_bg_color)
	button3.config(state="normal")
	button3.config(bg=active_bg_color)
	button4.config(state="normal")
	button4.config(bg=active_bg_color)
	button5.config(state="disabled")
	button5.config(bg='grey')
	
def score_not_more_than_one_off():
	global p1_score
	global p2_score
	print('p1_score:'+str(p1_score)+', p2_score:'+str(p2_score)+', abs'+str(abs(p1_score-p2_score)))
	print('score OK?'+str(abs(p1_score-p2_score) < 2))
	if abs(p1_score-p2_score) < 2: return True
	else: False
def score_not_more_than_four_off():
	global p1_score
	global p2_score
	print('p1_score:'+str(p1_score)+', p2_score:'+str(p2_score)+', abs'+str(abs(p1_score-p2_score)))
	print('score OK?'+str(abs(p1_score-p2_score) < 5))
	if abs(p1_score-p2_score) < 5: return True
	else: False
	
def number_of_tokens_in_hand_not_exceed():
	max = 4
	if (tokens_in_hand[0][0] + tokens_in_hand[0][1] <= max) and (tokens_in_hand[1][0] + tokens_in_hand[1][1] <= max): return True
	else: return False
	
def updateScreen():
	global move
	global tokens_on_board
	global tokens_in_hand
	global move_stringVar
	global tokens_in_hand_stringVar
	global p1_score
	global p2_score
	
	if str(move) == 'p1':
		move_stringVar.set('Move: player1')
	else:
		move_stringVar.set('Move: player2')
	button2_StringVar.set('3 tokens\n=\n1 victory\npoint\n\n'+str(tokens_on_board[1][0])+'R:'+str(tokens_on_board[1][1])+'B')
	if move == 'p1':
		tokens_in_hand_stringVar.set('Tokens in hand:'+str(tokens_in_hand[0][0])+'R, '+str(tokens_in_hand[0][1])+'B')
	else: tokens_in_hand_stringVar.set('Tokens in hand:'+str(tokens_in_hand[1][0])+'R, '+str(tokens_in_hand[1][1])+'B')
	
	if p1_score >= 10 and p2_score >= 10:#game won
		playWinSound()
		move_stringVar.set('You win the game!!!')
		win_stringVar = StringVar()
		win_stringVar_label = Label(root, font=MyFont, textvariable=win_stringVar).pack()
		win_stringVar.set('You win the game!!!')
		countdown_sec = 99999
		countdown_stringVar.set('You win the game!!!')
	
class Red_Blue_dialog:

	def __init__(self, parent):
		top = self.top = Toplevel(parent)
		self.myLabel = Label(top, text='Choose Red or Black token to add:')
		self.myLabel.pack()
		#self.myEntryBox = Entry(top)
		#self.myEntryBox.pack()
		#ans = askyesno('Confirm', 'Press Yes / No')#from tkinter.messagebox import askyesno
		self.mySubmitButton = Button(top, text=' Red ', bg='red', width=12, height=12, command=lambda: self.send('Red'))
		self.mySubmitButton.pack(side="left")
		self.mySubmitButton2 = Button(top, text='Black', bg='black', fg='blue', width=12, height=12, command=lambda: self.send('Black'))
		self.mySubmitButton2.pack(side="left")

	def send(self, a=''):
		if a=='Red': self.username = '1'
		else: self.username = '0'
		#self.username = self.myEntryBox.get()
		self.top.destroy()

def Red_Blue_dialog_onClick():
	global p1_score
	global p2_score
	
	global frame
	frame.pack_forget()#disable rest of the screen buttons so that user can't call this function again before closing smaller window
	
	inputDialog = Red_Blue_dialog(root)
	root.wait_window(inputDialog.top)
	
	frame.pack()#enable
	
	print('Red_Blue_dialog: ', inputDialog.username=='1')
	p1_score_stringVar.set('player1 victory points:'+str(p1_score))
	p2_score_stringVar.set('player2 victory points:'+str(p2_score))
	
	return inputDialog.username=='1'

'''
-----------------------------------------
'''


# define root window
root = Tk()
root.title("Red and Black Wordly")
root.minsize(900,680);
root.configure(bg='white')

smallFont = font.Font(size=19, underline=True)
MyFont = font.Font(size=26)
#helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)
butn_size = 7

frame = Frame(root, bg='teal', relief=RIDGE, borderwidth=5, width=400, height=400)
#frame.bind("<KeyPress>", keydown)
frame.focus_set()
frame.pack(fill='x')

p1_score_stringVar = StringVar()
p1_score_stringVar_label = Label(root, font=smallFont, fg='green', textvariable=p1_score_stringVar).pack()
p1_score_stringVar.set('player1 victory points:'+str(p1_score))

p2_score_stringVar = StringVar()
p2_score_stringVar_label = Label(root, font=smallFont, fg='green', textvariable=p2_score_stringVar).pack()
p2_score_stringVar.set('player2 victory points:'+str(p2_score))


move_stringVar = StringVar()
move_stringVar_label = Label(root, font=smallFont, fg='magenta', textvariable=move_stringVar).pack()
if str(move) == 'p1': move_stringVar.set('move:'+' player2')
else: move_stringVar.set('move:'+' player2')

tokens_in_hand_stringVar = StringVar()
tokens_in_hand_stringVar_label = Label(root, font=smallFont, fg='purple', textvariable=tokens_in_hand_stringVar).pack()
tokens_in_hand_stringVar.set('Tokens in hand:'+str(tokens_in_hand[1][0])+'R, '+str(tokens_in_hand[1][1])+'B')


button1_StringVar = StringVar()
button1_StringVar.set('+30sec\n\nplayer1:\n-3R, -1B\n\nplayer2:\n-1R, -3B')
button1 = Button(frame, textvariable=button1_StringVar, relief=RAISED, borderwidth=6, font=MyFont, height=butn_size, width=butn_size, command=button1_click)
button1.pack(side='left', padx=10)

button2_StringVar = StringVar()
button2_StringVar.set('3 tokens\n=\n1 victory\npoint\n\n'+str(tokens_on_board[1][0])+'R:'+str(tokens_on_board[1][1])+'B')
button2 = Button(frame, textvariable=button2_StringVar, relief=RAISED, borderwidth=6, font=MyFont, height=butn_size, width=butn_size, command=button2_click)
button2.pack(side='left', padx=10)

button3_StringVar = StringVar()
button3_StringVar.set('+1R\n\n25%\nchance\nplayer2\ngains\nVP')
button3 = Button(frame, textvariable=button3_StringVar, relief=RAISED, borderwidth=6, font=MyFont, height=butn_size, width=butn_size, command=button3_click)
button3.pack(side='left', padx=10)

button4_StringVar = StringVar()
button4_StringVar.set('+1B\n\n25%\nchance\nplayer1\ngains\nVP')
button4 = Button(frame, textvariable=button4_StringVar, relief=RAISED, borderwidth=6, font=MyFont, height=butn_size, width=butn_size, command=button4_click)
button4.pack(side='left', padx=10)

button5_StringVar = StringVar()
button5_StringVar.set('-2R, -2B\n\nremove\none\nletter')
button5 = Button(frame, textvariable=button5_StringVar, relief=RAISED, borderwidth=6, font=MyFont, height=butn_size, width=butn_size, command=button5_click)
button5.pack(side='left', padx=10)

frame_words_guess = Frame(root, bg='grey', width=400, height=300)

possible_word = ''
def game_over(reason = ''):
	global game_over_flag
	global possible_word
	global countdown_sec
	global tokens_in_hand
	global p1_score
	global p2_score
	global frame
	global current_word_len
	playDefeatSound()
	game_over_flag = True
	print('game over')
	if reason == 'tokens':
		tokens_in_hand_stringVar.set('Too many tokens in hand(4 max): player1='+str(tokens_in_hand[0][0])+'R, '+str(tokens_in_hand[0][1])+'B;  player2='+str(tokens_in_hand[1][0])+'R, '+str(tokens_in_hand[1][1])+'B')
	
	if reason == 'score':
		p1_score_stringVar.set('Scores musn\'t be more than one point different'+' player1:'+str(p1_score))
		p2_score_stringVar.set('Scores musn\'t be more than one point different'+' player2:'+str(p2_score))
		
	frame.pack_forget()
	gameOver_stringVar = StringVar()
	gameOver_stringVar_label = Label(root, font=MyFont, textvariable=gameOver_stringVar).pack()
	gameOver_stringVar.set('Game Over (Press F1 for help)')
	countdown_sec = 99999
	countdown_stringVar.set('One possible word was:'+possible_word)

def refresh():
	print('refresh')
	root.after(2000, refresh)
	
game_over_flag = False
countdown_sec = 60
def countdown():
	global countdown_sec
	global countdown_stringVar
	global game_over_flag
	if game_over_flag: return
	print('countdown:'+str(countdown_sec))
	if countdown_sec <= 0:
		game_over_flag = True
		game_over()
	else:
		countdown_sec -= 1
		countdown_stringVar.set(str(countdown_sec)+' seconds remaining')
		root.after(1000, countdown)
		#frame_words_guess.update_idletasks()
	

#words taken from: http://www.thefreedictionary.com
w3 = ['abs', 'ace', 'act', 'add', 'aft', 'age', 'ago', 'aid', 'aim', 'air', 'ale', 'all', 'and', 'ant', 'any', 'ape', 'app', 'apt', 'arc', 'are', 'ark', 'arm', 'art', 'ash', 'ask', 'asp', 'ass', 'ate', 'ave', 'awe', 'axe', 'aye', 'bad', 'bag', 'ban', 'bar', 'bat','bay', 'bed', 'bee', 'beg', 'bel', 'ben', 'bet', 'bid', 'big', 'bin', 'bio', 'bis', 'bit', 'biz', 'bob', 'bog', 'boo', 'bow', 'box', 'boy', 'bra', 'bud', 'bug', 'bum', 'bun', 'bus', 'but', 'buy', 'bye', 'cab', 'cad', 'cam', 'can', 'cap', 'car', 'cat', 'chi', 'cob', 'cod', 'col', 'con', 'coo', 'cop', 'cor', 'cos', 'cot', 'cow', 'cox', 'coy', 'cry', 'cub', 'cue', 'cup', 'cut', 'dab', 'dad', 'dal', 'dam', 'dan', 'day', 'Dee', 'def', 'del', 'den', 'dew', 'did', 'die', 'dig', 'dim', 'din', 'dip', 'dis', 'doc', 'doe', 'dog', 'don', 'dot', 'dry', 'dub','due', 'dug', 'dun', 'duo', 'dye', 'ear', 'eat', 'ebb', 'ecu', 'eft', 'egg', 'ego', 'elf', 'elm', 'emu', 'end', 'era', 'eta', 'eve', 'eye', 'fab', 'fad', 'fan', 'far', 'fat', 'fax', 'fay', 'fed', 'fee', 'fen', 'few', 'fig', 'fin', 'fir', 'fit', 'fix', 'flu', 'fly', 'foe', 'fog', 'for', 'fox', 'fry', 'fun', 'fur', 'gag', 'gal', 'gap', 'gas', 'gay', 'gee', 'gel', 'gem', 'get', 'gig', 'gin', 'god', 'got', 'gum', 'gun', 'gut', 'guy', 'gym', 'had', 'ham', 'has', 'hat', 'hay', 'hem', 'hen', 'her', 'hey', 'hid', 'him', 'hip', 'his', 'hit', 'hog', 'hon', 'hop','hot', 'how', 'hub', 'hue', 'hug', 'huh', 'hum', 'hut', 'ice', 'icy', 'igg', 'ill', 'imp', 'ink', 'inn', 'ion', 'its', 'ivy', 'jam', 'jar', 'jaw', 'jay', 'jet', 'jew', 'job', 'joe', 'jog', 'joy', 'jug', 'jun', 'kay', 'ken', 'key', 'kid', 'kin', 'kit', 'lab', 'lac', 'lad', 'lag', 'lam', 'lap', 'law', 'lax', 'lay', 'lea', 'led', 'Lee', 'leg', 'les', 'let', 'lib', 'lid', 'lie', 'lip', 'lit', 'log', 'lot', 'low', 'mac', 'mad', 'mag', 'man', 'map', 'mar', 'mas', 'mat', 'max', 'may', 'med', 'meg', 'men', 'Met', 'mid', 'mil', 'mix', 'mob', 'mod', 'mol', 'mom','mon', 'mop', 'mot', 'mud', 'mug', 'mum', 'nab', 'nah', 'nan', 'nap', 'nay', 'neb', 'neg', 'net', 'new', 'nil', 'nip', 'nod', 'nor', 'nos', 'not', 'now', 'nun', 'nut', 'oak', 'odd', 'off', 'oft', 'oil', 'old', 'ole', 'one', 'ooh', 'opt', 'orb', 'ore', 'our', 'out', 'owe', 'owl', 'own', 'pac', 'pad', 'pal', 'pam', 'pan', 'pap', 'par', 'pas', 'pat', 'paw', 'pay', 'pea', 'peg', 'pen', 'pep', 'per', 'pet', 'pew', 'phi', 'pic', 'pie', 'pig', 'pin', 'pip', 'pit', 'ply', 'pod', 'pol', 'pop', 'pot', 'pro', 'psi', 'pub', 'pup', 'put', 'rad', 'rag', 'raj', 'ram','ran', 'rap', 'rat', 'raw', 'ray', 'red', 'ref', 'reg', 'rem', 'rep', 'rev', 'rib', 'rid', 'rig', 'rim', 'rip', 'rob', 'rod', 'roe', 'rot', 'row', 'rub', 'rue', 'rug', 'rum', 'run', 'rye', 'sab', 'sac', 'sad', 'sae', 'sag', 'sal', 'sap', 'sat', 'saw', 'say', 'sea', 'sec', 'see', 'sen', 'set', 'sew', 'sex', 'she', 'shy', 'sic', 'sim', 'sin', 'sip', 'sir', 'sis', 'sit', 'six', 'ski', 'sky', 'sly', 'sod', 'sol', 'son', 'sow', 'soy', 'spa', 'spy', 'sub', 'sue', 'sum', 'sun', 'sup', 'tab', 'tad', 'tag', 'tam', 'tan', 'tap', 'tar', 'tat', 'tax', 'tea', 'ted','tee', 'ten', 'the', 'thy', 'tie', 'tin', 'tip', 'tod', 'toe', 'tom', 'ton', 'too', 'top', 'tor', 'tot', 'tow', 'toy', 'try', 'tub', 'tug', 'two', 'use', 'van', 'vat', 'vet', 'via', 'wan', 'war', 'was', 'wax', 'way', 'web', 'wed', 'wee', 'wet', 'who', 'why', 'wig', 'win', 'wit', 'won', 'yep', 'yes', 'yet', 'you', 'zip', 'zoo']
w3_extra = ['aba', 'aha', 'ado', 'ana', 'alt', 'amp', 'baa', 'cum', 'vie', 'vow', 'woo', 'wow', 'wry', 'wye', 'yen', 'wis']
w4 = ['mark', 'pose', 'verb', 'sing', 'noun', 'tail', 'tire', 'sail', 'lone', 'loud', 'cent', 'noon', 'atom', 'corn', 'poem', 'tube', 'swim', 'shoe', 'rope', 'duck', 'able', 'acid', 'aged', 'also', 'area', 'army', 'away', 'baby', 'back', 'ball', 'band', 'bank', 'base', 'bath', 'bear', 'beat', 'been', 'beer', 'bell', 'belt', 'best', 'bill', 'bird', 'blow', 'blue', 'boat', 'body', 'bomb', 'bond', 'bone', 'book', 'boom', 'born', 'boss', 'both', 'bowl', 'bulk', 'burn', 'bush', 'busy', 'call', 'calm', 'came', 'camp', 'card', 'care', 'case', 'cash', 'cast', 'cell', 'chat', 'chip', 'city', 'club', 'coal', 'coat', 'code', 'cold', 'come', 'cook', 'cool', 'cope', 'copy', 'CORE', 'cost', 'crew', 'crop', 'dark', 'data', 'date', 'dawn', 'days', 'dead', 'deal', 'dean', 'dear', 'debt', 'deep', 'deny', 'desk', 'dial', 'dick', 'diet', 'disc', 'disk', 'does', 'done', 'door', 'dose', 'down', 'draw', 'drew', 'drop', 'drug', 'dual', 'duke', 'dust', 'duty', 'each', 'earn', 'ease', 'east', 'easy', 'edge', 'else', 'even', 'ever', 'evil', 'exit', 'face', 'fact', 'fail', 'fair', 'fall', 'farm', 'fast', 'fate', 'fear', 'feed', 'feel', 'feet', 'fell', 'felt', 'file', 'fill', 'film', 'find', 'fine', 'fire', 'firm', 'fish', 'five', 'flat', 'flow', 'food', 'foot', 'ford', 'form', 'fort', 'four', 'free', 'from', 'fuel', 'full', 'fund', 'gain', 'game', 'gate', 'gave', 'gear', 'gene', 'gift', 'girl', 'give', 'glad', 'goal', 'goes', 'gold', 'Golf', 'gone', 'good', 'gray', 'grew', 'grey', 'grow', 'gulf', 'hair', 'half', 'hall', 'hand', 'hang', 'hard', 'harm', 'hate', 'have', 'head', 'hear', 'heat', 'held', 'hell', 'help', 'here', 'hero', 'high', 'hill', 'hire', 'hold', 'hole', 'holy', 'home', 'hope', 'host', 'hour', 'huge', 'hung', 'hunt', 'hurt', 'idea', 'inch', 'into', 'iron', 'item', 'jack', 'jane', 'jean', 'john', 'join', 'jump', 'jury', 'just', 'keen', 'keep', 'kent', 'kept', 'kick', 'kill', 'kind', 'king', 'knee', 'knew', 'know', 'lack', 'lady', 'laid', 'lake', 'land', 'lane', 'last', 'late', 'lead', 'left', 'less', 'life', 'lift', 'like', 'line', 'link', 'list', 'live', 'load', 'loan', 'lock', 'logo', 'long', 'look', 'lord', 'lose', 'loss', 'lost', 'love', 'luck', 'made', 'mail', 'main', 'make', 'male', 'many', 'mass', 'meal', 'mean', 'meat', 'meet', 'menu', 'mere', 'mike', 'mile', 'milk', 'mill', 'mind', 'mine', 'miss', 'mode', 'mood', 'moon', 'more', 'most', 'move', 'much', 'must', 'name', 'navy', 'near', 'neck', 'need', 'news', 'next', 'nice', 'nick', 'nine', 'none', 'nose', 'note', 'okay', 'once', 'only', 'onto', 'open', 'oral', 'over', 'pace', 'pack', 'page', 'paid', 'pain', 'pair', 'palm', 'park', 'part', 'pass', 'past', 'path', 'peak', 'pick', 'pink', 'pipe', 'plan', 'play', 'plot', 'plug', 'plus', 'poll', 'pool', 'poor', 'port', 'post', 'pull', 'pure', 'push', 'race', 'rail', 'rain', 'rank', 'rare', 'rate', 'read', 'real', 'rear', 'rely', 'rent', 'rest', 'rice', 'rich', 'ride', 'ring', 'rise', 'risk', 'road', 'rock', 'role', 'roll', 'roof', 'room', 'root', 'rose', 'rule', 'rush', 'ruth', 'safe', 'said', 'sake', 'sale', 'salt', 'same', 'sand', 'save', 'seat', 'seed', 'seek', 'seem', 'seen', 'self', 'sell', 'send', 'sent', 'sept', 'ship', 'shop', 'shot', 'show', 'shut', 'sick', 'side', 'sign', 'site', 'size', 'skin', 'slip', 'slow', 'snow', 'soft', 'soil', 'sold', 'sole', 'some', 'song', 'soon', 'sort', 'soul', 'spot', 'star', 'stay', 'step', 'stop', 'such', 'suit', 'sure', 'take', 'tale', 'talk', 'tall', 'tank', 'tape', 'task', 'team', 'tech', 'tell', 'tend', 'term', 'test', 'text', 'than', 'that', 'them', 'then', 'they', 'thin', 'this', 'thus', 'till', 'time', 'tiny', 'told', 'toll', 'tone', 'tony', 'took', 'tool', 'tour', 'town', 'tree', 'trip', 'true', 'tune', 'turn', 'twin', 'type', 'unit', 'upon', 'used', 'user', 'vary', 'vast', 'very', 'vice', 'view', 'vote', 'wage', 'wait', 'wake', 'walk', 'wall', 'want', 'ward', 'warm', 'wash', 'wave', 'ways', 'weak', 'wear', 'week', 'well', 'went', 'were', 'west', 'what', 'when', 'whom', 'wide', 'wife', 'wild', 'will', 'wind', 'wine', 'wing', 'wire', 'wise', 'wish', 'with', 'wood', 'word', 'wore', 'work', 'yard', 'yeah', 'year', 'your', 'zero', 'zone']
w5 = ['spell', 'color', 'heard', 'vowel', 'stead', 'organ', 'cloud', 'climb', 'shout', 'hurry', 'quart', 'shine', 'smell', 'shore', 'favor', 'chord', 'slave', 'chick', 'reply', 'about', 'above', 'abuse', 'actor', 'acute', 'admit', 'adopt', 'adult', 'after', 'again', 'agent', 'agree', 'ahead', 'alarm', 'album', 'alert', 'alike', 'alive', 'allow', 'alone', 'along', 'alter', 'among', 'anger', 'Angle', 'angry', 'apart', 'apple', 'apply', 'arena', 'argue', 'arise', 'array', 'aside', 'asset','audio', 'audit', 'avoid', 'award', 'aware', 'badly', 'baker', 'bases', 'basic', 'basis', 'beach', 'began', 'begin', 'begun', 'being', 'below', 'bench', 'billy', 'birth', 'black', 'blame', 'blind', 'block', 'blood', 'board', 'boost', 'booth', 'bound', 'brain', 'brand', 'bread', 'break', 'breed', 'brief', 'bring', 'broad', 'broke', 'brown', 'build', 'built', 'buyer', 'cable', 'calif', 'carry', 'catch', 'cause', 'chain', 'chair', 'chart', 'chase', 'cheap', 'check', 'chest', 'chief', 'child', 'china', 'chose', 'civil', 'claim', 'class', 'clean', 'clear', 'click', 'clock', 'close', 'coach', 'coast', 'could', 'count', 'court', 'cover', 'craft', 'crash', 'cream', 'crime', 'cross', 'crowd', 'crown', 'curve', 'cycle','daily', 'dance', 'dated', 'dealt', 'death', 'debut', 'delay', 'depth', 'doing', 'doubt', 'dozen', 'draft', 'drama', 'drawn', 'dream', 'dress', 'drill', 'drink', 'drive', 'drove', 'dying', 'eager', 'early', 'earth', 'eight', 'elite', 'empty', 'enemy', 'enjoy', 'enter', 'entry', 'equal', 'error', 'event', 'every', 'exact', 'exist', 'extra', 'faith', 'false', 'fault', 'fiber', 'field', 'fifth', 'fifty', 'fight', 'final', 'first', 'fixed', 'flash', 'fleet', 'floor', 'fluid', 'focus', 'force', 'forth', 'forty', 'forum', 'found', 'frame', 'frank', 'fraud', 'fresh', 'front', 'fruit', 'fully', 'funny', 'giant', 'given', 'glass', 'globe', 'going', 'grace', 'grade', 'grand', 'grant', 'grass', 'great', 'green', 'gross','group', 'grown', 'guard', 'guess', 'guest', 'guide', 'happy', 'harry', 'heart', 'heavy', 'hence', 'henry', 'horse', 'hotel', 'house', 'human', 'ideal', 'image', 'index', 'inner', 'input', 'issue', 'japan', 'jimmy', 'joint', 'jones', 'judge', 'known', 'label', 'large', 'laser', 'later', 'laugh', 'layer', 'learn', 'lease', 'least', 'leave', 'legal', 'level', 'lewis', 'light', 'limit', 'links', 'lives', 'local', 'logic', 'loose', 'lower', 'lucky', 'lunch', 'lying', 'magic', 'major', 'maker', 'march', 'maria', 'match', 'maybe', 'mayor', 'meant', 'media', 'metal', 'might', 'minor', 'minus', 'mixed', 'model', 'money', 'month', 'moral', 'motor', 'mount', 'mouse', 'mouth', 'movie', 'music', 'needs', 'never', 'newly','night', 'noise', 'north', 'noted', 'novel', 'nurse', 'occur', 'ocean', 'offer', 'often', 'order', 'other', 'ought', 'paint', 'panel', 'paper', 'party', 'peace', 'peter', 'phase', 'phone', 'photo', 'piece', 'pilot', 'pitch', 'place', 'plain', 'plane', 'plant', 'plate', 'point', 'pound', 'power', 'press', 'price', 'pride', 'prime', 'print', 'prior', 'prize', 'proof', 'proud', 'prove', 'queen', 'quick', 'quiet', 'quite', 'radio', 'raise', 'range', 'rapid', 'ratio', 'reach', 'ready', 'refer', 'right', 'rival', 'river', 'robin', 'roger', 'roman', 'rough', 'round', 'route', 'royal', 'rural', 'scale', 'scene', 'scope', 'score', 'sense', 'serve', 'seven', 'shall', 'shape', 'share', 'sharp', 'sheet', 'shelf', 'shell','shift', 'shirt', 'shock', 'shoot', 'short', 'shown', 'sight', 'since', 'sixth', 'sixty', 'sized', 'skill', 'sleep', 'slide', 'small', 'smart', 'smile', 'smith', 'smoke', 'solid', 'solve', 'sorry', 'sound', 'south', 'space', 'spare', 'speak', 'speed', 'spend', 'spent', 'split', 'spoke', 'sport', 'staff', 'stage', 'stake', 'stand', 'start', 'state', 'steam', 'steel', 'stick', 'still', 'stock', 'stone', 'stood', 'store', 'storm', 'story', 'strip', 'stuck', 'study', 'stuff', 'style', 'sugar', 'suite', 'super', 'sweet', 'table', 'taken', 'taste', 'taxes', 'teach', 'teeth', 'terry', 'texas', 'thank', 'theft', 'their', 'theme', 'there', 'these', 'thick', 'thing', 'think', 'third', 'those', 'three', 'threw', 'throw','tight', 'times', 'tired', 'title', 'today', 'topic', 'total', 'touch', 'tough', 'tower', 'track', 'trade', 'train', 'treat', 'trend', 'trial', 'tried', 'tries', 'truck', 'truly', 'trust', 'truth', 'twice', 'under', 'undue', 'union', 'unity', 'until', 'upper', 'upset', 'urban', 'usage', 'usual', 'valid', 'value', 'video', 'virus', 'visit', 'vital', 'voice', 'waste', 'watch', 'water', 'wheel', 'where', 'which', 'while', 'white', 'whole', 'whose', 'woman', 'women', 'world', 'worry', 'worse', 'worst', 'worth', 'would', 'wound', 'write', 'wrong', 'wrote', 'yield', 'young', 'youth']
w6 = ['govern', 'equate', 'divide', 'flower', 'clothe', 'excite', 'crease', 'melody', 'gentle', 'locate', 'insect', 'colony', 'invent', 'cotton', 'plural', 'oxygen', 'magnet', 'suffix', 'abroad', 'accept', 'access', 'across', 'acting', 'action', 'active', 'actual', 'advice', 'advise', 'affect', 'afford', 'afraid', 'agency', 'agenda', 'almost', 'always', 'amount', 'animal', 'annual', 'answer', 'anyone', 'anyway', 'appeal', 'appear', 'around', 'arrive', 'artist', 'aspect', 'assess', 'assist', 'assume', 'attack', 'attend', 'august', 'author', 'avenue', 'backed', 'barely', 'battle', 'beauty', 'became', 'become', 'before', 'behalf', 'behind', 'belief', 'belong', 'berlin', 'better', 'beyond', 'bishop', 'border', 'bottle', 'bottom', 'bought', 'branch', 'breath', 'bridge', 'bright', 'broken', 'budget', 'burden', 'bureau', 'button', 'camera', 'cancer', 'cannot', 'carbon', 'career', 'castle', 'casual', 'caught', 'center', 'centre', 'chance', 'change', 'charge', 'choice', 'choose', 'chosen', 'church', 'circle', 'client', 'closed', 'closer', 'coffee', 'column', 'combat', 'coming', 'common', 'comply', 'copper', 'corner', 'costly', 'county', 'couple', 'course', 'covers', 'create', 'credit', 'crisis', 'custom', 'damage', 'danger', 'dealer', 'debate', 'decade', 'decide', 'defeat', 'defend', 'define', 'degree', 'demand', 'depend', 'deputy', 'desert', 'design', 'desire', 'detail', 'detect', 'device', 'differ', 'dinner', 'direct', 'doctor', 'dollar', 'domain', 'double', 'driven', 'driver', 'during', 'easily', 'eating', 'editor', 'effect', 'effort', 'eighth', 'either', 'eleven', 'emerge', 'empire', 'employ', 'enable', 'ending', 'energy', 'engage', 'engine', 'enough', 'ensure', 'entire', 'entity', 'equity', 'escape', 'estate', 'ethnic', 'exceed', 'except', 'excess', 'expand', 'expect', 'expert', 'export', 'extend', 'extent', 'fabric', 'facing', 'factor', 'failed', 'fairly', 'fallen', 'family', 'famous', 'father', 'fellow', 'female', 'figure', 'filing', 'finger', 'finish', 'fiscal', 'flight', 'flying', 'follow', 'forced', 'forest', 'forget', 'formal', 'format', 'former', 'foster', 'fought', 'fourth', 'french', 'friend', 'future', 'garden', 'gather', 'gender', 'german', 'global', 'golden', 'ground', 'growth', 'guilty', 'handed', 'handle', 'happen', 'hardly', 'headed', 'health', 'height', 'hidden', 'holder', 'honest', 'impact', 'import', 'income', 'indeed', 'injury', 'inside', 'intend', 'intent', 'invest', 'island', 'itself', 'jersey', 'joseph', 'junior', 'killed', 'labour', 'latest', 'latter', 'launch', 'lawyer', 'leader', 'league', 'leaves', 'legacy', 'length', 'lesson', 'letter', 'lights', 'likely', 'linked', 'liquid', 'listen', 'little', 'living', 'losing', 'lucent', 'luxury', 'mainly', 'making', 'manage', 'manner', 'manual', 'margin', 'marine', 'marked', 'market', 'martin', 'master', 'matter', 'mature', 'medium', 'member', 'memory', 'mental', 'merely', 'merger', 'method', 'middle', 'miller', 'mining', 'minute', 'mirror', 'mobile', 'modern', 'modest', 'module', 'moment', 'morris', 'mostly', 'mother', 'motion', 'moving', 'murder', 'museum', 'mutual', 'myself', 'narrow', 'nation', 'native', 'nature', 'nearby', 'nearly', 'nights', 'nobody', 'normal', 'notice', 'notion', 'number', 'object', 'obtain', 'office', 'offset', 'online', 'option', 'orange', 'origin', 'output', 'oxford', 'packed', 'palace', 'parent', 'partly', 'patent', 'people', 'period', 'permit', 'person', 'phrase', 'picked', 'planet', 'player', 'please', 'plenty', 'pocket', 'police', 'policy', 'prefer', 'pretty', 'prince', 'prison', 'profit', 'proper', 'proven', 'public', 'pursue', 'raised', 'random', 'rarely', 'rather', 'rating', 'reader', 'really', 'reason', 'recall', 'recent', 'record', 'reduce', 'reform', 'regard', 'regime', 'region', 'relate', 'relief', 'remain', 'remote', 'remove', 'repair', 'repeat', 'replay', 'report', 'rescue', 'resort', 'result', 'retail', 'retain', 'return', 'reveal', 'review', 'reward', 'riding', 'rising', 'robust', 'ruling', 'safety', 'salary', 'sample', 'saving', 'saying', 'scheme', 'school', 'screen', 'search', 'season', 'second', 'secret', 'sector', 'secure', 'seeing', 'select', 'seller', 'senior', 'series', 'server', 'settle', 'severe', 'sexual', 'should', 'signal', 'signed', 'silent', 'silver', 'simple', 'simply', 'single', 'sister', 'slight', 'smooth', 'social', 'solely', 'sought', 'source', 'soviet', 'speech', 'spirit', 'spoken', 'spread', 'spring', 'square', 'stable', 'status', 'steady', 'stolen', 'strain', 'stream', 'street', 'stress', 'strict', 'strike', 'string', 'strong', 'struck', 'studio', 'submit', 'sudden', 'suffer', 'summer', 'summit', 'supply', 'surely', 'survey', 'switch', 'symbol', 'system', 'taking', 'talent', 'target', 'taught', 'tenant', 'tender', 'tennis', 'thanks', 'theory', 'thirty', 'though', 'threat', 'thrown', 'ticket', 'timely', 'timing', 'tissue', 'toward', 'travel', 'treaty', 'trying', 'twelve', 'twenty', 'unable', 'unique', 'united', 'unless', 'unlike', 'update', 'useful', 'valley', 'varied', 'vendor', 'versus', 'victim', 'vision', 'visual', 'volume', 'walker', 'wealth', 'weekly', 'weight', 'wholly', 'window', 'winner', 'winter', 'within', 'wonder', 'worker', 'wright', 'writer', 'yellow']
	
word_guess_so_far = ''
current_letters_to_guess = 'abcde'
current_word_len = 3
failed_guesses = 0
def keydown(e):
	global game_over_flag
	global possible_word
	global word_guess_so_far
	global current_word_len
	global failed_guesses
	global word_stringVar
	global countdown_sec
	global current_letters_to_guess
	global p1_score
	global p2_score
	global w3
	global w3_extra
	global w4
	global w5
	global w6
	
	if str(e.keysym) == 'F1' or str(e.keycode) == str(112):
		if len(str(p1_score_stringVar.get())) > 70:
			p1_score_stringVar.set('player1 victory points:'+str(p1_score))
		else:
			p1_score_stringVar.set(instructions)
		
	if str(e.char) not in 'abcdefghijklmnopqrstuvwxyz':
		return#enter, backspace, space, etc
	
	if game_over_flag: return
		
	print(e.char+' pressed')
	word_guess_so_far += str(e.char)
	
	guessed_word_correctly = False
	
	#last letter guessed
	if len(word_guess_so_far) >= current_word_len:
		
		guessed_word_correctly = True
		
		#if word in dictionary and uses available letters
		if current_word_len == 3:
			if word_guess_so_far in w3 or word_guess_so_far in w3_extra:
				for c in word_guess_so_far:
					if c not in current_letters_to_guess:
						guessed_word_correctly = False
			else: guessed_word_correctly = False
		if current_word_len == 4:
			if word_guess_so_far in w4:
				for c in word_guess_so_far:
					if c not in current_letters_to_guess:
						guessed_word_correctly = False
			else: guessed_word_correctly = False
		if current_word_len == 5:
			if word_guess_so_far in w5:
				for c in word_guess_so_far:
					if c not in current_letters_to_guess:
						guessed_word_correctly = False
			else: guessed_word_correctly = False
		if current_word_len == 6:
			if word_guess_so_far in w6:
				for c in word_guess_so_far:
					if c not in current_letters_to_guess:
						guessed_word_correctly = False
			else: guessed_word_correctly = False
		
		
		word_guess_so_far = ''
		added_time = 30 + (current_word_len*10)
		
		
		#guessed_word_correctly = True#temp cheat
		if guessed_word_correctly == False:
			failed_guesses += 1
			if failed_guesses >= 3: game_over()
			word_stringVar.set(str('_ '*current_word_len) + ': incorrect word' + '(' + str(failed_guesses) + '/3)')
			
		else:
			p1_score += 1
			p2_score += 1
			p1_score_stringVar.set('player1 victory points:'+str(p1_score))
			p2_score_stringVar.set('player2 victory points:'+str(p2_score))
			playButtonSound('vp')
			playButtonSound('vp')
			#new word length = current_word_len+1
			current_word_len += 1
			if current_word_len > 6:
				current_word_len = 3
				
			#get new word
			if current_word_len == 3:
				current_letters_to_guess = copy.copy(getNewWord(w3))
			if current_word_len == 4:
				current_letters_to_guess = copy.copy(getNewWord(w4))
			if current_word_len == 5:
				current_letters_to_guess = copy.copy(getNewWord(w5))
			if current_word_len == 6:
				current_letters_to_guess = copy.copy(getNewWord(w6))
				
			possible_word = copy.copy(current_letters_to_guess)#remember, so it can be shown on game over screen
			
			#add 2 random letters to new word
			current_letters_to_guess += random.choice('abcdefghijklmnopqrstuvwxyz')
			current_letters_to_guess += random.choice('abcdefghijklmnopqrstuvwxyz')
			
			#shuffle new word
			l = list(current_letters_to_guess)
			random.shuffle(l)
			current_letters_to_guess = ''.join(l)
			
			given_letters_stringVar.set('Letters:'+current_letters_to_guess)
			
			#set new word
			word_stringVar.set(str('_ '*current_word_len) +':'+ 'Correct, '+str(current_word_len)+' letters next.' + '(' + str(failed_guesses) + '/3)')
			
		#reset timer
		print('extra time:'+str(added_time))
		countdown_sec += added_time
		
	else: word_stringVar.set(str('_ '*current_word_len) +':'+ word_guess_so_far + '  (' + str(failed_guesses) + '/3)')
	
def getNewWord(wX):
	return wX[random.randrange(len(wX))]
	
MyFont = font.Font(size=36)
word_stringVar = StringVar()
given_letters_stringVar = StringVar()
countdown_stringVar = StringVar()
def nextGame():
	global word_stringVar
	global failed_guesses
	global countdown_stringVar
	global possible_word
	global current_letters_to_guess
	global w3
	print('nextGame()')
	frame_words_guess.bind("<KeyPress>", keydown)
	frame_words_guess.focus_set()
	frame_words_guess.pack(side = BOTTOM)
	
	word_stringVar_label = Label(frame_words_guess, font=MyFont, textvariable=word_stringVar).pack()
	word_stringVar.set('_ _ _:'+str('your guess') + '  (' + str(failed_guesses) + '/3)')
	
	given_letters_stringVar_label = Label(frame_words_guess, font=MyFont, textvariable=given_letters_stringVar).pack()
	
	#add 3 letter word shuffled with 2 extra random letters
	current_letters_to_guess_temp = copy.copy(getNewWord(w3))
	possible_word = copy.copy(current_letters_to_guess_temp)#remember, so it can be shown on game over screen
	current_letters_to_guess_temp += random.choice('abcdefghijklmnopqrstuvwxyz')
	current_letters_to_guess_temp += random.choice('abcdefghijklmnopqrstuvwxyz')
	#shuffle new word
	l = list(current_letters_to_guess_temp)
	random.shuffle(l)
	current_letters_to_guess_temp = ''.join(l)
	current_letters_to_guess = copy.copy(current_letters_to_guess_temp)
	given_letters_stringVar.set('Letters:'+str(current_letters_to_guess_temp))
	
	countdown_stringVar_label = Label(frame_words_guess, font=MyFont, textvariable=countdown_stringVar).pack()
	countdown_stringVar.set('60 seconds remaining')
	
	countdown()
	
root.after(30000, nextGame)#30000 = 30sec
refresh()
root.mainloop()