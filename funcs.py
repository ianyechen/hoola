# converting a card number to a card string (5 -> c5)
# params: int card 
# return: str card 
def cardnum_to_cardstr(card):

    number = str(card % 13)
    if (number == '0'): number = '13'

    suit = (card-1) // 13
    if (suit == 0): suit = 'c'
    elif (suit == 1): suit = 'd'
    elif (suit == 2): suit = 'h'
    else: suit = 's'

    return './cards/' + suit + number + '.png'

# converting a card string to a card number (c5 -> 5)
# params: str card 
# return: int card 
def cardstr_to_cardnum(card):
    
    multiply = 0

    if card[0] == 'c': multiply = 0
    elif card[0] == 'd': multiply = 1
    elif card[0] == 'h': multiply = 2
    else: multiply = 3

    return int((multiply * 13)) + int(card[1:])
     
# checking to see if a meld is valid or not 
# params: list cards 
# return: bool result 
def is_meld_valid(cards):

    if len(cards) == 1:
        if cards[0][1] == '7': return True
        else: return False

    elif len(cards) == 2:
        if (cards[0][0] == cards[1][0]) and (abs(int(cards[0][1]) - int(cards[1][1])) == 1) and (cards[0][1] == '7' or cards[1][1] == '7'): return True
        else: return False

    elif len(cards) == 3:

        cards_with_num = []

        for card in cards:
            card_num = int(card[1:])
            cards_with_num.append(card_num)

        if cards[0][0] == cards[1][0] == cards[2][0]:
           
            cards_with_num.sort()

            if 13 and 1 in cards_with_num:
                cards_with_num[1] %= 10
                cards_with_num[2] %= 10
                cards_with_num.sort()
            
            for count, card in enumerate(cards_with_num):
                if count + 1 >= len(cards_with_num): break
                if cards_with_num[count+1] != card + 1: return False

            return True

        else:
            if cards_with_num[0] == cards_with_num[1] == cards_with_num[2]: return True
            else: return False
            
# checking to see if a end turn is valid or not 
# params: list cards 
# return: bool result 
def is_end_turn_valid(cards):
    if len(cards) != 1: return False
    else: return True