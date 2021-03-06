from kivy.uix.widget import Widget

class Touch(Widget):
    def __init__(self, **kwargs):
        super(Touch, self).__init__(**kwargs)
     
    def on_touch_down(self, touch):
        
        # too far up, not selecting anything 
        if touch.spos[1] > 0.25: return

        # each card is 0.05 in width
        distance = (touch.spos[0] - 0.45) // 0.05
        num_cards = len(self.parent.players[0].player_cards) 
        selected_card = (num_cards//2) + int(distance)
        if selected_card < 0 or selected_card >= num_cards: return

        pos_x = self.parent.widgets_for_player_cards[0][selected_card].pos_hint['x']
        pos_y = self.parent.widgets_for_player_cards[0][selected_card].pos_hint['y']

        if self.parent.widgets_for_player_cards[0][selected_card].pos_hint['y'] == 0:
            pos_y = 0.05
            card_str = self.parent.widgets_for_player_cards[0][selected_card].source[8:]
            card_str = card_str.split('.')[0]
            self.parent.cards_currently_selected.append(card_str)
          
        else: 
            pos_y = 0
            card_str = self.parent.widgets_for_player_cards[0][selected_card].source[8:]
            card_str = card_str.split('.')[0]

            self.parent.cards_currently_selected.remove(card_str)

        self.parent.widgets_for_player_cards[0][selected_card].pos_hint = {'x': pos_x, 'y': pos_y}

    def on_touch_up(self, touch):
        pass

    def on_touch_move(self, touch):
        pass