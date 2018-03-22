import re

flag = ''

seq = ('745,6A0,7F5,7BE,6AB,837,6C1,75B,695,6CC,6D7,766,6ED,6B6,821,68A,703,72F,800,73A,724,7D4,771,77C,6F8,842,750,792,79D,7A8,70E,7B3,7C9,7DF,7EA,719,80B,816,787,82C,6E2').lower().split(',')

with open('table', 'r') as f:
	table = ''.join(f.readlines())

	for idx in seq:
		res = table.find('$', table.find(str(idx)))
		flag += chr(int(table[res+3:res+5],16))

print '[*] flag :', flag[:33]+flag[34:]
