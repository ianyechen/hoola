def cardnum_to_cardstr(card):

    number = str(card % 13)
    if (number == '0'): number = '13'

    suit = (card-1) // 13
    if (suit == 0): suit = 'c'
    elif (suit == 1): suit = 'd'
    elif (suit == 2): suit = 'h'
    else: suit = 's'

    return './cards/' + suit + number + '.png'
    
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
            
def player_turn(player):

    return player + 1 if (player + 1 != 4) else 0