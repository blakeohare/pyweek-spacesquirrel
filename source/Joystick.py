"""
config is a dictionary of button types as strings to their configuration
configuration entries per button are in the following formats:

BUTTON:
('B', index)
HAT:
('H', index, 0 or 1 for the ordinate, True for positive sign)
AXIS:
('A', index, True for positive sign)
"""

cached_joysticks = {} # NAME to CONFIGURATION

previous_active_joystick = None
joysticks_present = {} # NAME to INDEX
joystick_instances = [] # INDEX to INSTANCE

JOYSTICK_BUTTON_ORDER = 'A B up down left right start'.split(' ')
#def get_joystick_config(

def configureJoysticksFromFile():
	if os.path.exists('js_cache.txt'):
		c = open('js_cache.txt', 'rt')
		t = trim(c.read()).split('\n')
		c.close()
		configs = {}
		first = True
		active = None
		for line in t:
			if first:
				if len(line) > 0:
					active = line
				first = False
			parts = line[:-1].split('|')
			if len(parts) < 8:
				continue
			cfgs = []
			cfgs += [('A', parts[0])]
			cfgs += [('B', parts[1])]
			cfgs += [('up', parts[2])]
			cfgs += [('down', parts[3])]
			cfgs += [('left', parts[4])]
			cfgs += [('right', parts[5])]
			cfgs += [('start', parts[6])]
			name = '|'.join(parts[7:])
			
			configs[name] = {}
			ignoreMe = False
			for i in range(len(cfgs)):
			
				button = cfgs[i][0]
				cfg = cfgs[i][1].split('^')
				type = cfg[0]
				if type == 'B': # button
					num = int(cfg[1])
					cfg = ('B', num)
				elif type == 'H': # hat
					num = int(cfg[1])
					ordinate = int(cfg[2])
					positive = cfg[3] == '+'
					cfg = ('H', num, ordinate, positive)
				elif type == 'A':
					num = int(cfg[1])
					positive = cfg[2] == '+'
					cfg = ('A', num, positive)
				else:
					ignoreMe = True
					break
					# uhhh....
				
				
				configs[name][button] = cfg
			if ignoreMe:
				configs.pop(name)
			else:
				cached_joysticks[name] = configs[name]
		
		if cached_joysticks.get(active, None) != None:
			global previous_active_joystick
			previous_active_joystick = active
		

def getJoysticksPresent():
	for i in range(pygame.joystick.get_count()):
		js = pygame.joystick.Joystick(i)
		js.init()
		name = js.get_name()
		joysticks_present[name] = i
		joystick_instances.append(js)



BUTTONS = 'A B up down left right start'.split(' ')

def set_active_joystick(name):
	global active_joystick
	active_joystick = name

active_joystick = None # joystick NAME
active_joystick_snapshot = {}

for button in BUTTONS:
	active_joystick_snapshot[button] = False

names_cached = {}
def get_joystick_manifest():
	value = names_cached.get('value')
	if value == None:
		value = []
		for js in joystick_instances:
			value.append(js.get_name())
		names_cached['value'] = value
	return value
		

def poll_active_joystick(events_out, pressedActions):
	if active_joystick == None:
		return
	
	name = active_joystick
	index = joysticks_present.get(name)
	if index == None or len(joystick_instances) <= index:
		return
	ajs = active_joystick_snapshot
	js = joystick_instances[index]
	config = cached_joysticks[name]
	for button in JOYSTICK_BUTTON_ORDER:
		cfg = config[button]
		type = cfg[0]
		if type == 'B':
			pressed = not not js.get_button(cfg[1])
			if ajs[button] != pressed:
				ajs[button] = pressed
				events_out.append(MyEvent(button, pressed))
				pressedActions[button] = pressed
		elif type == 'H':
			state = js.get_hat(cfg[1])[cfg[2]]
			if cfg[3]:
				pressed = state == 1
			else:
				pressed = state == -1
			if ajs[button] != pressed:
				ajs[button] = pressed
				events_out.append(MyEvent(button, pressed))
				pressedActions[button] = pressed
		elif type == 'A':
			state = js.get_axis(cfg[1])
			if cfg[2]:
				pressed = state > 0.5
			else:
				pressed = state < -0.5
			if ajs[button] != pressed:
				ajs[button] = pressed
				events_out.append(MyEvent(button, pressed))
				pressedActions[button] = pressed
		else: pass # Destroy the universe and start over. Or just ignore.

def serialize_joystick_config():
	output = []
	if active_joystick == None:
		output.append('')
	else:
		output.append(active_joystick)
	for key in cached_joysticks.keys():
		line = []
		config = cached_joysticks[key]
		for button in 'A B up down left right start'.split(' '):
			cfg = config[button]
			if cfg[0] == 'B':
				line.append('B^' + str(cfg[1]))
			elif cfg[0] == 'H':
				line.append('H^' + str(cfg[1]) + '^' + str(cfg[2]) + '^' + str('+' if cfg[3] else '-'))
			elif cfg[0] == 'A':
				line.append('A^' + str(cfg[1]) + '^' + str('+' if cfg[2] else '-'))
		line.append(key)
		line.append('')
		
		output.append('|'.join(line))
	output = '\n'.join(output)
	c = open('js_cache.txt', 'wt')
	c.write(output)
	c.close()