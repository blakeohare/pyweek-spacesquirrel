
#arc = adjusted render counter (slowed down for animation frames, so I don't have to do rc = (rc // 4) to slow things down
def SPRITE_renderPlayerOver(sprite, scene, screen, offsetX, offsetY, arc):
	left = sprite.x + offsetX - 8
	top = sprite.y + offsetY - 8
	width = 16
	height = 16
	if scene.side:
		top -= 16
		height = 32
	
	if scene.side:
		base = 'basic' if scene.hasAtmosphere else 'space'
		moving = sprite.moving
		if sprite.cling:
			path = base + '_climb_'
			if moving:
				path += '1232'[arc % 4]
			else:
				path += '2'
		else:
			path = base + '_'
			if moving:
				# TODO: running, cut RC in half
				path += '1213'[arc % 4]
			else:
				path += '1'
		if sprite.damageDir != None:
			dir = sprite.damageDir
		else:
			dir = sprite.lastDirection
		reverse = dir == 'left'
		
		x = left
		y = top
		if sprite.deathState != None and sprite.deathState != 'fall':
			if sprite.deathState == 'collapse':
				img = getImage('sprites/' + base + '_death.png')
				top += 16
				left -= 8
			elif sprite.deathState == 'lava':
				img = pygame.Surface((16, 32))
				img.fill((0, 0, 0))
		else:
			if sprite.sprinkle:
				img = getImage('sprites/space_sprinkle.png')
				left = left + 16 - img.get_width()
			elif reverse:
				img = getBackwardsImage('sprites/' + path +'.png')
			else:
				img = getImage('sprites/' + path +'.png')
				left = left + 16 - img.get_width()
			
	else:
		counter = '1232'[arc % 4] if sprite.moving else '2'
		dir = sprite.lastDirection
		reverse = False
		if dir == 'left':
			reverse = True
			dir = 'right'
		path = 'sprites/space_overworld_' + dir + '_' + counter + '.png'
		img = getBackwardsImage(path) if reverse else getImage(path) 
	screen.blit(img, (left, top))
