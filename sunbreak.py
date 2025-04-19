import pandas as pd
import pymem
import pymem.process

pm = pymem.Pymem('MonsterHunterRise.exe')
module = pymem.process.module_from_name(pm.process_handle, "MonsterHunterRise.exe")
base = module.lpBaseOfDll

guild_card = base + 0xF6E3650
hunter_rank = base + 0xF6FA348
save_data = base + 0xF6F7438
data = {}


def read_pointer_var(var : str, base_address: int, offsets: list[int], var_type: str, string_length: int = 100):
	address = pm.read_ulonglong(base_address)

	for offset in offsets[:-1]:
		address = pm.read_ulonglong(address + offset)

	final_address = address + offsets[-1]

	match var_type:
		case 'int':
			value = pm.read_int(final_address)
		case 'uint':
			value = pm.read_uint(final_address)
		case 'float':
			value = pm.read_float(final_address)
		case 'double':
			value = pm.read_double(final_address)
		case 'bool':
			value = pm.read_bool(final_address)
		case 'long':
			value = pm.read_long(final_address)
		case 'ulong':
			value = pm.read_ulong(final_address)
		case 'longlong':
			value = pm.read_longlong(final_address)
		case 'ulonglong':
			value = pm.read_ulonglong(final_address)
		case 'string':
			value = pm.read_string(final_address, string_length)
		case _:
			raise ValueError(f"Unsupported variable type: {var_type}")
	
	data.update({var : value})


unused_pointers = [
	('Play Time', guild_card, [0x68, 0xD18], 'double'), # temporary
	('Times Liked', guild_card, [0x68, 0xD20], 'int'), # temporary
	('Total Monsters Hunted', guild_card, [0x68, 0xD24], 'int'), # temporary
	('Total Monsters Captured', guild_card, [0x68, 0xD28], 'int'), # temporary
	('Felyne Count', guild_card, [0x68, 0xD2C], 'int'), # temporary, regular version not found
	('Canyne Count', guild_card, [0x68, 0xD30], 'int'), # temporary, regular version not found
	('Total Zenny Obtained', guild_card, [0x68, 0xD34], 'int'), # temporary, regular version not found
	('Monster Most Hunted ID ???', guild_card, [0x68, 0xD38], 'int'), # temporary, regular version not found, unconfirmed
	('Endemic Lifes Encountered', guild_card, [0x68, 0xD3C], 'int'), # temporary, regular version not found
	('Monster Types Hunted', guild_card, [0x68, 0xD40], 'int'), # temporary, regular version not found
	('Usable Titles', guild_card, [0x68, 0xD44], 'int'), # temporary, regular version not found
	('Awards Owned', guild_card, [0x68, 0xD48], 'int'), # temporary, regular version not found
	('Follower Most Used ID ???', guild_card, [0x68, 0xD4C], 'int'), # temporary, regular version not found, unconfirmed
	('???', guild_card, [0x68, 0xD50], 'int'), # temporary, unconfirmed
]

