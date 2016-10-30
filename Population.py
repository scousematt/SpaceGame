import random



class Planet:
	def __init__(self, numSettlements):
		self.numSettlements = numSettlements
		
		self.Settlements = []
		
		self.startup()
		
		
	def startup(self):
		for i in range(0, numSettlements):
			
			inf = 500 + random.randint(0,10) * 200
			energy = random.randint(5, 15)
			food = random.randint(5, 15)
			prod = random.randint(5, 15)
			civ = random.randint(5, 15)
			
			self.Settlements.append(Settlement(inf, energy, food, prod, civ))


class Settlement:
	def __init__(self, infrastructure, energy, food, production, civilian):
		self.infrastructure = infrastructure
		self.energy = energy
		self.food = food
		self.production = production
		self.civilian = civilian
		self.ageRanges = []
		self.name = self.getName()
		
		
	def getName(self):
		nameList = ["Alpha", "Beta", "Tanstafaal", "Aurara", "Derek's Nose", "Fairbright", \
					"Witherspoon", "Liverpool", "Widnes", "Hull", "Oregon", "France", "Glowlight", \
					"Texas", "Carrot", "Vienna", "Essex", "London", "Help", "Welcome", "Norway", \
					"Right", "Landis", "Purnell", "Noethhood", "Perfect", "Frozen", "Tangled"]
		return(nameList[random.randint(0,len(nameList)) - 1])
		
	def setup(self):
		#birthRate, deathRate, startAge, endAge, totalNumber
		#0-4
		self.ageRanges.append(AgeRange(0, 15, 0, 4, 1000))
		self.ageRanges.append(AgeRange(0, 12, 5, 9, 10000))
		self.ageRanges.append(AgeRange(15, 10, 10, 14, 10000))
		self.ageRanges.append(AgeRange(150, 8, 15, 19, 10000))
		self.ageRanges.append(AgeRange(205, 7, 20, 24, 10000))
		self.ageRanges.append(AgeRange(250, 7, 25, 29, 10000))
		self.ageRanges.append(AgeRange(175, 8, 30, 34, 10000))
		self.ageRanges.append(AgeRange(150, 9, 35, 39, 10000))
		self.ageRanges.append(AgeRange(55, 15, 40, 44, 10000))
		self.ageRanges.append(AgeRange(20, 29, 45, 49, 10000))
		self.ageRanges.append(AgeRange(0, 50, 50, 54, 10000))
		self.ageRanges.append(AgeRange(0, 60, 55, 59, 10000))
		self.ageRanges.append(AgeRange(0, 70, 60, 64, 10000))
		self.ageRanges.append(AgeRange(0, 80, 65, 69, 10000))
		self.ageRanges.append(AgeRange(0, 125, 70, 74, 10000))
		self.ageRanges.append(AgeRange(0, 250, 75, 79, 10000))
		self.ageRanges.append(AgeRange(0, 500, 80, 84, 10000))
		self.ageRanges.append(AgeRange(0, 700, 85, 89, 1000))
		self.ageRanges.append(AgeRange(0, 900, 90, 110, 10))
	
	def report(self):
		for entry in self.ageRanges:
			print ("Age " + str(entry.startAge) + " to "+ str(entry.endAge) + \
					" :" + str(int(entry.totalNumber)))
	
	def getWorkingPopulation(self):
		c = 0
		for i in range(4, 13):
			c += self.ageRanges[i].totalNumber
		return(c)
		
		
	def getTotalPopulation(self):
		c = 0
		for entry in self.ageRanges:
			c += entry.totalNumber
		return(c)
		
		
	def update(self, seconds):
		#check to see how full the settlement is
		popFactor = (10 - ( self.getTotalPopulation() / self.infrastructure * 1000 ))/10
		if self.getTotalPopulation() / (self.infrastructure * 1000) < 0.8:
			popFactor = 1
		elif self.getTotalPopulation() / (self.infrastructure * 1000) >= 0.8:
			popFactor = 1 - (self.getTotalPopulation() / (self.infrastructure * 1000))
			if popFactor < 0:
				popFactor = 0
		
		annualFactor = seconds / (365 * 24 * 3600)
		
	
		numberBirths = 0
		nextNumberChange = 0 # movement of 1/4 of pop up a group
		for ages in self.ageRanges:
			#total number of births through the population
			numberBirths += annualFactor *  popFactor *\
							(ages.birthRate / 1000) * ages.totalNumber
			
			thisNumberChange = ages.totalNumber * 0.2 * annualFactor
			
			
			ages.totalNumber -= thisNumberChange
			
			ages.totalNumber += nextNumberChange
			#deaths
			ages.totalNumber -= (ages.deathRate / 1000) * \
								annualFactor * ages.totalNumber
			 
			#amount to increase next age range
			nextNumberChange = thisNumberChange
			
		self.ageRanges[0].totalNumber += numberBirths
		
	
		
class AgeRange():
	def __init__(self, birthRate, deathRate, startAge, endAge, totalNumber):
		self.birthRate = birthRate
		self.deathRate = deathRate
		self.startAge = startAge
		self.endAge = endAge
		self.totalNumber = totalNumber
		
	
myCity = Settlement(2000, 10, 10, 10, 10)
myCity.setup()
for i in range(0, 175):
	myCity.update(31536000)   #a year
myCity.report()

print("Total Pop: " + str(int(myCity.getTotalPopulation())))
print("Working Pop: " + str(int(myCity.getWorkingPopulation())))
print("Working %: " + str((myCity.getWorkingPopulation() * 100 / myCity.getTotalPopulation())))
