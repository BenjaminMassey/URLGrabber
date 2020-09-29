
# Current version was made for the website URL:
# https://pkmncards.com/set/legendary-collection/

# The main thing to search for.
# if images on the page are like "x.com/image/y.png",
# then use "/image/"
match_phrase = "/wp-content/uploads/"

# Any phrases that the program will completely discard.
# if there are multiple versions, like there's
# "mareep480p", "mareep720p" and "mareep1080p", and you
# only want the highest res, so you put in "480p" and "720p"
ignore_phrases = [
	"312x429"
]

# Maximum number of lines to go through
# Simply used in case the loop breaks, so
# that the loop doesn't go forever. Just make
# sure timeout is larger than the number of lines
timeout = 600

# Here's the html file that you want to search through
website_file = open("site.html", "r")

output_file = open("output.txt", "w")
output_file.close()
output_file = open("output.txt", "a")

print("initialized files, starting...")

content = []
i = -1

while True:
	
	i += 1
	
	if (i % 25) == 0:
		print((i), "lines through...")
	
	if i == timeout:
		break
	
	try:
		line = website_file.readline()
	except:
		continue
	
	if not line:
		break
	
	if match_phrase in line:
		content.append(line)

website_file.close()

repeat_scrub_content = []

for line in content:

	quote_scrub_data = line.split('"')
	
	quote_scrub_content = []
	
	for datum in quote_scrub_data:
		if match_phrase in datum:
			datum = datum.replace('"', '')
			quote_scrub_content.append(datum)
			
	space_scrub_content = []
	
	for part in quote_scrub_content:
		pieces = part.split(" ")
		for piece in pieces:
			if match_phrase in piece:
				space_scrub_content.append(piece)
	
	for url in space_scrub_content:
		if piece in url:
			continue
		for piece in repeat_scrub_content:
			type_scrubbed = piece.replace(".jpg", "")
			type_scrubbed = type_scrubbed.replace(".png", "")
			type_scrubbed = type_scrubbed.replace(".jpeg", "")
			type_scrubbed = type_scrubbed.split(match_phrase)[1]
			if type_scrubbed in url or piece in url:
				continue
		repeat_scrub_content.append(url)

final_content = list(dict.fromkeys(repeat_scrub_content))

i = 0
j = 1
while j < len(final_content):
	for k in range(0, i + 1):
		type_scrubbed = final_content[k].replace(".jpg", "")
		type_scrubbed = type_scrubbed.replace(".png", "")
		type_scrubbed = type_scrubbed.replace(".jpeg", "")
		if type_scrubbed in final_content[j]:
			final_content.remove(final_content[j])
			break
	i += 1
	j += 1
	
for url in final_content:
	for ignore_phrase in ignore_phrases:
		if ignore_phrase in url:
			final_content.remove(url)

for url in final_content:
		output_file.write(url + "\n")

output_file.close()

print("done!")