pointers = [
	('Play Time', guild_card, [0x70, 0x40], 'double'),
	('Quests Completed - Shrine Ruins', guild_card, [0x70, 0xD0, 0x24], 'int'),
	('Quests Completed - Sandy Plains', guild_card, [0x70, 0xD0, 0x28], 'int'),
	('Quests Completed - Flooded Forest', guild_card, [0x70, 0xD0, 0x2C], 'int'),
	('Quests Completed - Frost Islands', guild_card, [0x70, 0xD0, 0x30], 'int'),
	('Quests Completed - Lava Caverns', guild_card, [0x70, 0xD0, 0x34], 'int'),
	('Quests Completed - Red Stronghold', guild_card, [0x70, 0xD0, 0x3C], 'int'),
	('Quests Completed - Infernal Springs', guild_card, [0x70, 0xD0, 0x44], 'int'),
	('Quests Completed - Arena', guild_card, [0x70, 0xD0, 0x48], 'int'),
	('Quests Completed - Coral Palace', guild_card, [0x70, 0xD0, 0x4C], 'int'),
	('Quests Completed - Jungle', guild_card, [0x70, 0xD0, 0x50], 'int'),
	('Quests Completed - Citadel', guild_card, [0x70, 0xD0, 0x54], 'int'),
	('Quests Completed - Forlorn Arena', guild_card, [0x70, 0xD0, 0x58], 'int'),
	('Quests Completed - Yawning Abyss', guild_card, [0x70, 0xD0, 0x5C], 'int'),
	('Times Liked', guild_card, [0x70, 0x48], 'int'),
	('Wiredashes Performed', guild_card, [0x70, 0x4C], 'int'),
	('Well-Done Steaks Cooked', guild_card, [0x70, 0x50], 'int'),
	('Great Wirebug Launch Points Discovered', guild_card, [0x70, 0x54], 'int'),
	('Golden Spiribugs Collected', guild_card, [0x70, 0x58], 'int'),
	('Hunting Helpers Collected', guild_card, [0x70, 0x5C], 'int'),
	('Shabby Canyne Saddle Time', guild_card, [0x70, 0x68], 'double'),
	('Quests Completed - Village Quests', guild_card, [0x70, 0xA0], 'int'),
	('Quests Completed - Low Rank Hub Quests', guild_card, [0x70, 0xA4], 'int'),
	('Quests Completed - High Rank Hub Quests', guild_card, [0x70, 0xA8], 'int'),
	('Quests Completed - Rampages', guild_card, [0x70, 0xAC], 'int'),
	('Quests Completed - Arena Quests', guild_card, [0x70, 0xB0], 'int'),
	('Quests Completed - Master Rank Hub Quests', guild_card, [0x70, 0xB4], 'int'),
	('Quests Completed - Support Surveys', guild_card, [0x70, 0xB8], 'int'),
	('Quests Completed - Follower Quests', guild_card, [0x70, 0xBC], 'int'),
	('Quests Completed - Anomaly Quests', guild_card, [0x70, 0xC0], 'int'),
	('Quests Completed - Anomaly Investigations', guild_card, [0x70, 0xC4], 'int'),
	('Total Monsters Hunted', guild_card, [0x70, 0xDC], 'int'),
	('Total Monsters Captured', guild_card, [0x70, 0xE0], 'int'),
	('Weapon Usage - Great Sword', guild_card, [0x70, 0x190, 0x20], 'int'),
	('Weapon Usage - Switch Axe', guild_card, [0x70, 0x190, 0x24], 'int'),
	('Weapon Usage - Long Sword', guild_card, [0x70, 0x190, 0x28], 'int'),
	('Weapon Usage - Light Bowgun', guild_card, [0x70, 0x190, 0x2C], 'int'),
	('Weapon Usage - Heavy Bowgun', guild_card, [0x70, 0x190, 0x30], 'int'),
	('Weapon Usage - Hammer', guild_card, [0x70, 0x190, 0x34], 'int'),
	('Weapon Usage - Gunlance', guild_card, [0x70, 0x190, 0x38], 'int'),
	('Weapon Usage - Lance', guild_card, [0x70, 0x190, 0x3C], 'int'),
	('Weapon Usage - Sword & Shield', guild_card, [0x70, 0x190, 0x40], 'int'),
	('Weapon Usage - Dual Blades', guild_card, [0x70, 0x190, 0x44], 'int'),
	('Weapon Usage - Hunting Horn', guild_card, [0x70, 0x190, 0x48], 'int'),
	('Weapon Usage - Charge Blade', guild_card, [0x70, 0x190, 0x4C], 'int'),
	('Weapon Usage - Insect Glaive', guild_card, [0x70, 0x190, 0x50], 'int'),
	('Weapon Usage - Bow', guild_card, [0x70, 0x190, 0x54], 'int'),
	('Hunting Log - Hunted - Great Izuchi', guild_card, [0x70, 0x138, 0xB4], 'int'),
	('Hunting Log - Captured - Great Izuchi', guild_card, [0x70, 0x150, 0xB4], 'int'),
	('Hunting Log - Anomaly Hunts - Great Izuchi', guild_card, [0x70, 0x140, 0xB4], 'int'),
	('Hunting Log - Hunted - Great Baggi', guild_card, [0x70, 0x138, 0x64], 'int'),
	('Hunting Log - Captured - Great Baggi', guild_card, [0x70, 0x150, 0x64], 'int'),
	('Hunting Log - Anomaly Hunts - Great Baggi', guild_card, [0x70, 0x140, 0x64], 'int'),
	('Hunting Log - Hunted - Kulu-Ya-Ku', guild_card, [0x70, 0x138, 0xC8], 'int'),
	('Hunting Log - Captured - Kulu-Ya-Ku', guild_card, [0x70, 0x150, 0xC8], 'int'),
	('Hunting Log - Anomaly Hunts - Kulu-Ya-Ku', guild_card, [0x70, 0x140, 0xC8], 'int'),
	('Hunting Log - Hunted - Great Wroggi', guild_card, [0x70, 0x138, 0x70], 'int'),
	('Hunting Log - Captured - Great Wroggi', guild_card, [0x70, 0x150, 0x70], 'int'),
	('Hunting Log - Anomaly Hunts - Great Wroggi', guild_card, [0x70, 0x140, 0x70], 'int'),
	('Hunting Log - Hunted - Arzuros', guild_card, [0x70, 0x138, 0x74], 'int'),
	('Hunting Log - Captured - Arzuros', guild_card, [0x70, 0x150, 0x74], 'int'),
	('Hunting Log - Anomaly Hunts - Arzuros', guild_card, [0x70, 0x140, 0x74], 'int'),
	('Hunting Log - Hunted - Lagombi', guild_card, [0x70, 0x138, 0x7C], 'int'),
	('Hunting Log - Captured - Lagombi', guild_card, [0x70, 0x150, 0x7C], 'int'),
	('Hunting Log - Anomaly Hunts - Lagombi', guild_card, [0x70, 0x140, 0x7C], 'int'),
	('Hunting Log - Hunted - Volvidon', guild_card, [0x70, 0x138, 0x80], 'int'),
	('Hunting Log - Captured - Volvidon', guild_card, [0x70, 0x150, 0x80], 'int'),
	('Hunting Log - Anomaly Hunts - Volvidon', guild_card, [0x70, 0x140, 0x80], 'int'),
	('Hunting Log - Hunted - Aknosom', guild_card, [0x70, 0x138, 0x98], 'int'),
	('Hunting Log - Captured - Aknosom', guild_card, [0x70, 0x150, 0x98], 'int'),
	('Hunting Log - Anomaly Hunts - Aknosom', guild_card, [0x70, 0x140, 0x98], 'int'),
	('Hunting Log - Hunted - Royal Ludroth', guild_card, [0x70, 0x138, 0x60], 'int'),
	('Hunting Log - Captured - Royal Ludroth', guild_card, [0x70, 0x150, 0x60], 'int'),
	('Hunting Log - Anomaly Hunts - Royal Ludroth', guild_card, [0x70, 0x140, 0x60], 'int'),
	('Hunting Log - Hunted - Barroth', guild_card, [0x70, 0x138, 0x5C], 'int'),
	('Hunting Log - Captured - Barroth', guild_card, [0x70, 0x150, 0x5C], 'int'),
	('Hunting Log - Anomaly Hunts - Barroth', guild_card, [0x70, 0x140, 0x5C], 'int'),
	('Hunting Log - Hunted - Daimyo Hermitaur', guild_card, [0x70, 0x138, 0x158], 'int'),
	('Hunting Log - Captured - Daimyo Hermitaur', guild_card, [0x70, 0x150, 0x158], 'int'),
	('Hunting Log - Anomaly Hunts - Daimyo Hermitaur', guild_card, [0x70, 0x140, 0x158], 'int'),
	('Hunting Log - Hunted - Khezu', guild_card, [0x70, 0x138, 0x30], 'int'),
	('Hunting Log - Captured - Khezu', guild_card, [0x70, 0x150, 0x30], 'int'),
	('Hunting Log - Anomaly Hunts - Khezu', guild_card, [0x70, 0x140, 0x30], 'int'),
	('Hunting Log - Hunted - Tetranadon', guild_card, [0x70, 0x138, 0x9C], 'int'),
	('Hunting Log - Captured - Tetranadon', guild_card, [0x70, 0x150, 0x9C], 'int'),
	('Hunting Log - Anomaly Hunts - Tetranadon', guild_card, [0x70, 0x140, 0x9C], 'int'),
	('Hunting Log - Hunted - Bishaten', guild_card, [0x70, 0x138, 0x94], 'int'),
	('Hunting Log - Captured - Bishaten', guild_card, [0x70, 0x150, 0x94], 'int'),
	('Hunting Log - Anomaly Hunts - Bishaten', guild_card, [0x70, 0x140, 0x94], 'int'),
	('Hunting Log - Hunted - Blood Orange Bishaten', guild_card, [0x70, 0x138, 0x180], 'int'),
	('Hunting Log - Captured - Blood Orange Bishaten', guild_card, [0x70, 0x150, 0x180], 'int'),
	('Hunting Log - Anomaly Hunts - Blood Orange Bishaten', guild_card, [0x70, 0x140, 0x180], 'int'),
	('Hunting Log - Hunted - Pukei-Pukei', guild_card, [0x70, 0x138, 0xC4], 'int'),
	('Hunting Log - Captured - Pukei-Pukei', guild_card, [0x70, 0x150, 0xC4], 'int'),
	('Hunting Log - Anomaly Hunts - Pukei-Pukei', guild_card, [0x70, 0x140, 0xC4], 'int'),
	('Hunting Log - Hunted - Jyuratodus', guild_card, [0x70, 0x138, 0xCC], 'int'),
	('Hunting Log - Captured - Jyuratodus', guild_card, [0x70, 0x150, 0xCC], 'int'),
	('Hunting Log - Anomaly Hunts - Jyuratodus', guild_card, [0x70, 0x140, 0xCC], 'int'),
	('Hunting Log - Hunted - Basarios', guild_card, [0x70, 0x138, 0x34], 'int'),
	('Hunting Log - Captured - Basarios', guild_card, [0x70, 0x150, 0x34], 'int'),
	('Hunting Log - Anomaly Hunts - Basarios', guild_card, [0x70, 0x140, 0x34], 'int'),
	('Hunting Log - Hunted - Somnacanth', guild_card, [0x70, 0x138, 0xA0], 'int'),
	('Hunting Log - Captured - Somnacanth', guild_card, [0x70, 0x150, 0xA0], 'int'),
	('Hunting Log - Anomaly Hunts - Somnacanth', guild_card, [0x70, 0x140, 0xA0], 'int'),
	('Hunting Log - Hunted - Aurora Somnacanth', guild_card, [0x70, 0x138, 0x184], 'int'),
	('Hunting Log - Captured - Aurora Somnacanth', guild_card, [0x70, 0x150, 0x184], 'int'),
	('Hunting Log - Anomaly Hunts - Aurora Somnacanth', guild_card, [0x70, 0x140, 0x184], 'int'),
	('Hunting Log - Hunted - Rathian', guild_card, [0x70, 0x138, 0x20], 'int'),
	('Hunting Log - Captured - Rathian', guild_card, [0x70, 0x150, 0x20], 'int'),
	('Hunting Log - Anomaly Hunts - Rathian', guild_card, [0x70, 0x140, 0x20], 'int'),
	('Hunting Log - Hunted - Gold Rathian', guild_card, [0x70, 0x138, 0x150], 'int'),
	('Hunting Log - Captured - Gold Rathian', guild_card, [0x70, 0x150, 0x150], 'int'),
	('Hunting Log - Anomaly Hunts - Gold Rathian', guild_card, [0x70, 0x140, 0x150], 'int'),
	('Hunting Log - Hunted - Barioth', guild_card, [0x70, 0x138, 0x58], 'int'),
	('Hunting Log - Captured - Barioth', guild_card, [0x70, 0x150, 0x58], 'int'),
	('Hunting Log - Anomaly Hunts - Barioth', guild_card, [0x70, 0x140, 0x58], 'int'),
	('Hunting Log - Hunted - Tobi-Kadachi', guild_card, [0x70, 0x138, 0xD0], 'int'),
	('Hunting Log - Captured - Tobi-Kadachi', guild_card, [0x70, 0x150, 0xD0], 'int'),
	('Hunting Log - Anomaly Hunts - Tobi-Kadachi', guild_card, [0x70, 0x140, 0xD0], 'int'),
	('Hunting Log - Hunted - Magnamalo', guild_card, [0x70, 0x138, 0x90], 'int'),
	('Hunting Log - Captured - Magnamalo', guild_card, [0x70, 0x150, 0x90], 'int'),
	('Hunting Log - Anomaly Hunts - Magnamalo', guild_card, [0x70, 0x140, 0x90], 'int'),
	('Hunting Log - Hunted - Scorned Magnamalo', guild_card, [0x70, 0x138, 0x17C], 'int'),
	('Hunting Log - Captured - Scorned Magnamalo', guild_card, [0x70, 0x150, 0x17C], 'int'),
	('Hunting Log - Anomaly Hunts - Scorned Magnamalo', guild_card, [0x70, 0x140, 0x17C], 'int'),
	('Hunting Log - Hunted - Anjanath', guild_card, [0x70, 0x138, 0xC0], 'int'),
	('Hunting Log - Captured - Anjanath', guild_card, [0x70, 0x150, 0xC0], 'int'),
	('Hunting Log - Anomaly Hunts - Anjanath', guild_card, [0x70, 0x140, 0xC0], 'int'),
	('Hunting Log - Hunted - Nargacuga', guild_card, [0x70, 0x138, 0x54], 'int'),
	('Hunting Log - Captured - Nargacuga', guild_card, [0x70, 0x150, 0x54], 'int'),
	('Hunting Log - Anomaly Hunts - Nargacuga', guild_card, [0x70, 0x140, 0x54], 'int'),
	('Hunting Log - Hunted - Lucent Nargacuga', guild_card, [0x70, 0x138, 0x164], 'int'),
	('Hunting Log - Captured - Lucent Nargacuga', guild_card, [0x70, 0x150, 0x164], 'int'),
	('Hunting Log - Anomaly Hunts - Lucent Nargacuga', guild_card, [0x70, 0x140, 0x164], 'int'),
	('Hunting Log - Hunted - Mizutsune', guild_card, [0x70, 0x138, 0x84], 'int'),
	('Hunting Log - Captured - Mizutsune', guild_card, [0x70, 0x150, 0x84], 'int'),
	('Hunting Log - Anomaly Hunts - Mizutsune', guild_card, [0x70, 0x140, 0x84], 'int'),
	('Hunting Log - Hunted - Violet Mizutsune', guild_card, [0x70, 0x138, 0x178], 'int'),
	('Hunting Log - Captured - Violet Mizutsune', guild_card, [0x70, 0x150, 0x178], 'int'),
	('Hunting Log - Anomaly Hunts - Violet Mizutsune', guild_card, [0x70, 0x140, 0x178], 'int'),
	('Hunting Log - Hunted - Goss Harag', guild_card, [0x70, 0x138, 0xB0], 'int'),
	('Hunting Log - Captured - Goss Harag', guild_card, [0x70, 0x150, 0xB0], 'int'),
	('Hunting Log - Anomaly Hunts - Goss Harag', guild_card, [0x70, 0x140, 0xB0], 'int'),
	('Hunting Log - Hunted - Garangolm', guild_card, [0x70, 0x138, 0x19C], 'int'),
	('Hunting Log - Captured - Garangolm', guild_card, [0x70, 0x150, 0x19C], 'int'),
	('Hunting Log - Anomaly Hunts - Garangolm', guild_card, [0x70, 0x140, 0x19C], 'int'),
	('Hunting Log - Hunted - Shogun Ceanataur', guild_card, [0x70, 0x138, 0x15C], 'int'),
	('Hunting Log - Captured - Shogun Ceanataur', guild_card, [0x70, 0x150, 0x15C], 'int'),
	('Hunting Log - Anomaly Hunts - Shogun Ceanataur', guild_card, [0x70, 0x140, 0x15C], 'int'),
	('Hunting Log - Hunted - Rathalos', guild_card, [0x70, 0x138, 0x28], 'int'),
	('Hunting Log - Captured - Rathalos', guild_card, [0x70, 0x150, 0x28], 'int'),
	('Hunting Log - Anomaly Hunts - Rathalos', guild_card, [0x70, 0x140, 0x28], 'int'),
	('Hunting Log - Hunted - Silver Rathalos', guild_card, [0x70, 0x138, 0x154], 'int'),
	('Hunting Log - Captured - Silver Rathalos', guild_card, [0x70, 0x150, 0x154], 'int'),
	('Hunting Log - Anomaly Hunts - Silver Rathalos', guild_card, [0x70, 0x140, 0x154], 'int'),
	('Hunting Log - Hunted - Almudron', guild_card, [0x70, 0x138, 0xA8], 'int'),
	('Hunting Log - Captured - Almudron', guild_card, [0x70, 0x150, 0xA8], 'int'),
	('Hunting Log - Anomaly Hunts - Almudron', guild_card, [0x70, 0x140, 0xA8], 'int'),
	('Hunting Log - Hunted - Magma Almudron', guild_card, [0x70, 0x138, 0x18C], 'int'),
	('Hunting Log - Captured - Magma Almudron', guild_card, [0x70, 0x150, 0x18C], 'int'),
	('Hunting Log - Anomaly Hunts - Magma Almudron', guild_card, [0x70, 0x140, 0x18C], 'int'),
	('Hunting Log - Hunted - Zinogre', guild_card, [0x70, 0x138, 0x68], 'int'),
	('Hunting Log - Captured - Zinogre', guild_card, [0x70, 0x150, 0x68], 'int'),
	('Hunting Log - Anomaly Hunts - Zinogre', guild_card, [0x70, 0x140, 0x68], 'int'),
	('Hunting Log - Hunted - Lunagaron', guild_card, [0x70, 0x138, 0x198], 'int'),
	('Hunting Log - Captured - Lunagaron', guild_card, [0x70, 0x150, 0x198], 'int'),
	('Hunting Log - Anomaly Hunts - Lunagaron', guild_card, [0x70, 0x140, 0x198], 'int'),
	('Hunting Log - Hunted - Astalos', guild_card, [0x70, 0x138, 0x174], 'int'),
	('Hunting Log - Captured - Astalos', guild_card, [0x70, 0x150, 0x174], 'int'),
	('Hunting Log - Anomaly Hunts - Astalos', guild_card, [0x70, 0x140, 0x174], 'int'),
	('Hunting Log - Hunted - Espinas', guild_card, [0x70, 0x138, 0x1A4], 'int'),
	('Hunting Log - Captured - Espinas', guild_card, [0x70, 0x150, 0x1A4], 'int'),
	('Hunting Log - Anomaly Hunts - Espinas', guild_card, [0x70, 0x140, 0x1A4], 'int'),
	('Hunting Log - Hunted - Flaming Espinas', guild_card, [0x70, 0x138, 0x1A8], 'int'),
	('Hunting Log - Captured - Flaming Espinas', guild_card, [0x70, 0x150, 0x1A8], 'int'),
	('Hunting Log - Anomaly Hunts - Flaming Espinas', guild_card, [0x70, 0x140, 0x1A8], 'int'),
	('Hunting Log - Hunted - Gore Magala', guild_card, [0x70, 0x138, 0x168], 'int'),
	('Hunting Log - Captured - Gore Magala', guild_card, [0x70, 0x150, 0x168], 'int'),
	('Hunting Log - Anomaly Hunts - Gore Magala', guild_card, [0x70, 0x140, 0x168], 'int'),
	('Hunting Log - Hunted - Chaotic Gore Magala', guild_card, [0x70, 0x138, 0x1E4], 'int'),
	('Hunting Log - Captured - Chaotic Gore Magala', guild_card, [0x70, 0x150, 0x1E4], 'int'),
	('Hunting Log - Anomaly Hunts - Chaotic Gore Magala', guild_card, [0x70, 0x140, 0x1E4], 'int'),
	('Hunting Log - Hunted - Seregios', guild_card, [0x70, 0x138, 0x170], 'int'),
	('Hunting Log - Captured - Seregios', guild_card, [0x70, 0x150, 0x170], 'int'),
	('Hunting Log - Anomaly Hunts - Seregios', guild_card, [0x70, 0x140, 0x170], 'int'),
	('Hunting Log - Hunted - Tigrex', guild_card, [0x70, 0x138, 0x50], 'int'),
	('Hunting Log - Captured - Tigrex', guild_card, [0x70, 0x150, 0x50], 'int'),
	('Hunting Log - Anomaly Hunts - Tigrex', guild_card, [0x70, 0x140, 0x50], 'int'),
	('Hunting Log - Hunted - Diablos', guild_card, [0x70, 0x138, 0x38], 'int'),
	('Hunting Log - Captured - Diablos', guild_card, [0x70, 0x150, 0x38], 'int'),
	('Hunting Log - Anomaly Hunts - Diablos', guild_card, [0x70, 0x140, 0x38], 'int'),
	('Hunting Log - Hunted - Rakna-Kadaki', guild_card, [0x70, 0x138, 0xA4], 'int'),
	('Hunting Log - Captured - Rakna-Kadaki', guild_card, [0x70, 0x150, 0xA4], 'int'),
	('Hunting Log - Anomaly Hunts - Rakna-Kadaki', guild_card, [0x70, 0x140, 0xA4], 'int'),
	('Hunting Log - Hunted - Pyre Rakna-Kadaki', guild_card, [0x70, 0x138, 0x188], 'int'),
	('Hunting Log - Captured - Pyre Rakna-Kadaki', guild_card, [0x70, 0x150, 0x188], 'int'),
	('Hunting Log - Anomaly Hunts - Pyre Rakna-Kadaki', guild_card, [0x70, 0x140, 0x188], 'int'),
	('Hunting Log - Hunted - Kushala Daora', guild_card, [0x70, 0x138, 0x44], 'int'),
	('Hunting Log - Captured - Kushala Daora', guild_card, [0x70, 0x150, 0x44], 'int'),
	('Hunting Log - Anomaly Hunts - Kushala Daora', guild_card, [0x70, 0x140, 0x44], 'int'),
	('Hunting Log - Hunted - Risen Kushala Daora', guild_card, [0x70, 0x138, 0x1CC], 'int'),
	('Hunting Log - Captured - Risen Kushala Daora', guild_card, [0x70, 0x150, 0x1CC], 'int'),
	('Hunting Log - Anomaly Hunts - Risen Kushala Daora', guild_card, [0x70, 0x140, 0x1CC], 'int'),
	('Hunting Log - Hunted - Chameleos', guild_card, [0x70, 0x138, 0x48], 'int'),
	('Hunting Log - Captured - Chameleos', guild_card, [0x70, 0x150, 0x48], 'int'),
	('Hunting Log - Anomaly Hunts - Chameleos', guild_card, [0x70, 0x140, 0x48], 'int'),
	('Hunting Log - Hunted - Risen Chameleos', guild_card, [0x70, 0x138, 0x1D0], 'int'),
	('Hunting Log - Captured - Risen Chameleos', guild_card, [0x70, 0x150, 0x1D0], 'int'),
	('Hunting Log - Anomaly Hunts - Risen Chameleos', guild_card, [0x70, 0x140, 0x1D0], 'int'),
	('Hunting Log - Hunted - Teostra', guild_card, [0x70, 0x138, 0x4C], 'int'),
	('Hunting Log - Captured - Teostra', guild_card, [0x70, 0x150, 0x4C], 'int'),
	('Hunting Log - Anomaly Hunts - Teostra', guild_card, [0x70, 0x140, 0x4C], 'int'),
	('Hunting Log - Hunted - Risen Teostra', guild_card, [0x70, 0x138, 0x1D4], 'int'),
	('Hunting Log - Captured - Risen Teostra', guild_card, [0x70, 0x150, 0x1D4], 'int'),
	('Hunting Log - Anomaly Hunts - Risen Teostra', guild_card, [0x70, 0x140, 0x1D4], 'int'),
	('Hunting Log - Hunted - Malzeno', guild_card, [0x70, 0x138, 0x194], 'int'),
	('Hunting Log - Captured - Malzeno', guild_card, [0x70, 0x150, 0x194], 'int'),
	('Hunting Log - Anomaly Hunts - Malzeno', guild_card, [0x70, 0x140, 0x194], 'int'),
	('Hunting Log - Hunted - Primordial Malzeno', guild_card, [0x70, 0x138, 0x1E0], 'int'),
	('Hunting Log - Captured - Primordial Malzeno', guild_card, [0x70, 0x150, 0x1E0], 'int'),
	('Hunting Log - Anomaly Hunts - Primordial Malzeno', guild_card, [0x70, 0x140, 0x1E0], 'int'),
	('Hunting Log - Hunted - Shagaru Magala', guild_card, [0x70, 0x138, 0x16C], 'int'),
	('Hunting Log - Captured - Shagaru Magala', guild_card, [0x70, 0x150, 0x16C], 'int'),
	('Hunting Log - Anomaly Hunts - Shagaru Magala', guild_card, [0x70, 0x140, 0x16C], 'int'),
	('Hunting Log - Hunted - Risen Shagaru Magala', guild_card, [0x70, 0x138, 0x1D8], 'int'),
	('Hunting Log - Captured - Risen Shagaru Magala', guild_card, [0x70, 0x150, 0x1D8], 'int'),
	('Hunting Log - Anomaly Hunts - Risen Shagaru Magala', guild_card, [0x70, 0x140, 0x1D8], 'int'),
	('Hunting Log - Hunted - Velkhana', guild_card, [0x70, 0x138, 0x1E8], 'int'),
	('Hunting Log - Captured - Velkhana', guild_card, [0x70, 0x150, 0x1E8], 'int'),
	('Hunting Log - Anomaly Hunts - Velkhana', guild_card, [0x70, 0x140, 0x1E8], 'int'),
	('Hunting Log - Hunted - Rajang', guild_card, [0x70, 0x138, 0x40], 'int'),
	('Hunting Log - Captured - Rajang', guild_card, [0x70, 0x150, 0x40], 'int'),
	('Hunting Log - Anomaly Hunts - Rajang', guild_card, [0x70, 0x140, 0x40], 'int'),
	('Hunting Log - Hunted - Furious Rajang', guild_card, [0x70, 0x138, 0x160], 'int'),
	('Hunting Log - Captured - Furious Rajang', guild_card, [0x70, 0x150, 0x160], 'int'),
	('Hunting Log - Anomaly Hunts - Furious Rajang', guild_card, [0x70, 0x140, 0x160], 'int'),
	('Hunting Log - Hunted - Bazelgeuse', guild_card, [0x70, 0x138, 0xD4], 'int'),
	('Hunting Log - Captured - Bazelgeuse', guild_card, [0x70, 0x150, 0xD4], 'int'),
	('Hunting Log - Anomaly Hunts - Bazelgeuse', guild_card, [0x70, 0x140, 0xD4], 'int'),
	('Hunting Log - Hunted - Seething Bazelgeuse', guild_card, [0x70, 0x138, 0x190], 'int'),
	('Hunting Log - Captured - Seething Bazelgeuse', guild_card, [0x70, 0x150, 0x190], 'int'),
	('Hunting Log - Anomaly Hunts - Seething Bazelgeuse', guild_card, [0x70, 0x140, 0x190], 'int'),
	('Hunting Log - Hunted - Wind Serpent Ibushi', guild_card, [0x70, 0x138, 0xAC], 'int'),
	('Hunting Log - Captured - Wind Serpent Ibushi', guild_card, [0x70, 0x150, 0xAC], 'int'),
	('Hunting Log - Anomaly Hunts - Wind Serpent Ibushi', guild_card, [0x70, 0x140, 0xAC], 'int'),
	('Hunting Log - Hunted - Thunder Serpent Narwa', guild_card, [0x70, 0x138, 0xB8], 'int'),
	('Hunting Log - Captured - Thunder Serpent Narwa', guild_card, [0x70, 0x150, 0xB8], 'int'),
	('Hunting Log - Anomaly Hunts - Thunder Serpent Narwa', guild_card, [0x70, 0x140, 0xB8], 'int'),
	('Hunting Log - Hunted - Narwa the Allmother', guild_card, [0x70, 0x138, 0xBC], 'int'),
	('Hunting Log - Captured - Narwa the Allmother', guild_card, [0x70, 0x150, 0xBC], 'int'),
	('Hunting Log - Anomaly Hunts - Narwa the Allmother', guild_card, [0x70, 0x140, 0xBC], 'int'),
	('Hunting Log - Hunted - Crimson Glow Valstrax', guild_card, [0x70, 0x138, 0x8C], 'int'),
	('Hunting Log - Captured - Crimson Glow Valstrax', guild_card, [0x70, 0x150, 0x8C], 'int'),
	('Hunting Log - Anomaly Hunts - Crimson Glow Valstrax', guild_card, [0x70, 0x140, 0x8C], 'int'),
	('Hunting Log - Hunted - Risen Crimson Glow Valstrax', guild_card, [0x70, 0x138, 0x1DC], 'int'),
	('Hunting Log - Captured - Risen Crimson Glow Valstrax', guild_card, [0x70, 0x150, 0x1DC], 'int'),
	('Hunting Log - Anomaly Hunts - Risen Crimson Glow Valstrax', guild_card, [0x70, 0x140, 0x1DC], 'int'),
	('Hunting Log - Hunted - Gaismagorm', guild_card, [0x70, 0x138, 0x1A0], 'int'),
	('Hunting Log - Captured - Gaismagorm', guild_card, [0x70, 0x150, 0x1A0], 'int'),
	('Hunting Log - Anomaly Hunts - Gaismagorm', guild_card, [0x70, 0x140, 0x1A0], 'int'),
	('Hunting Log - Hunted - Amatsu', guild_card, [0x70, 0x138, 0x1EC], 'int'),
	('Hunting Log - Captured - Amatsu', guild_card, [0x70, 0x150, 0x1EC], 'int'),
	('Hunting Log - Anomaly Hunts - Amatsu', guild_card, [0x70, 0x140, 0x1EC], 'int'),
	('Hunting Log - Hunted - Apex Arzuros', guild_card, [0x70, 0x138, 0x78], 'int'),
	('Hunting Log - Captured - Apex Arzuros', guild_card, [0x70, 0x150, 0x78], 'int'),
	('Hunting Log - Anomaly Hunts - Apex Arzuros', guild_card, [0x70, 0x140, 0x78], 'int'),
	('Hunting Log - Hunted - Apex Rathian', guild_card, [0x70, 0x138, 0x24], 'int'),
	('Hunting Log - Captured - Apex Rathian', guild_card, [0x70, 0x150, 0x24], 'int'),
	('Hunting Log - Anomaly Hunts - Apex Rathian', guild_card, [0x70, 0x140, 0x24], 'int'),
	('Hunting Log - Hunted - Apex Mizutsune', guild_card, [0x70, 0x138, 0x88], 'int'),
	('Hunting Log - Captured - Apex Mizutsune', guild_card, [0x70, 0x150, 0x88], 'int'),
	('Hunting Log - Anomaly Hunts - Apex Mizutsune', guild_card, [0x70, 0x140, 0x88], 'int'),
	('Hunting Log - Hunted - Apex Rathalos', guild_card, [0x70, 0x138, 0x2C], 'int'),
	('Hunting Log - Captured - Apex Rathalos', guild_card, [0x70, 0x150, 0x2C], 'int'),
	('Hunting Log - Anomaly Hunts - Apex Rathalos', guild_card, [0x70, 0x140, 0x2C], 'int'),
	('Hunting Log - Hunted - Apex Diablos', guild_card, [0x70, 0x138, 0x3C], 'int'),
	('Hunting Log - Captured - Apex Diablos', guild_card, [0x70, 0x150, 0x3C], 'int'),
	('Hunting Log - Anomaly Hunts - Apex Diablos', guild_card, [0x70, 0x140, 0x3C], 'int'),
	('Hunting Log - Hunted - Apex Zinogre', guild_card, [0x70, 0x138, 0x6C], 'int'),
	('Hunting Log - Captured - Apex Zinogre', guild_card, [0x70, 0x150, 0x6C], 'int'),
	('Hunting Log - Anomaly Hunts - Apex Zinogre', guild_card, [0x70, 0x140, 0x6C], 'int'),
]


for pointer in pointers:
	read_pointer_var(*pointer)

df = pd.DataFrame.from_records(data, index=['Value']).T
df.reset_index(inplace=True, names='Variable')
df.to_csv(r'processing/raw_sunbreak.tsv', sep='\t', index=False)