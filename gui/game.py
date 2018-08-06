


class Settlement():
    def __init__(self, name,pop, parent, player_id=0):
        self.name = name
        self.pop = pop
        self.pop_int = int(self.pop)
        self.parent = parent
        self.player_id = player_id


    def display(self):
        #Note that this will always be shown in the smae panel
        #gui.change_label_text('Data', 'pop', self.pop_int)
        # TODO this is clumsy, I should just remake the Data panel with a new settlement
        self.parent.gui.change_label_text(self.parent.settlement_panel_name, 'name', self.name)
        self.parent.gui.change_label_text(self.parent.settlement_panel_name, 'pop', self.pop_int)
        print(f'Settlement {self.name}, {self.pop_int} pop, player {self.player_id}')


    def update(self, time):
        self.pop += time * self.pop * 2.78 ** -10.5
        self.pop_int = int(self.pop)


class Game:
    def __init__(self, gui, settlement_panel_name='Data'):
        self.gui = gui
        self.settlement_panel_name = settlement_panel_name

        self.settlements = {}
        self.settlement_names = []
        self.cur_settlement = None
        self.time_increment = 30
        self.time_increments = ['5s', '30s', '2m', '5m', '20m', '1h', '3h', '6h', '1d', '2d', '5d', '30d']

    def add_settlement(self, name, pop, player_id=0):
        self.settlements[name] = (Settlement(name, pop, self, player_id))
        self.settlement_names.append(name)
        self.cur_settlement = name # The button is not tied to this on startup

    def display_settlement(self, name):
        self.cur_settlement = name
        self.settlements[name].display()



    def update(self):
        for settlement in self.settlement_names:
            self.settlements[settlement].update(30)
        print('Got to update30')
        self.settlements[self.cur_settlement].display()

    def set_time_increment(self, inc):
        self.time_increment = inc





