GO_TO_TITLE = True

class OpeningScene:
	def __init__(self):
		if GO_TO_TITLE:
			self.next = TitleScene()
			self.mode = None
			self.flags = ''
			self.fade = 0
			self.mode_counter = 0
		else:
			self.mode = 'open'
			self.ch3 = [
				' XXX  X  X   XXX ',
				'XX XX X  X  X   X',
				'X     X  X      X',
				'X     XXXX    XX ',
				'X     X  X      X',
				'XX XX X  X  X   X',
				' XXX  X  X   XXX '
				]
			self.logo = [
				'TTTTT TTTTT  TTT  T     T       N   N NNNN    NNNN  NNNN  NNNNN  NNN  NNNNN N   N NNNNN  NNN ',
				'  T   T     T   T TT   TT       NN  N N   N   N   N N   N N     N   N N     NN  N   N   N   N',
				'  T   T     T   T T T T T       N N N N   N   N   N N   N N     N     N     N N N   N   N    ',
				'  T   TTT   TTTTT T  T  T       N  NN NNNN    NNNN  NNNN  NNN    NNN  NNN   N  NN   N    NNN ',
				'  T   T     T   T T     T       N   N N       N     N N   N         N N     N   N   N       N',
				'  T   T     T   T T     T       N   N N       N     N  N  N     N   N N     N   N   N   N   N',
				'  T   TTTTT T   T T     T       N   N N       N     N   N NNNNN  NNN  NNNNN N   N   N    NNN ',
			]
			self.next = self
			self.flags = 'W'
			static = pygame.Surface((120, 120))
			self.scrolly = pygame.Surface((WIDTH, 5))
			black = (0, 0, 0)
			white = (255, 255, 255)
			self.dark = pygame.Surface((WIDTH, HEIGHT)).convert()
			self.dark.fill((0, 0, 0))
			
			dr = pygame.draw.rect
			pr = pygame.Rect
			e = 0
			y = 0
			self.fade = 0
			colors = [black, white] * (120 * 60)
			random.shuffle(colors)
			i = 0
			while y < 120:
				x = 0
				while x < 120:
					dr(static, colors[i], pr(x, y, 2, 2))
					i += 1
					x += 1
				y += 1
			self.static = static
			self.mode_counter = 0
		
	def processInput(self, events, pressedKeys):
		for event in events:
			
			if self.mode == 'open':
				if event.down and event.action == 'start':
					self.mode = 'starting'
					self.mode_counter = 0
			
	def update(self):
		self.fade += 1
		self.mode_counter += 1
		if self.mode == 'starting' and self.mode_counter > 20:
			self.next = TitleScene()
		if self.mode == 'open':
			if self.mode_counter > 200:
				self.mode = 'starting'
				self.mode_counter = 0
	
	def render(self, screen, renderCounter):
		if self.mode == 'starting':
			if self.mode_counter < 10:
				screen.fill((255, 80, 255))
			else:
				screen.fill((200, 200, 200))
		elif self.mode == 'open':
			left = -random.random() * 120
			top = -random.random() * 120
			y = top
			while y < HEIGHT:
				x = left
				while x < WIDTH:
					screen.blit(self.static, (x, y))
					x += 120
				y += 120
			
			self.scrolly.blit(screen, (0, 0))
			
			for i in range(5):
				y = (renderCounter * 2 + 10 * i + 300) % HEIGHT
				screen.blit(self.scrolly, (0, y))
				
			width = len(self.ch3[0])
			height = len(self.ch3)
			
			y = 0
			while y < height:
				x = 0
				while x < width:
					if self.ch3[y][x] != ' ':
						pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(20 + x * 8, 20 + y * 8, 8, 8))
					x += 1
				y += 1
			
			width = len(self.logo[0])
			height = len(self.logo)
			y = 0
			while y < height:
				x = 0
				while x < width:
					if self.logo[y][x] != ' ':
						pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(20 + x * 8, 250 + y * 8, 8, 8))
					x += 1
				y += 1
			opacity = int(self.fade * 1.5)
			if opacity > 255:
				opacity = 255
			
			v = 255 - opacity
			self.dark.set_alpha(v)
			if (v > 0):
				screen.blit(self.dark, (0, 0))
				