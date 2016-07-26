import simplegui
import random

#functions and handlers
def new_game():
    global cards, exposed, state, turn
    state = 0
    turn = 0
    cards = range(8)
    cards.extend(range(8))
    exposed = [False for n in cards]
    random.shuffle(cards)
    l.set_text("Turns = " + str(turn))
    #print cards

def mouseclick(pos):
    global exposed, state, memory, turn
    if(not pos[0] % 50 > 45):
        idx = pos[0] / 50
        
        if exposed[idx]:
            '''Stops if the card is already turned up'''
            return
        if state == 0:
            memory = [idx]
            state = 1
        elif state == 1:
            state = 2
            memory.append(idx)
        else:
            state = 1
            if(not cards[memory[0]] == cards[memory[1]]):
                exposed[memory[0]] = False
                exposed[memory[1]] = False
            memory = [idx]
        if state == 1:
            turn += 1
            l.set_text("Turns = " + str(turn))
        exposed[idx] = True

def draw(canvas):
    for card in enumerate(cards):
        x = 50 * card[0]
        if exposed[card[0]]:
            canvas.draw_polygon([(x, 5), (x+45, 5), (x+45, 95), (x, 95)], 2, 'White', '#808080')
            canvas.draw_text(str(card[1]), (x+10, 65), 48, 'White')
        else: 
            canvas.draw_polygon([(x, 5), (x+45, 5), (x+45, 95), (x, 95)], 2, 'White', 'Blue')

#frame and controls
frame = simplegui.create_frame("Memory", 800, 100)
frame.set_canvas_background("#4DDE2C")
frame.add_button("Restart", new_game)
l=frame.add_label("Turns = 0")

#assign handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

#event handler
new_game()
frame.start()