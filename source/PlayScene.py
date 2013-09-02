class PlayScene:
	def __init__(self, map, startCol, startRow):
		self.next = self
		self.flags = ''
		if not map.endswith('.map'):
			map += '.map'
		mapParser = MapParser(map)
		map = mapParser.parse()
		
		self.cols = map.width
		self.rows = map.height
		self.upper = map.upper
		self.lower = map.lower
		self.side = map.side
		
		self.tiles = makeGrid(self.cols, self.rows)
		
		doorTiles = []
		
		y = 0
		while y < self.rows:
			x = 0
			while x < self.cols:
				
				t = Tile(self.lower[x][y], self.upper[x][y], x, y)
				self.tiles[x][y] = t
				if t.isDoor:
					doorTiles.append((str(x) + '|' + str(y), t))
				x += 1
			y += 1
		
		doorLookup = {}
		for door in map.doors:
			doorLookup[str(door.sx) + '|' + str(door.sy)] = door
		
		for doorTile in doorTiles:
			dk = doorTile[0]
			door = doorLookup.get(dk, None)
			if door != None:
				doorTile[1].door = door
				doorTile[1].collisions = []
		
		self.cameraX = 0
		self.cameraY = 0
		
		self.player = Sprite('player_' + ('over' if self.side else 'side'), startCol * 16 + 8, startRow * 16 + 8)
		self.sprites = [self.player]
		
	def processInput(self, events, pressed):
		if self.side:
			print("TODO: side scroller part")
			z = 1 / 0
		else:
			v = 3
			dx = 0
			dy = 0
			
			if pressed['left']:
				dx = -v
			elif pressed['right']:
				dx = v
				
			if pressed['up']:
				dy = -v
			elif pressed['down']:
				dy = v
				
			self.player.dx = dx
			self.player.dy = dy
	
	def update(self):
		for sprite in self.sprites:
			sprite.update(self)
			
		player_tx = int(self.player.modelX / 16)
		player_ty = int(self.player.modelY / 16)
		activeTile = self.tiles[player_tx][player_ty]
		if activeTile.door != None:
			door = activeTile.door
			self.next = PlayScene(door.target, door.tx, door.ty)
	
	def render(self, screen, rc):
		screen.fill((0, 0, 0))
		
		colStart = 0
		colEnd = self.cols - 1
		
		rowStart = 0
		rowEnd = self.rows - 1
		
		offsetX = -(self.player.x - 128)
		offsetY = -(self.player.y - 112)
		
		if offsetX > 0: offsetX = 0
		if offsetY > 0: offsetY = 0
		
		right = -(self.cols * 16 - 256)
		if offsetX < right: offsetX = right
		
		bottom = -(self.rows * 16 - 224)
		if offsetY < bottom: offsetY = bottom
		
		if self.cols * 16 < 256:
			offsetX = (256 - self.cols * 16) // 2
		if self.rows * 16 < 224:
			offsetY = (224 - self.rows * 16) // 2
		
		row = rowStart
		while row <= rowEnd:
			col = colStart
			while col <= colEnd:
				
				tile = self.lower[col][row]
				if tile != None:
					screen.blit(tile.getImage(rc), (col * 16 + offsetX, row * 16 + offsetY))
				tile = self.upper[col][row]
				if tile != None:
					screen.blit(tile.getImage(rc), (col * 16 + offsetX, row * 16 + offsetY))
				
				
				col += 1
			row += 1
		
		for sprite in self.sprites:
			sprite.render(screen, offsetX, offsetY, rc)