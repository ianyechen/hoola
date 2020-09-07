import kivy
import random 
import sys

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, BooleanProperty, StringProperty
from kivy.clock import Clock 
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView

from rotated_cards import RotatedCards
from touch import Touch
from player import Player
from funcs import cardnum_to_card_image_path, cardstr_to_cardnum, is_meld_valid, is_add_valid, is_end_turn_valid, cardnum_to_cardstr
from functools import partial
from rules import rules_string

class ImageButton(ButtonBehavior, Image):
    pass

class WindowManager(ScreenManager):
    pass

class TitleWindow(Screen):
    pass


class RulesWindow(Screen):
    rules = StringProperty('')

    def __init__(self, **kwargs):
        super(RulesWindow, self).__init__(**kwargs)
        self.rules = rules_string

class PopUpWindow(FloatLayout):

    game_over_message = StringProperty('')

    def __init__(self, game_over_message, **kwargs):
        super(PopUpWindow, self).__init__(**kwargs)
        self.game_over_message = game_over_message
        print(self.game_over_message)
    
    def close_popup(self):
        print(self.get_parent_window())

Builder.load_string('''
<ScrolllabelLabel>:

    # pos_hint: {'x':0.05,'y':-0.8}
    size_hint: (0.25, 0.3)
    Label:
        text: root.game_log
        font_size: 18
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]

''')

class ScrolllabelLabel(ScrollView):
    game_log = StringProperty('')

    def __init__(self, **kwargs):
        super(ScrolllabelLabel, self).__init__(**kwargs)


    # def on_scroll_start(self, scroll):
    #     print(scroll)


