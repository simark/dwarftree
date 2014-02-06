from dwarfmodel import ChildrenGroup, DwarfModelBuilder
import sys
from elftools.elf.elffile import ELFFile

def print_rec(elem, tabs = ""):
	print("%s%s" % (tabs, elem.name))

	tabs += "  "

	for group in elem.children_groups:
		children_list = elem.children_groups[group]
		if group is not None:
			print("%s%s:" % (tabs, ChildrenGroup.name(group)))
		else:
			print("%s%s:" % (tabs, "Others"))
		for child in children_list:
			print_rec(child, tabs)


if __name__ == "__main__":
	filename = sys.argv[1]

	with open(filename, 'rb') as f:
		elf = ELFFile(f)

		if not elf.has_dwarf_info():
			print("%s has no dwarf info." % filename)
			sys.exit(1)


		di = elf.get_dwarf_info()

		builder = DwarfModelBuilder(di)
		root_elem = builder.build()
		print_rec(root_elem)
