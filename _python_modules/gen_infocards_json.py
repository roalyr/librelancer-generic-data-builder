# Example XML schema, source: https://wiki.librelancer.net/rdl
# ================================= EXAMPLE ===================================
# <?xml version="1.0" encoding="UTF-16"?>
# <RDL>
#     <PUSH/>
#     <TRA color="green", bold="true"/>
#     <TEXT>Welcome to the Librelancer infocard example XML!</TEXT>
#     <PARA/>
#     <TEXT>This is the second paragraph</TEXT>
#     <POP/>
# </RDL>
#
# In .json it must go with escape \ character before " characters in strings
# this script does everything and gives the output infocards.json
#
# ================================ ELEMENTS ===================================
# PUSH - should be present at start of RDL
# POP  - should be present at the end of RDL
# TEXT - Adds the text between <TEXT> and </TEXT> to the rich text
#        with the current attributes.
# JUST - Changes the text alignment, in format <JUST LOC="alignment"/>
#        where accepted values are LEFT, RIGHT, CENTER
# PARA - Paragraph, adds a line break. Similar to HTML <p>
# TRA  - Text Render Attributes, use this to change the font style,
#        text colors etc. This comes in two forms, packed and unpacked.
#
# ============================== TRA UNPACKED =================================
# This is a more standard form, where the TRA tag has data
# in individual attributes. Those attributes are:
# -----------------------------------------------------------------------------
# AttrName  |                     Accepted Values
# -----------------------------------------------------------------------------
# COLOR     | fuchsia, gray, blue, green, aqua, red, yellow, white 
#           | OR #FFF, #FFFFFF hex colors
# -----------------------------------------------------------------------------
# BOLD      | TRUE, FALSE, DEFAULT
# -----------------------------------------------------------------------------
# ITALIC    | TRUE, FALSE, DEFAULT
# -----------------------------------------------------------------------------
# UNDERLINE | TRUE, FALSE, DEFAULT
# -----------------------------------------------------------------------------
# FONT      | Numeric font index
#           | Font index for both forms refers to the [TrueType]
#           | section in rich_fonts.ini. An example entry being:
#           |     [TrueType]
#           |     font = 0, Arial, 22
#           |     font = 1, Times New Roman, 35
# -----------------------------------------------------------------------------

# This is not meant to be called directly, see "build_data.py" in root directory
if __name__ != '__main__':
	#TODO sort imports
	from _python_modules.common import json_files, nl, space, divider
	from _python_modules.common import nl, eq, space, divider # for printing

# =========================== ADD FONTS IDS HERE ==============================
# Yes, they are strings. Font sizes from rich_fonts.ini
# TODO to common
	allowed_font_ids = {
		"0" : '\\"0\\"', #Size 20
		"1" : '\\"1\\"', #Size 25
		"2" : '\\"2\\"', #Size 30
		"3" : '\\"3\\"', #Size 35
	}

# ============================ DO NOT EDIT BELOW ==============================
	infocards = []

	allowed_args = ["color", "bold", "italic", "underline", "font"]
	allowed_options = {
		"true"    : '\\"true\\"',
		"false"   : '\\"false\\"',
		"default" : '\\"default\\"',
	}
	allowed_alignment = {
		"left"    : '\\"left\\"',
		"right"   : '\\"right\\"',
		"center"  : '\\"center\\"',
	}
	allowed_colors = {
		"fuchsia" : '\\"fuchsia\\"',
		"gray"    : '\\"gray\\"',
		"blue"    : '\\"blue\\"',
		"green"   : '\\"green\\"',
		"aqua"    : '\\"aqua\\"',
		"red"     : '\\"red\\"',
		"yellow"  : '\\"yellow\\"',
		"white"   : '\\"white\\"',
	}

	block_end = "/>"
	infocard_start = "<?xml version=\\\"1.0\\\" encoding=\\\"UTF-16\\\"?><RDL><PUSH/>"
	infocard_end = "<POP/></RDL>"
	text_start = "<TEXT>"
	text_end = "</TEXT>"
	tra_start = "<TRA"
	just_start = "<JUST loc="

	class infocard():
		string = ""
		
		def __init__(self, *args):
			self.string += infocard_start
			for i in range(len(args)):
				self.string += args[i].string
			self.string += infocard_end
			#print(self.string)

	class paragraph():
		string = "<PARA/>"

	class alignment():
		string = ""
		
		def __init__(self, option):
			self.string += just_start + allowed_alignment[option] + block_end

	class text():
		tras = ""
		string = ""
		
		def __init__(self, text, **kwargs):
			# Check for TRAs.
			if kwargs:
				self.tras += tra_start
				for key, value in kwargs.items():
					if key not in allowed_args:
						print("WRONG ATTRIBUTE at text block:", text)
						print("Attribute:", key)
						print("Value:", value)
						exit()
					if key == "color":
						self.tras += " " + key + eq + allowed_colors[value]
					elif key == "bold":
						self.tras += " " + key + eq + allowed_options[value]
					elif key == "italic":
						self.tras += " " + key + eq + allowed_options[value]
					elif key == "underline":
						self.tras += " " + key + eq + allowed_options[value]
					elif key == "font":
						self.tras += " " + key + eq + allowed_font_ids[value]
				self.tras += block_end
			# If no TRAs passed, just proceed without it.
			self.string = self.tras + text_start + text + text_end

# ======================== EDIT CARD TEMPLATES HERE ===========================
	def system_card(sys_name, description):
		return infocard(
		alignment("center"),
		text(sys_name, color="aqua", bold="true", font="3"),
		paragraph(),
		alignment("left"),
		text(description, color="white", bold="false", font="0"),
		)

	def star_card(star_name, description):
		return infocard(
		alignment("center"),
		text(star_name, color="yellow", bold="true", font="3"),
		paragraph(),
		alignment("left"),
		text(description, color="white", bold="false", font="0"),
		)

# ========================== EDIT INFOCARDS HERE ==============================
# Add entries to this list. Each entry is a call to a template fucntion above.
# TODO: automatically make a list from all the .ini refs.
	def make_infocards():
		global infocards
		infocards.append(
			system_card("System 01", "A test system for the generic data pack."),
		)

# =========================== CODE FOR PRINTING ===============================
	def print_infocards():
		for i in range(len(infocards)):
			print(divider)
			print(json_files["infocards"])
			print(divider)
			print("Infocard", i+1, ":")
			print(infocards[i].string)
			print()

	def write_infocards():
		make_infocards()
		infocards_json_start = "{" + nl + space +'"filetype": "infocards",'+ nl + space \
			+ '"data": {' + nl
		infocards_json_end = space + "}" + nl + "}"
		output = ""

		output += infocards_json_start
		for i in range(len(infocards)):
			output += space*2 + '"'+str(i+1)+'" : "' + infocards[i].string + '",'
			output += nl
		output += infocards_json_end

		f = open(json_files["infocards"], "w")
		f.write(output)
		f.close()
	
	