class GameWindow(Screen):

    # indicates whether or not the first card has been taken for a turn 
    took_first_card = BooleanProperty(False)
    # number of cards left in the entire deck 
    number_of_cards_left = NumericProperty(0)
    # whether to hide the buttons or display
    buttons_visible = BooleanProperty(True)
    # whether player is deciding a thank you or not (shows the pass or thank you button)
    deciding_thank_you = BooleanProperty(False)
    # what the response for the thank you is (False is pass, True is Thank You)
    response_for_thank_you = BooleanProperty(False)
    # the entire card deck left for players to draw from 
    card_deck = []
    # holds the 4 Player classes 
    players = []
    # holds the current player's widgets for displaying the cards in hand
    widgets_for_player_cards = [[],[],[],[]]
    # holds the current player's widgets for displaying the cards that were melded
    widgets_for_player_melds = [[],[],[],[]]
    # holds the cards currently selected by the player in string ('h13')
    cards_currently_selected = []
    # holds which turn it is (0-3)
    turn = NumericProperty(0)
    # holds the event for all the functions ran with Clock
    event_for_clock_scheduling = None

    def __init__(self, **kwargs):

        super(GameWindow, self).__init__(**kwargs)
        self.card_deck = [i+1 for i in range(52)]
        self.players = [Player() for i in range(4)]
      
        # initial distribution of cards at the beginning of game 
        count = 0

        for player in self.players:
            self.add_widget(player)

            # if count == 0:
            #     player.player_cards = [27,28,29,30,44]
            #     for card in player.player_cards:
            #         self.card_deck.remove(card)
            #     count+=1
            #     continue
            # if count == 1:
            #     player.player_cards = [7]
            #     for card in player.player_cards:
            #         self.card_deck.remove(card)
            #     count+=1
            #     continue

            for i in range(7):
                card = random.choice(self.card_deck)
                self.card_deck.remove(card)
                player.add_card(card)
            
            count+=1

        self.add_widget(Touch())
        self.game_log = ScrolllabelLabel()
        self.add_widget(self.game_log)
        self.display_cards()
        self.number_of_cards_left = len(self.card_deck)
        self.start_game()

    def display_cards(self):

        for i in range(4):
            self.players[i].display_card(i)

        self.trash_pile_card = Image(source='./cards/back.png', size_hint_y=0.2, pos_hint={'x': 0.1, 'y':0.5})
        self.add_widget(self.trash_pile_card)

    def start_game(self):

        card = random.choice(self.card_deck)
        self.trash_pile_card.source = cardnum_to_card_image_path(card)
        self.trash_pile_card_num = card
        self.card_deck.remove(card)
        self.turn = 0
        self.check_for_thank_yous_count = 1
        self.game_over = False
        self.took_first_card = False
        self.buttons_visible = True
        self.game_log.game_log += "Player 0's turn\n"
        print('-------------------------------------------', 'Starting Turn number', '0', '-------------------------------------------')

    def verify_meld(self):

        if is_meld_valid(self.cards_currently_selected):
            game_log_string = "Player 0 melded " + str(self.cards_currently_selected) + "\n"
            self.game_log.game_log += game_log_string

            print('Player 0 melded', self.cards_currently_selected)
            
            for count, card in enumerate(self.cards_currently_selected):
                self.cards_currently_selected[count] = cardstr_to_cardnum(self.cards_currently_selected[count])
                self.players[0].remove_card(self.cards_currently_selected[count])

            copy_cards_currently_selected = list(self.cards_currently_selected)
            copy_cards_currently_selected.sort()
            self.players[0].player_melded_cards.append(copy_cards_currently_selected)
            self.players[0].display_melded_cards(0)
            self.cards_currently_selected.clear()
            self.refresh_cards(0)

        else:
            # needs to have melded before adding to other combinations 
            if len(self.players[0].player_melded_cards) == 0: 
                print('Add failed. Has to meld own cards first before adding')
                return

            # checking for all 4 players' melded combinations to see if there is anything to add to 
            check_meld_turn = 0
            while check_meld_turn < 4:
                valid, melded_cards_index = is_add_valid(self.cards_currently_selected, self.players[check_meld_turn].player_melded_cards) 
                
                if (valid): 
                    game_log_string = "Player 0 added " + self.cards_currently_selected[0] + " to Player " + str(check_meld_turn) + "\n"
                    self.game_log.game_log += game_log_string
                    print('Player 0 added', self.cards_currently_selected, 'to Player', check_meld_turn)
                    for card in self.cards_currently_selected:             
                        card_num = cardstr_to_cardnum(card)
                        self.players[0].remove_card(card_num)
                        self.players[check_meld_turn].player_melded_cards[melded_cards_index].append(card_num)
                        self.players[check_meld_turn].player_melded_cards[melded_cards_index].sort()
                        self.refresh_cards(0)

                    self.cards_currently_selected.clear()
                    self.players[check_meld_turn].display_melded_cards(check_meld_turn)
                    self.update_melds(check_meld_turn)
                    break

                check_meld_turn += 1

        if self.check_for_game_over(0, False): return
        
            
    def end_turn(self, turn_num):
        
        if len(self.card_deck) == 0: self.card_deck_empty()

        if self.game_over: return

        if turn_num != 0:
            card = self.players[turn_num].player_cards[0]
            self.players[turn_num].remove_card(card)
            self.trash_pile_card.source = cardnum_to_card_image_path(card)
            self.trash_pile_card_num = card
            if self.check_for_game_over(turn_num, False): return 
            game_log_string = "Player " + str(turn_num) + " threw away " + str(cardnum_to_cardstr(card)) + "\n"
            self.game_log.game_log += game_log_string
            print('-------------------------------------------', 'Ending Turn number', turn_num, '-------------------------------------------')
            self.check_for_thank_yous_count = 1
            self.event_for_clock_scheduling = Clock.schedule_interval(partial(self.check_for_thank_yous, (turn_num + self.check_for_thank_yous_count) % 4, turn_num), 0.1) 
            return 

        # if the card selected to end the turn isn't one card
        if not is_end_turn_valid(self.cards_currently_selected): return 

        card_num = cardstr_to_cardnum(self.cards_currently_selected[0])
        self.players[0].remove_card(card_num)
        self.trash_pile_card.source = cardnum_to_card_image_path(card_num)
        self.trash_pile_card_num = card_num
        if self.check_for_game_over(turn_num, False): return
        self.refresh_cards(0)
        self.buttons_visible = False
        self.took_first_card = False
        game_log_string = "Player 0 threw away " + str(cardnum_to_cardstr(card_num)) + "\n"
        self.game_log.game_log += game_log_string
        print('-------------------------------------------', 'Ending Turn number', turn_num, '-------------------------------------------')
        self.check_for_thank_yous_count = 1
        self.event_for_clock_scheduling = Clock.schedule_interval(partial(self.check_for_thank_yous, (turn_num + self.check_for_thank_yous_count) % 4, turn_num), 0.1) 

    def draw_card(self, player):

        self.took_first_card = True
        self.cards_currently_selected.clear()
        random_card = random.choice(self.card_deck)
        player.add_card(random_card)
        self.card_deck.remove(random_card)
        self.number_of_cards_left = len(self.card_deck)
        self.refresh_cards(0)

    def refresh_cards(self, player_number):

        for widget in self.widgets_for_player_cards[player_number]:
            self.remove_widget(widget)

        self.widgets_for_player_cards[player_number].clear()        
        self.players[player_number].display_card(player_number)

    def update_melds(self, player_number):

        for widget in self.widgets_for_player_melds[player_number]:
            self.remove_widget(widget)

        self.widgets_for_player_melds[player_number].clear()        
        self.players[player_number].display_melded_cards(player_number)

    def check_for_thank_yous(self, thank_you_turn_num, actual_turn_num, *largs):

        self.event_for_clock_scheduling.cancel()

        if thank_you_turn_num != 0:
            if self.players[thank_you_turn_num].check_for_thank_yous(thank_you_turn_num): return 
            self.check_for_thank_yous_count +=  1
            if self.check_for_thank_yous_count != 4: self.event_for_clock_scheduling = Clock.schedule_interval(partial(self.check_for_thank_yous, (actual_turn_num + self.check_for_thank_yous_count) % 4, actual_turn_num), 0.1) 
            else:
                self.turn += 1
                if self.turn == 4:
                    self.turn = 0
                    self.buttons_visible = True
                    self.took_first_card = False
                    return

                self.players[self.turn].player_turn(self.turn)

        else:
            print('Checking thank you for turn 0')
            self.deciding_thank_you = True
            self.response_for_thank_you = False
            self.buttons_visible = True
            self.event_for_clock_scheduling = Clock.schedule_interval(partial(self.set_deciding_thank_you, thank_you_turn_num, actual_turn_num), 0.1)

    def set_deciding_thank_you(self, thank_you_turn_num, actual_turn_num, *largs):
        
        if not self.deciding_thank_you:
            self.event_for_clock_scheduling.cancel()
            if self.response_for_thank_you: return
            self.check_for_thank_yous_count +=  1
            if self.check_for_thank_yous_count != 4: self.event_for_clock_scheduling = Clock.schedule_interval(partial(self.check_for_thank_yous, (actual_turn_num + self.check_for_thank_yous_count) % 4, actual_turn_num), 0.1) 
            else: 
                self.turn += 1
                if self.turn == 4:
                    self.turn = 0
                    self.buttons_visible = True
                    self.took_first_card = False
                    return

                self.players[self.turn].player_turn(self.turn)

    def thank_you(self):

        self.players[0].add_card(self.trash_pile_card_num)
        if not self.players[0].decide_can_meld(0, True):
            print('Can not say thank you since there are no possible combos')
            self.players[0].remove_card(self.trash_pile_card_num)
            return 
        game_log_string = "Player 0 said thank you to " + str(cardnum_to_cardstr(self.trash_pile_card_num)) + "\n"
        self.game_log.game_log += game_log_string
        print('Player 0 can say thank you to', self.trash_pile_card_num)

        self.response_for_thank_you = True
        self.took_first_card = True
        self.turn = 0
        self.cards_currently_selected.clear()
        self.refresh_cards(0)
        self.trash_pile_card.source = './cards/back.png'
        self.trash_pile_card_num = None
        self.deciding_thank_you = False

    def pass_for_thank_you(self):

        self.deciding_thank_you = False
        self.buttons_visible = False 
      
    def exit_pop(self, *kwargs):
        # self.root.current = 'Title Window'
        print('Exiting Pop Up')
        self.parent.current = 'Title Window'
        self.clear_widgets()
        self.__init__()

    def check_for_game_over(self, turn_num, no_more_cards):

        if len(self.players[turn_num].player_cards) == 0 or no_more_cards:
            print('Game over. Player', turn_num, 'won!')
            game_over_message = f'Game over. Player {str(turn_num)} won!'

            pop_up = PopUpWindow(game_over_message)
            button_to_close = Button(text='Return to title page.', size_hint=(0.8, 0.2), pos_hint={'x':0.1, 'y':0.1})
            pop_up.add_widget(button_to_close)
            pop_up_window = Popup(title='Game Over', auto_dismiss=False, content=pop_up, size_hint=(0.5,0.5))
            button_to_close.bind(on_press=pop_up_window.dismiss)
            button_to_close.bind(on_press=self.exit_pop)

            pop_up_window.open()
            self.game_over = True

            return True
        else: return False

    def card_deck_empty(self):

        final_scores = []
        for player in self.players:
            scores_for_player = 0
            for card in player.player_cards:
                scores_for_player += (card % 13)
            
            final_scores.append(scores_for_player)
        
        winner = -1
        min_score = sys.maxsize
        for index, score in enumerate(final_scores):
            if (score < min_score):
                min_score = score
                winner = index 

        self.check_for_game_over(winner, True)



            


    
class HoolaApp(App):
    
    def build(self):
        kv = Builder.load_file('hoola.kv')
        return kv

if __name__ == '__main__':
    HoolaApp().run()