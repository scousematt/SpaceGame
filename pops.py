'''
So, this is colonization but set in space
'''
import random


class Pop:
    def __init__(self):
        self.generate()

    def generate(self):
        culture = ['English', 'French', 'German', 'American', 'Russian', 'Chinese']
        religion = ['Christian', 'Muslim', 'Athiest', 'Shintist', 'Hindu']
        types = ['Unemployed', 'Farmer', 'Labourer', 'Soldier', 'Hydroponics', 'Technician', 'Academican', 'Elite', 'Banker']

        self.number = random.randint(10000)
        self.type = types[random.randint(len(types))-1]
        self.culture = culture[random.randint(len(culture)-1)]
        self.religion = religion[random.randint(len(religion) - 1)]
        self.liberalism = random.randint(100)
        self.selfishness = random.randint(100)
        self.militancy = random.randint(100)
        self.wealth = random.randint(100)

    def update(self):
        # What gets updated? the population will change over time
        # Members of the pop can evolve or devolve depending on mood / wealth
        if self.wealth > 100:
            # a % will change, farmer to hydroponics
            # labourer to technician
            # soldier to elite
            pass
        elif self.wealth > 250:
            pass
            # change a % to banker
        pass