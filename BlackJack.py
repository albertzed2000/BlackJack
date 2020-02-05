# Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize global variables: 
in_play = True
has_lost = False
# define global constants for cards:
# tuples for suits and ranks
# dictionary of values
SUITS = ('C','S','H','D')
RANKS = ('A','2','3','4','5','6',
         '7','8','9','10','J','Q','K')
VALUES = {'A':1,'2':2,'3':3,
          '4':4,'5':5,'6':6,
         '7':7,'8':8,'9':9,
          '10':10,'J':10,
          'Q':10,'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_img_loc = [CARD_CENTER[0] + RANKS.index(self.rank)*CARD_SIZE[0], CARD_CENTER[1] + SUITS.index(self.suit)*CARD_SIZE[1]]
        canvas.draw_image(card_images,
                         card_img_loc,
                         CARD_SIZE,
                         pos,
                         CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        s = ""
        for card in self.cards:
            s += str(card) + " "
        return s   
    
    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        v = 0
        for card in self.cards:
            v += VALUES[card.get_rank()]
        for card in self.cards:
            if card.get_rank() == "A" and v + 10 <= 21:
                v += 10 
        return v    
        
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, 
                      [pos[0] + self.cards.index(card)*CARD_SIZE[0], pos[1]])
                      
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                self.cards.append(Card(SUITS[i],RANKS[j]))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop(0)
    
    def __str__(self):
        s = ""
        for card in self.cards:
            s += str(card) + " "
        return s    
    
#define event handlers for buttons
def deal():
    global deck, player_hand, dealer_hand, in_play
    #count deal in the middle of a round as a forfeit
    in_play = True
    #initialize deck
    deck = Deck()
    deck.shuffle()
    #initialize hands
    player_hand = Hand()
    dealer_hand = Hand()
    #add cards to hands
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())


def hit():
    global in_play
    # if the hand is in play, deal a card to player's hand
    if in_play:
        player_hand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update 
    
    # in_play and score
    player_val = player_hand.get_value()
    if player_val > 21:
        in_play = False
        
def stand():
    # if hand is in play, repeatedly hit dealer until 
    # his hand has value 17 or more
    global in_play, has_lost
    while dealer_hand.get_value()< 17:
        dealer_hand.add_card(deck.deal_card())
        
        dealer_val = dealer_hand.get_value()
        player_val = player_hand.get_value()
        
        if dealer_val > 21:
            in_play = False  
            has_lost = False
            return
        elif dealer_val >= player_val:
            in_play = False
            has_lost = True
            return

    
    dealer_val = dealer_hand.get_value()
    player_val = player_hand.get_value()
    
    if dealer_val >= player_val:
        in_play = False
        has_lost = True
    else:    
        in_play = False
        has_lost = False
        # assign a message to outcome, update in_play and score
    
        
# draw handler    
def draw(canvas):
    global has_lost
    dealer_val = dealer_hand.get_value()
    player_val = player_hand.get_value()
    if dealer_val > player_val and dealer_val <= 21:
        has_lost = True
    elif dealer_val < player_val and player_val < 21:
        has_lost = False
    elif dealer_val > 21 and player_val <= 21:
        has_lost = False
    elif dealer_val <= 21 and player_val > 21:
        has_lost = True
    elif dealer_val == player_val:
        has_pushed = True
    dealer_hand.draw(canvas, [50, 200])
    player_hand.draw(canvas, [50, 400])
    
    if in_play == False:
        canvas.draw_text(str(dealer_val), (500, 200), 40, 'White')
        
    canvas.draw_text(str(player_val), (500, 500), 40, 'White') 
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50,200], CARD_BACK_SIZE)        
                 
    if in_play == False and has_lost == True:
        canvas.draw_text("You Lost ", (100, 500), 25, 'White')
        
    elif in_play == False and has_lost == False:
        canvas.draw_text("You Won!", (700, 500), 25, 'White') 
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()