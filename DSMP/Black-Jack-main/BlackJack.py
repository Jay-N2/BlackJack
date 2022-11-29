from random import seed
from datetime import datetime
from time import sleep
from PIL import ImageTk, Image
from tkinter import Entry, Button, Tk, Canvas, Label, filedialog, IntVar
from playsound import playsound
import random

# Once before randint call
seed(datetime.now())

# Global Variables
kind = {"hearts", "diamonds", "spades", "clubs"}
number = {"ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king"}

# 52 Cards
# deck = {(k, n) for k in kind for n in number}

# Array to append cards when we call the hit() or stand() function
HIT = []
STAND = []

add_card = ""
width = 300
number_card = 2

# score[0] - Player , score[1] - Dealer
score = [0, 0]

# Sound effects path
path_card_sound = 'Sound_Effects\\CardPlace.mp3'
path_start_sound = 'Sound_Effects\\StartSound.mp3'
path_win_sound = 'Sound_Effects\\WinSound.mp3'
path_lost_sound = 'Sound_Effects\\LostSound.mp3'
path_tie_sound = 'Sound_Effects\\TieSound.mp3'

# Build Tkinter GUI
root = Tk(className=" BlackJack")
canvas1 = Canvas(root, width=1000, height=550, relief='raised', bg='#00B050')
canvas1.pack()


#############
# Functions #
#############


