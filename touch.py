from kivy.uix.widget import Widget

class Touch(Widget):
    def __init__(self, **kwargs):
        super(Touch, self).__init__(**kwargs)
     
    def on_touch_down(self, touch):
        if touch.spos[1] > 0.25: return
        # print('Mouse Down', touch)
        distance = (touch.spos[0] - 0.45) // 0.05
        num_cards = len(self.parent.players[0].player_cards) 
        selected_card = (num_cards//2) - int(distance)
        if selected_card < 0 or selected_card >= num_cards: return
        # print(self.parent.children) 
        pos_x = self.parent.children[selected_card].pos_hint['x']
        pos_y = 0.05 if self.parent.children[selected_card].pos_hint['y'] == 0 else 0
        self.parent.children[selected_card].pos_hint = {'x': pos_x, 'y': pos_y}

    def on_touch_up(self, touch):
        pass

    def on_touch_move(self, touch):
        pass