rules_string = '''

1. Melds
    As in all rummy games the objective is to form melds. These may be sets of equal cards, 
    or sequences of consecutive cards in a suit. Sets and sequences must consist of at least
    three cards unless they contain a seven. The sevens are special cards. A single seven by
    itself is a valid meld. 

    Examples of valid melds include:
        a. diamond A, diamond 2, diamond 3
        b. spade Q, clover Q, hearts Q
        c. spade 7
        d. clover 6, clover 7

    Notes: 
        a. A card cannot be used in more than one meld at the same time
        b. Ace counts as high, low or both, so that A-2-3, Q-K-A and K-A-2 are all valid sequences.

2. The Play 
    A turn consists of:
        a. drawing one card from the top of the stock pile or discard pile
        b. optionally placing one or more melds from hand face up on the table 
        c. optionally extending melds that are already on the table by adding cards to make larger melds
        d. discarding one card face up on the discard pile.

    Notes:
        a. The discard can only be taken if it is immediately used to lay down a new meld from the
            player's hand. It is not possible to take the discard to add it to an existing meld on the
            table, or to keep in hand for future use.
        b. Cards can only be added to melds that are already on the table if the player has already,
            in the same turn or a previous turn, played a complete new meld from hand.
        c. The play ends when one player has no more cards in their hand.

'''