# Open an .png image an return it
def pick_card(card_name):
    path_name = "PNG-Cards" + "\\" + card_name + ".png"
    img = Image.open(path_name)
    img = img.resize((80, 120), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img


# When we push the START button we destroy it
# and show up the buttons HIT & STAND
def start():
    # global Start
    Start.destroy()
    playsound(path_start_sound)

    global Hit, Stand
    Hit = Button(text='HIT', command=hit, bg='#0070C0', fg='black',
                 font=('Times New Roman', 16, 'bold'))
    canvas1.create_window(100, 520, window=Hit, width=90)

    Stand = Button(text='STAND', command=stand, bg='#FF0000', fg='black',
                   font=('Times New Roman', 16, 'bold'))
    canvas1.create_window(200, 520, window=Stand, width=90)


# Return the value of cards that a player or a dealer has
def hand_value(hand):
    s = 0
    for card in hand:
        n = card[1]
        if n == "jack" or n == "queen" or n == "king":
            s += 10
        elif n == "ace":
            if s + 11 <= 21:
                s += 11
            else:
                s += 1
        else:
            s += n

    return s


##################################################
# IT DOES NOT USE IT... BUT MAYBE USE IT NEXT TIME
#################################################
# Player Function that initializes 2 cards and
# ask for Hit(Continue) or Stand(Stop)
def player(hand):
    while True:
        global HIT, STAND
        print(hand)
        print("Waiting...")
        choice = input("H-Hit or S-Stand: ")
        if choice == "H":
            hand.add(deck.pop())
            if int(hand_value(hand)) >= 21:
                return hand_value(hand)
        elif choice == "S":
            return hand_value(hand)


#################################################


# Computer Function that take as first parameter the
# final value of player and play like the player
# until it wins or lost
def computer(value_player, hand):
    global STAND
    i = 2
    size = 300

    while True:
        value = int(hand_value(hand))
        #        >= 21
        if value >= 17:
            return value
        #          >=
        elif value > value_player:
            return value
        else:
            hand.append(deck.pop())

            add_card = list(hand)[i]
            add_card = str(add_card[1]) + "_" + str(add_card[0])
            add_card = pick_card(add_card)

            STAND.append(add_card)

            label_computer = Label(root, image=STAND[i - 2])
            canvas1.create_window(size, 200, window=label_computer)
            canvas1.update()

            # Play the card sound effect
            playsound(path_card_sound)

            i += 1
            size += 100
            sleep(.25)


# Keeps and increase the score of player and dealer,
# and call the function play_again()
def score_table(score, result):
    # TEST VALUE TO DEBUG PLAYER (ONLY FOR DEBUG SO FAR)
    global player_hand
    # print(hand_value(player_hand))
    label_player = Label(root, text=' = ' + str(hand_value(player_hand)))
    label_player.config(font=('Times New Roman', 17), bg='#00B050')
    canvas1.create_window(220, 320, window=label_player)
    ############################

    # TEST VALUE TO DEBUG DEALER (ONLY FOR DEBUG SO FAR)
    global computer_hand
    # print(hand_value(computer_hand))
    label_player = Label(root, text=' = ' + str(hand_value(computer_hand)))
    label_player.config(font=('Times New Roman', 17), bg='#00B050')
    canvas1.create_window(220, 110, window=label_player)
    ############################

    if result == "player":
        playsound(path_win_sound)
        score[0] += 1
    elif result == "computer":
        playsound(path_lost_sound)
        score[1] += 1
    elif result == "tie":
        Hit.config(command="")
        Stand.config(command="")
        Hit.update()
        Stand.update()
        playsound(path_tie_sound)

    play_again()


# Wait until the user push the button play again
# after delete and initialize the game again
# and call the main() function
def play_again():
    global number_card, width
    # print("*************PLAY AGAIN NOW***************")
    var = IntVar()

    button = Button(root, text="Play Again", command=lambda: var.set(1))
    button.config(font=('Times New Roman', 15, 'bold'))
    canvas1.create_window(833, 500, window=button)
    button.wait_variable(var)

    canvas1.delete("all")
    number_card = 2
    width = 300
    HIT.clear()
    STAND.clear()
    main()


# Main
def main():
    # 52 Cards
    global deck
    deck = [(k, n) for k in kind for n in number]
    random.shuffle(deck)

    # Once, before randint call
    seed(datetime.now())

    # Open Black Jack image and create a Label
    black_jack_img = Image.open("GUIElements\\Black_Jack_logo.png")
    black_jack_img = black_jack_img.resize((400, 110), Image.ANTIALIAS)
    black_jack_img = ImageTk.PhotoImage(black_jack_img)

    label1 = Label(root, image=black_jack_img, bg='#00B050')
    canvas1.create_window(500, 60, window=label1)

    # Create a Label under the Black_Jack_logo(with a tagline)cd
    label_dealer_text = Label(root, foreground='#1a0000', text="It's either all win or all lose!")
    label_dealer_text.config(font=('Times New Roman', 19, 'bold'), bg='#00B050')
    canvas1.create_window(500, 130, window=label_dealer_text)

    # Create a Label for a Dealer
    label_dealer = Label(root, text='DEALER')
    label_dealer.config(font=('Times New Roman', 17), bg='#00B050')
    canvas1.create_window(150, 110, window=label_dealer)

    # Create a Label for a Player
    label_player = Label(root, text='PLAYER')
    label_player.config(font=('Times New Roman', 17), bg='#00B050')
    canvas1.create_window(150, 320, window=label_player)

    # Open score image and create a label
    score_img = Image.open("GUIElements\\ScoreBoard.png")
    score_img = score_img.resize((230, 100), Image.ANTIALIAS)
    score_img = ImageTk.PhotoImage(score_img)

    score_label = Label(root, image=score_img, bg='#00B050')
    canvas1.create_window(830, 410, window=score_label)

    # Player Score
    score_player = Label(root, text=str(score[0]), bg='#BDD6EE',
                         font=('Times New Roman', 13, 'bold'), width=3)
    canvas1.create_window(776, 442, window=score_player)

    # Dealer Score
    score_dealer = Label(root, text=str(score[1]), bg='#BDD6EE',
                         font=('Times New Roman', 13, 'bold'), width=3)
    canvas1.create_window(886, 442, window=score_dealer)

    seed(datetime.now())  # once, before randint call

    # Create array for player
    global player_hand
    player_hand = []

    # Player - Initialize 2 random cards from deck
    player_hand.append(deck.pop())
    card1_player = list(player_hand)[0]
    card1_player = str(card1_player[1]) + "_" + str(card1_player[0])
    card1_player = pick_card(card1_player)
    label1_player = Label(root, image=card1_player)
    canvas1.create_window(100, 410, window=label1_player)

    player_hand.append(deck.pop())
    card2_player = list(player_hand)[1]
    card2_player = str(card2_player[1]) + "_" + str(card2_player[0])
    card2_player = pick_card(card2_player)
    label2_player = Label(root, image=card2_player)
    canvas1.create_window(200, 410, window=label2_player)

    # Create array for dealer
    global computer_hand
    computer_hand = []

    # Dealer - Initialize 2 random cards from deck
    computer_hand.append(deck.pop())
    card1_dealer = list(computer_hand)[0]
    card1_dealer = str(card1_dealer[1]) + "_" + str(card1_dealer[0])
    card1_dealer = pick_card(card1_dealer)
    label1_dealer = Label(root, image=card1_dealer)
    canvas1.create_window(100, 200, window=label1_dealer)

    card2_dealer = pick_card("Back_of_Card")
    label2_dealer = Label(root, image=card2_dealer)
    canvas1.create_window(200, 200, window=label2_dealer)

    # Initialize START Button
    global Start
    Start = Button(text='START', command=start, bg='#92D050', fg='black',
                   font=('Times New Roman', 17, 'bold'))
    canvas1.create_window(150, 520, window=Start)

    # If the first 2 cards that a player takes is equal to 21(Player wins immediately!)
    if int(hand_value(player_hand)) == 21:

        # Disable the buttons HIT & STAND
        Hit.config(command="")
        Stand.config(command="")
        Hit.update()
        Stand.update()

        # Keep the Player Value
        player_value = hand_value(player_hand)

        # print("Computer Play NOW!")
        sleep(2)

        # Dealer - Append new card from deck
        computer_hand.append(deck.pop())
        card2_dealer = list(computer_hand)[1]
        card2_dealer = str(card2_dealer[1]) + "_" + str(card2_dealer[0])
        card2_dealer = pick_card(card2_dealer)
        label2_dealer = Label(root, image=card2_dealer)
        canvas1.create_window(200, 200, window=label2_dealer)
        root.update()

        # Keep the Dealer value
        computer_value = computer(player_value, computer_hand)

        # Check if computer hits 21 or Not
        if computer_value == 21:
            score_table(score, "tie")
        else:
            Win = Label(root, bg="yellow", text="You WIN! HIT 21 Points!",
                        font=('Times New Roman', 22, 'bold'), width=19)
            canvas1.create_window(820, 280, window=Win)
            root.update()
            score_table(score, "player")

    # hit() function activated when the player push the HIT button
    global hit
    def hit():
        global HIT, STAND
        global add_card
        global width, number_card

        # Player - Append new card from deck
        player_hand.append(deck.pop())

        add_card = list(player_hand)[number_card]
        add_card = str(add_card[1]) + "_" + str(add_card[0])
        add_card = pick_card(add_card)

        HIT.append(add_card)

        label_player_card = Label(root, image=HIT[number_card - 2])
        canvas1.create_window(width, 410, window=label_player_card)
        canvas1.update()

        # Play the card sound effect
        playsound(path_card_sound)

        width += 100
        number_card += 1

        if int(hand_value(player_hand)) >= 21:

            # Take the player value
            player_value = hand_value(player_hand)

            # Disable the buttons HIT & STAND
            Hit.config(command="")
            Stand.config(command="")
            Hit.update()
            Stand.update()

            if player_value == 21:
                # print("Computer Play NOW!")
                sleep(2)

                # Dealer - Append new card from deck
                computer_hand.append(deck.pop())
                card2_dealer = list(computer_hand)[1]
                card2_dealer = str(card2_dealer[1]) + "_" + str(card2_dealer[0])
                card2_dealer = pick_card(card2_dealer)
                label2_dealer = Label(root, image=card2_dealer)
                canvas1.create_window(200, 200, window=label2_dealer)
                root.update()

                # Keep the Dealer value
                computer_value = computer(player_value, computer_hand)

                # Check if computer hits 21 or Not
                if computer_value == 21:
                    score_table(score, "tie")
                else:
                    Win = Label(root, bg="yellow", text="You WIN! HIT 21 Points!",
                                font=('Times New Roman', 22, 'bold'), width=19)
                    canvas1.create_window(820, 280, window=Win)
                    root.update()
                    score_table(score, "player")
            elif player_value > 21:
                Lost = Label(root, bg="red", text="You lost the Round!",
                             font=('Times New Roman', 22, 'bold'), width=18)
                canvas1.create_window(820, 280, window=Lost)
                root.update()
                score_table(score, "computer")
            else:
                # print("Computer Play NOW!")
                sleep(2)

                # Dealer - Append new card from deck
                computer_hand.append(deck.pop())
                card2_dealer = list(computer_hand)[1]
                card2_dealer = str(card2_dealer[1]) + "_" + str(card2_dealer[0])
                card2_dealer = pick_card(card2_dealer)
                label2_dealer = Label(root, image=card2_dealer)
                canvas1.create_window(200, 200, window=label2_dealer)
                root.update()

                # Keep the Dealer value
                computer_value = computer(player_value, computer_hand)

                if computer_value > 21:
                    Win = Label(root, bg="yellow", text="YOU WIN!",
                                font=('Times New Roman', 22, 'bold'), width=18)
                    canvas1.create_window(820, 280, window=Win)
                    root.update()
                    score_table(score, "player")
                else:
                    Lost = Label(root, bg="red", text="YOU LOST!",
                                 font=('Times New Roman', 22, 'bold'), width=18)
                    canvas1.create_window(820, 280, window=Lost)
                    root.update()
                    score_table(score, "computer")

    # stand() function activated when the player push the STAND button
    global stand
    def stand():

        # Disable the buttons HIT & STAND
        Stand.config(command="")
        Hit.config(command="")
        Stand.update()
        Hit.update()

        # Keep the Player value
        player_value = hand_value(player_hand)

        # print("Computer Play NOW!")
        sleep(2)

        # That is the second card of DEALER
        # Dealer - Append new card from deck
        computer_hand.append(deck.pop())

        card2_dealer = list(computer_hand)[1]
        card2_dealer = str(card2_dealer[1]) + "_" + str(card2_dealer[0])
        card2_dealer = pick_card(card2_dealer)

        label2_dealer = Label(root, image=card2_dealer)
        canvas1.create_window(200, 200, window=label2_dealer)
        root.update()

        # Play the card sound effect
        playsound(path_card_sound)

        # Keep the Dealer value
        computer_value = computer(player_value, computer_hand)

        if computer_value > 21 or player_value > computer_value:
            Win = Label(root, bg="yellow", text="YOU WIN!",
                        font=('Times New Roman', 22, 'bold'), width=18)
            canvas1.create_window(820, 280, window=Win)
            root.update()
            score_table(score, "player")
        elif computer_value == player_value:
            Tie = Label(root, bg="grey", text="  TIE!",
                        font=('Times New Roman', 22, 'bold'), width=18)
            canvas1.create_window(820, 280, window=Tie)
            root.update()
            score_table(score, "tie")
        else:
            Lost = Label(root, bg="red", text="YOU LOST!",
                         font=('Times New Roman', 22, 'bold'), width=18)
            canvas1.create_window(820, 280, window=Lost)
            root.update()
            score_table(score, "computer")

    root.mainloop()


main()
