import pandas as pd
import pymem

pm = pymem.Pymem('MonsterHunterWorld.exe')

base_offset = 0x5013950
slot_offset = 0x26CC00
monster_offset = 0xF4EA8
weapon_offset = 0x148CB4
endemic_life_offset = 0xF6F28

base_address = pm.base_address + base_offset

slot = 1
gSave = 0
gSaveMon = 0
gSaveWeap = 0
svData = 0

rcx = pm.read_longlong(base_address)
rcx = pm.read_longlong(rcx + 0xA8)
rdx = slot_offset * (slot - 1)
rcx += rdx

gSave = rcx
gSaveMon = rcx + monster_offset
gSaveWeap = rcx + weapon_offset
svData = rcx + endemic_life_offset

data = {}


def read_pointer_var(var: str, base_address: int, offsets: list[int], var_type: str, length: int = 100):
	address = base_address

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
			value = pm.read_string(final_address, length)
		case 'binary':
			if not 0 <= length <= 7:
				raise ValueError("Bit index for 'binary' must be between 0 and 7.")
			byte_value = pm.read_bytes(final_address, 1)
			value = byte_value[0] >> length & 1
		case _:
			raise ValueError(f"Unsupported variable type: {var_type}")

	data.update({var: value})


pointers = [
	('Hunter Name', gSave, [0x50], 'string', 16),
	('Hunter Rank', gSave, [0x90], 'int'),
	('Zenny', gSave, [0x94], 'int'),
	('Research Points', gSave, [0x98], 'int'),
	('Hunter Rank Experience', gSave, [0x9C], 'int'),
	('Play Time (s)', gSave, [0xA0], 'int'),
	('Master Rank', gSave, [0xD4], 'int'),
	('Master Rank Experience', gSave, [0xD8], 'int'),
	('Unity', gSave, [0x16E248], 'int'),
]


for pointer in pointers:
	read_pointer_var(*pointer)

df = pd.DataFrame.from_records(data, index=['Value']).T
df.reset_index(inplace=True, names='Variable')
df.to_csv(r'processing/raw_iceborne.tsv', sep='\t', index=False)