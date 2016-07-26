# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 950x392 - source: jfitz.com
CARD_SIZE = (73, 98)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize global variables
deck = []
in_play = False
outcome = ""
score = 0
covered = True

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            print "Invalid card: ", self.suit, self.rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_SIZE[0] * (0.5 + RANKS.index(self.rank)), CARD_SIZE[1] * (0.5 + SUITS.index(self.suit)))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_SIZE[0] / 2, pos[1] + CARD_SIZE[1] / 2], CARD_SIZE)
        if covered:
            canvas.draw_image(card_back, [CARD_BACK_SIZE[0] /2 , CARD_BACK_SIZE[1] /2], CARD_BACK_SIZE, [96, 260], CARD_BACK_SIZE)
                
# define hand class
class Hand:
    def __init__(self):
        self.cards=[]

    def __str__(self):
        hand = ""
        for card in self.cards:
             hand = hand + " " + str(card)
        return hand
    
    def add_card(self, card):
        self.cards.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if don't bust
    def get_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                aces += 1
            if (aces >= 1) and ((value + 10) < 21):
                value = value + 10
        return value

    def busted(self):
        if self.get_value() > 21:
            return True
    
    def draw(self, canvas, p):
        spacing = 0
        for card in self.cards:
            # we draw at the same height (y), but advance the x. The 20 is space between cards.
            card.draw(canvas, [p[0] + spacing * (CARD_SIZE[0] + 20), p[1]])
            spacing += 1
 
        
# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))
        
    def __str__(self):
        deck = ""
        for card in self.deck:
            deck = deck + " " + str(card) 
        return deck

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

#define callbacks for buttons
def deal():
    global outcome, in_play, covered
    
    initial_deal ()
    outcome = "Hit or Stand?"
    covered = True
    in_play = True

def hit():
    global in_play, score, outcome, covered
 
    # if the hand is in play, hit the player
    if in_play == True:
        player_hand.add_card(deck.deal_card())     
   
    # if busted, assign an message to outcome, update in_play and score
        if player_hand.busted():
            score -= 1
            outcome = "Player Busted!"
            in_play = False
            covered = False

       
def stand():
    global in_play, outcome, score, covered
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    if in_play:
        covered = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.busted():
            score += 1
            outcome = "Dealer Busted, Player Wins!"
            in_play = False
        elif dealer_hand.get_value() >= player_hand.get_value():
            score -= 1
            outcome = "Dealer Wins"
            in_play = False
        else:
            score += 1
            outcome = "Player Wins"
            in_play = False
            
    # assign a message to outcome, update in_play and score

def draw(canvas):
    canvas.draw_text("Blackjack", [40,60], 42, "Yellow")
    canvas.draw_text("Score: " + str(score), [450,60], 28, "Yellow")
    canvas.draw_text(outcome, [60, 550], 24, "Yellow")
    canvas.draw_text("Dealer", [60, 200], 24, "Yellow")
    canvas.draw_text("Player", [60, 400], 24, "Yellow")
    
    player_hand.draw(canvas, [60, 410])
    dealer_hand.draw(canvas, [60, 210])
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand

def initial_deal():
    global deck, player_hand, dealer_hand, outcome, in_play
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    deck.shuffle()
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    if player_hand.get_value() == 21:
        score += 1
        outcome = "Blackjack! Player wins!"
        in_play = False
        
# get things rolling
frame.start()

deal()

# Grading rubric - 18 pts total (scaled to 100)

# 1 pt - The program opens a frame with the title "Blackjack" appearing on the canvas.
# 3 pts - The program displays 3 buttons ("Deal", "Hit" and "Stand") in the control area. (1 pt per button)
# 2 pts - The program graphically displays the player's hand using card sprites. 
#		(1 pt if text is displayed in the console instead) 
# 2 pts - The program graphically displays the dealer's hand using card sprites. 
#		Displaying both of the dealer's cards face up is allowable when evaluating this bullet. 
#		(1 pt if text displayed in the console instead)
# 1 pt - Hitting the "Deal" button deals out new hands to the player and dealer.
# 1 pt - Hitting the "Hit" button deals another card to the player. 
# 1 pt - Hitting the "Stand" button deals cards to the dealer as necessary.
# 1 pt - The program correctly recognizes the player busting. 
# 1 pt - The program correctly recognizes the dealer busting. 
# 1 pt - The program correctly computes hand values and declares a winner. 
#		Evalute based on player/dealer winner messages. 
# 1 pt - The dealer's hole card is hidden until the hand is over when it is then displayed.
# 2 pts - The program accurately prompts the player for an action with the messages 
#        "Hit or stand?" and "New deal?". (1 pt per message)
# 1 pt - The program keeps score correctly.