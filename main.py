import os
import tkinter
from tkinter import ttk
from hand_evaluator import cards
from simulations import win_simulations

base_folder = os.path.dirname(__file__)

hand = []
flop = []

number_of_sim_to_run = 10000
total_number_of_players = 5

table_buttons = []


def press_card_button(card):
    card_info = list(card.split('_'))
    card_info[0] = cards[int(card_info[0])-2]
    card_info = tuple(card_info)

    all_cards = hand + flop

    def command(card=card): return press_card_button(card)

    img = globals()[f'image_{card}']

    if globals()[f'button_{card}']['state'] == 'disabled':

        if card_info == all_cards[-1]:
            if len(hand) <= 2 and card_info in hand:
                globals()[f'button_{card}']['state'] = 'normal'
                globals()[f'hand_button_{card}'].grid_forget()

                table_buttons.remove(globals()[f'hand_button_{card}'])
                hand.remove(card_info)

            elif len(flop) <= 5 and card_info in flop:
                globals()[f'button_{card}']['state'] = 'normal'
                globals()[f'flop_button_{card}'].grid_forget()

                table_buttons.remove(globals()[f'flop_button_{card}'])
                flop.remove(card_info)
    else:
        if len(hand) < 2:
            globals()[f'button_{card}']['state'] = 'disabled'
            globals()[f'hand_button_{card}'] = tkinter.Button(
                table_frame, image=img, command=command)
            globals()[f'hand_button_{card}'].grid(column=len(hand), row=0)

            table_buttons.append(globals()[f'hand_button_{card}'])
            hand.append(card_info)

        elif len(flop) < 5:
            globals()[f'button_{card}']['state'] = 'disabled'
            globals()[f'flop_button_{card}'] = tkinter.Button(
                table_frame, image=img, command=command)
            globals()[f'flop_button_{card}'].grid(
                column=(len(flop))+3, row=0)

            table_buttons.append(globals()[f'flop_button_{card}'])
            flop.append(card_info)


def press_run_stats():
    sim = win_simulations(hand, flop, number_of_sim_to_run,
                          total_number_of_players)
    won_stats_dict = sim[0]
    general_stats_dict = sim[1]

    for k, v in won_stats_dict.items():
        win_stats_tree_view.set(f'{k}', 'Percentages', f': {v}%')

    for k, v in general_stats_dict.items():
        general_stats_tree_view.set(f'{k}', 'Percentages', f': {v}%')


def press_reset():
    for button in globals()['table_buttons']:
        button.grid_forget()

    for button in buttons:
        if button['state'] == 'disabled':
            button['state'] = 'normal'

    globals()['table_buttons'] = []
    globals()['hand'] = []
    globals()['flop'] = []


