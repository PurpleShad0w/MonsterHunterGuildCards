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


read_pointer_var('Play Time', guild_card, [0x70, 0x40], 'double')


data = pd.DataFrame([[k, v] for k, v in data.items()], columns=['Variable', 'Value'])
data.to_csv(r'processing/raw_sunbreak.tsv', sep='\t', index=False)