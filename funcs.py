# converting a card number to a card string (26 -> d13)
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

    return suit + number

# converting a card number to the corresponding card image path (5 -> ./cards/c5.png)
# params: int card 
# return: str card path
def cardnum_to_card_image_path(card):

    cardstr = cardnum_to_cardstr(card)

    return './cards/' + cardstr + '.png'

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

    # if only one card, only a 7 is valid
    if len(cards) == 1:
        if cards[0][1] == '7': return True
        else: return False

    # if only two cards, it has to have a 7 with a consecutive pattern
    elif len(cards) == 2:
        if (cards[0][0] == cards[1][0]) and (abs(int(cards[0][1]) - int(cards[1][1])) == 1) and (cards[0][1] == '7' or cards[1][1] == '7'): return True
        else: return False

    else:

        # holds a list of only the card numbers without the suit 
        cards_with_num = []
        consecutive = True

        for count, card in enumerate(cards):
            if count != len(cards) - 1 and cards[count][0] != cards[count+1][0]: consecutive = False
            card_num = int(card[1:])
            cards_with_num.append(card_num)

        # at least three consecutive numbers 
        if consecutive:
           
            cards_with_num.sort()

            loop = False
            if 13 and 1 in cards_with_num: loop = True 
            broke_order = 0

            for count, card in enumerate(cards_with_num):
                if count + 1 >= len(cards_with_num): 
                    if broke_order != 0 and cards_with_num[count] == 13 and 1 not in cards_with_num: broke_order += 1
                    break
                if cards_with_num[count+1] != card + 1: broke_order += 1

            if (loop and broke_order < 2) or (not loop and broke_order == 0): return True
            else: return False

        # at least three of the same numbers 
        else:
            for i in range(len(cards_with_num)):
                if i+1 == len(cards_with_num): return True
                elif cards_with_num[i] != cards_with_num[i+1]: return False
           
# checking to see if an add is valid or not 
# params: list cards_currently_selected, list of lists, melded combinations for a player 
# return: bool valid, int index of the melded combination to be added to  
def is_add_valid(cards_currently_selected, melded_cards):

    cards_to_be_added = list(cards_currently_selected)
    
    for index in range(len(cards_to_be_added)):
        cards_to_be_added[index] = cardstr_to_cardnum(cards_to_be_added[index])
        
    if len(cards_to_be_added) == 1:

        for index, combination in enumerate(melded_cards):

            # if adding to a 7 
            if len(combination) == 1:
                if cards_to_be_added[0] == combination[0] + 1 or cards_to_be_added[0] == combination[0] - 1: return True, index
            # if adding to other combinations 
            elif len(combination) >= 2:
                if combination[0] % 13 == combination[-1] % 13 == cards_to_be_added[0] % 13: return True, index
                if combination[1] == combination[0] + 1:
                    if cards_to_be_added[0] % 13 == 1 and combination[-1] % 13 == 0 and cards_to_be_added[0] == combination[-1] - 12: return True, index
                    elif cards_to_be_added[0] % 13 == 0 and combination[0] % 13 == 1 and cards_to_be_added[0] == combination[0] + 12: return True, index
                    elif (abs(cards_to_be_added[0] - combination[0]) == 1 or 
                          abs(cards_to_be_added[0] - combination[-1]) == 1): return True, index
             
    # still needs to add if adding more than 1 card 
    return False, 0

# checking to see if a end turn is valid or not 
# params: list cards 
# return: bool result 
def is_end_turn_valid(cards):
    if len(cards) != 1: return False
    else: return True