def press_settings():
    # Create window
    w_width = 300
    w_height = 300
    posX = (screen_x // 2) - (w_width // 2)
    posY = ((screen_y // 2) - (w_height // 2)) - 50
    w_geo = f'{w_width}x{w_height}+{posX}+{posY}'

    settings_window = tkinter.Toplevel(root)
    settings_window.title('Simulation Settings')
    settings_window.geometry(w_geo)
    settings_window.resizable(width=False, height=False)

    # Widgets
    var = tkinter.IntVar()
    var.set(number_of_sim_to_run)
    set_number_of_sim = tkinter.Spinbox(settings_window, from_=1, to=999999, textvariable=var)
    set_number_of_players = tkinter.Scale(
        settings_window, from_=1, to=21, orient='horizontal')
    set_number_of_players.set(total_number_of_players)
    ok_button = tkinter.Button(settings_window, text='Apply Settings', command=lambda sim=set_number_of_sim,
                               p=set_number_of_players, w=settings_window: press_apply_settings(n_sim=sim, n_players=p, w=w))
    cancel_button = tkinter.Button(settings_window, text='Cancel',
                                   command=lambda: settings_window.destroy())

    # Place Widgets
    set_number_of_sim.pack(pady=50)
    set_number_of_players.pack()
    ok_button.pack(side='left', padx=10)
    cancel_button.pack(side='right', padx=10)


def press_apply_settings(n_sim, n_players, w):
    globals()['number_of_sim_to_run'] = int(n_sim.get())
    globals()['total_number_of_players'] = int(n_players.get())
    w.destroy()


WIDTH = 1400
HEIGHT = 600

root = tkinter.Tk()
root.title('Poker Simulation')

root.option_add('*tearOff', False)

menubar = tkinter.Menu(root)
settings = tkinter.Menu(menubar)
menubar.add_cascade(menu=settings, label='Settings')

settings.add_command(label='Simulation Settings', command=press_settings)

screen_x = root.winfo_screenwidth()
screen_y = root.winfo_screenheight()

posX = (screen_x // 2) - (WIDTH // 2)
posY = ((screen_y // 2) - (HEIGHT // 2)) - 50

geo = f'{WIDTH}x{HEIGHT}+{posX}+{posY}'

root.geometry(geo)
root.resizable(width=False, height=False)

mainframe = tkinter.Frame(root, width=WIDTH, height=HEIGHT)

# Mainframe Grid Config
tkinter.Grid.columnconfigure(mainframe, 0, weight=1)
tkinter.Grid.columnconfigure(mainframe, 1, weight=1)
tkinter.Grid.rowconfigure(mainframe, 0, weight=1)
tkinter.Grid.rowconfigure(mainframe, 1, weight=1)

# Frames
table_frame = tkinter.LabelFrame(mainframe, text='Table', bg='green')
cards_frame = tkinter.LabelFrame(mainframe, text='Cards', bg='YELLOW')
stats_frame = tkinter.LabelFrame(mainframe, text='Stats')

# Table Frame Grid Config
tkinter.Grid.columnconfigure(table_frame, 2, minsize=10)
tkinter.Grid.rowconfigure(table_frame, 0, weight=1, minsize=100)

suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
buttons = []


# Creating buttons for each card in cards frame
for suit in suits:
    for c in range(2, 15):
        image_path = os.path.join(base_folder, f'playing_cards/{c}_{suit}.png')
        globals()[f'image_{c}_{suit}'] = tkinter.PhotoImage(file=image_path)
        globals()[f'button_{c}_{suit}'] = tkinter.Button(cards_frame, image=globals()[f'image_{c}_{suit}'],
                                                         command=lambda card=f'{c}_{suit}': press_card_button(card))
        buttons.append(globals()[f'button_{c}_{suit}'])

# Frames Grid Placements
mainframe.pack(anchor='nw', expand=True, fill='both')

table_frame.grid(column=0, row=0, sticky='news')
cards_frame.grid(column=0, row=1, sticky='news')
stats_frame.grid(column=1, row=0, rowspan=2, sticky='news')

# Stats Frame Widgets
win_stats_tree_view = ttk.Treeview(stats_frame, columns=('Percentages'))
win_stats_tree_view.column('#0', width=150)
win_stats_tree_view.column('Percentages', anchor='w', width=150)
win_stats_tree_view.heading('#0', text='Hand')
win_stats_tree_view.heading('Percentages', text='Percentages')

general_stats_tree_view = ttk.Treeview(stats_frame, columns=('Percentages'))
general_stats_tree_view.column('#0', width=150)
general_stats_tree_view.column('Percentages', anchor='w', width=150)
general_stats_tree_view.heading('#0', text='Hand')
general_stats_tree_view.heading('Percentages', text='Percentages')

win_stats_label = tkinter.Label(
    stats_frame, text='Chance of getting a hand:', font='Helvetica 12 bold')
general_label = tkinter.Label(
    stats_frame, text='Percentage of opponents\' hands:', font='Helvetica 12 bold')
run_stats_button = tkinter.Button(
    stats_frame, text='Run Stats', command=press_run_stats)
reset_button = tkinter.Button(
    stats_frame, text='Reset Cards', command=press_reset)


# Adding names to tree view
tree_view_names = ('Games Won', 'High Card', 'One Pair', 'Two Pairs', 'Three of a Kind',
                   'Straight', 'Flush', 'Full House', 'Quads', 'Straight Flush', 'Royal Flush')

for name in tree_view_names:
    name_index = tree_view_names.index(name)
    if name_index == 0:
        win_stats_tree_view.insert('', name_index, name, text=name)
    else:
        win_stats_tree_view.insert('', name_index, name, text=name)
        general_stats_tree_view.insert('', name_index, name, text=name)


# Stats Frame Widget placement
win_stats_label.grid(column=0, row=0, columnspan=2, sticky='w')
win_stats_tree_view.grid(column=0, row=1, columnspan=2)
general_label.grid(column=0, row=5, rowspan=4, columnspan=2, sticky='w')
general_stats_tree_view.grid(column=0, row=9, columnspan=2)
run_stats_button.grid(column=0, row=10)
reset_button.grid(column=1, row=10)

# Placing previously created card buttons
counter = 0
for l in range(4):
    for i in range(13):
        buttons[counter].grid(column=i, row=l)
        counter += 1


root.config(menu=menubar)


if __name__ == '__main__':
    root.mainloop()
