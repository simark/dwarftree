import sys

class ChildrenGroup:
    BaseType = 0
    StructType = 1
    EnumType = 2
    ArrayType = 3
    Typedef = 4
    PointerType = 5

    names = ["Basic types", "Structure types", "Enumeration types", "Array types", "Typedefs", "Pointer types"]

    def name(group):
        return ChildrenGroup.names[group]


class Element:
    def __init__(self, name, die):
        self.name = name
        self.die = die

        # Dict ChildrenGroup -> list of children of that group
        self.children_groups = dict()

    def add_child(self, group, child_elem):
        assert(type(child_elem) == Element)
        if group not in self.children_groups:
            self.children_groups[group] = []

        self.children_groups[group].append(child_elem)

    def add_children(self, group, child_elements):
        assert(type(child_elements) == list)
        for x in child_elements:
            assert(type(x) == Element)

        if len(child_elements) == 0:
            return

        if group not in self.children_groups:
            self.children_groups[group] = []

        self.children_groups[group] += child_elements

def dp(s):
    print(s, file = sys.stderr)

def filter_children_by_tag(die, tag):
    return [x for x in die.iter_children() if x.tag == tag]

def die_get_attr(die, attr_name):
    if attr_name in die.attributes:
        return die.attributes[attr_name].value

def die_get_name(die):
    name = die_get_attr(die, 'DW_AT_name')

    if name is not None:
        name = name.decode()

    return name


class DwarfModelBuilder:
    # dwarf_info: a pyelftools DWAFRInfo object
    def __init__(self, dwarf_info):
        self.dwarf_info = dwarf_info

        # (cu, relative offset) -> type string
        # abs offset = rel offset + cu offset
        self.types = dict()

    def build(self):
        file_elem = Element("File", None)

        for cu in self.dwarf_info.iter_CUs():
            top_die = cu.get_top_DIE()

            self._types_pass(top_die)
            cu_elem = self.visit_cu(top_die)
            file_elem.add_child(None, cu_elem)

        return file_elem

    def _types_pass(self, die):
        tag = die.tag

        type_tags = ['DW_TAG_structure_type',
                     'DW_TAG_base_type',
                     'DW_TAG_typedef',
                     'DW_TAG_array_type',
                     'DW_TAG_pointer_type',
                     'DW_TAG_const_type',
                     'DW_TAG_subroutine_type',
                     'DW_TAG_volatile_type',
                     'DW_TAG_union_type']

        if tag in type_tags:
            cu = die.cu
            offset = die.offset - die.cu.cu_offset
            dp("adding type at %x" % (offset))

            assert((cu, offset) not in self.types)

            self.types[(cu, offset)] = die

        for child in die.iter_children():
            self._types_pass(child)


    def visit_cu(self, cu_die):
        name = die_get_name(cu_die)
        cu_elem = Element("Compile unit %s" % (name), cu_die)

        cu_elem.add_children(ChildrenGroup.BaseType,self.visit_children_of_tag(cu_die, 'DW_TAG_base_type', self.visit_base_type))
        cu_elem.add_children(ChildrenGroup.StructType,self.visit_children_of_tag(cu_die, 'DW_TAG_structure_type', self.visit_struct_type))
        cu_elem.add_children(ChildrenGroup.ArrayType,self.visit_children_of_tag(cu_die, 'DW_TAG_array_type', self.visit_array_type))
        cu_elem.add_children(ChildrenGroup.Typedef,self.visit_children_of_tag(cu_die, 'DW_TAG_typedef', self.visit_typedef))
        cu_elem.add_children(ChildrenGroup.PointerType,self.visit_children_of_tag(cu_die, 'DW_TAG_pointer_type', self.visit_pointer_types))

        return cu_elem

    def visit_children_of_tag(self, die, tag, callback):
        ret = []
        children_dies = filter_children_by_tag(die, tag)
        for cd in children_dies:
            ret.append(callback(cd))

        return ret

    def visit_base_type(self, base_type_die):
        name = die_get_name(base_type_die)
        elem = Element(name, base_type_die)
        return elem


    def visit_struct_type(self, struct_type_die):
        name = die_get_name(struct_type_die)
        if not name:
            name = '<anonymous>'

        elem = Element(name, struct_type_die)

        elem.add_children(None, self.visit_children_of_tag(struct_type_die, 'DW_TAG_member', self.visit_type_member))

        return elem

    def visit_type_member(self, member_type_die):
        member_name = die_get_name(member_type_die)
        member_elem = Element(member_name, member_type_die)

        return member_elem

    def visit_array_type(self, array_type_die):
        array_elem = Element("An array?", array_type_die)

        return array_elem

    def visit_typedef(self, typedef_die):
        typedef_elem = Element("A typedef?", typedef_die)

        return typedef_elem

    def visit_pointer_types(self, pointer_type_die):
        pointer_elem = Element("A pointer?", pointer_type_die)

        return pointer_elem
