
class Context:
	def __init__(self):
		self.lifemeter = 10
		self.lives = 3
		self.volcanoA = False
		self.volcanoB = False
		self.volcanoC = False
		self.balloonA = False
		self.balloonB = False
		self.balloonC = False
		self.gravity = True
	
	def convertToPassword(self):
		password = 0
		things = [
			True,
			self.gravity,
			self.volcanoA,
			not self.volcanoB,
			self.volcanoC,
			self.balloonA,
			not self.balloonB,
			self.balloonC]
			
		z = 1
		for thing in things:
			if thing:
				password += 1 << z
			z += 1
		
		output = [0, 0, 0, 0]
		for i in range(4):
			output[i] = password & 3
			password = password >> 2
		
	def convertFromPassword(self, password):
		self.gravity = (password[0] & 2) != 0
		self.volcanoA = (password[1] & 1) != 0
		self.volcanoB = (password[1] & 2) == 0
		self.volcanoC = (password[2] & 1) != 0
		self.balloonA = (password[2] & 2) != 0
		self.balloonB = (password[3] & 1) == 0
		self.balloonC = (password[3] & 2) != 0
		