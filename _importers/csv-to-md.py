# Takes a file CSV file called "data.csv" and outputs each row as a YAML MD file named after first column.
# Data in the first row of the CSV is assumed to be the column heading.
# Original work borrowed from: https://github.com/hfionte/csv_to_yaml

# Import the python library for parsing CSV files.
import csv
from datetime import datetime
from slugify import slugify

# Open our data file in read-mode.
csvfile = open('data.csv', 'r')

# Save a CSV Reader object.
datareader = csv.reader(csvfile, delimiter=',', quotechar='"')

# Empty array for data headings, which we will fill with the first row from our CSV.
data_headings = []

# Loop through each row...
for row_index, row in enumerate(datareader):

	# If this is the first row, populate our data_headings variable.
	if row_index == 0:
		data_headings = row

	# Otherwise, create a YAML file from the data in this row...
	else:
		# Open a new file with filename based on the first column
		date_str = row[0]
		# Sanitise the title column (2nd column of my CSV)
		title = row[1].lower()
		titleSlug = slugify(title)
		# Convert the pocket time stamp string to a date
		date_object = datetime.strptime(date_str, '%B %d, %Y at %I:%M%p').date()
		# Combine the date and title to geneate the filename
		filename = date_object.strftime("%Y-%m-%d-") + titleSlug + '.md'
		content_path = "_links/"
		new_yaml = open(content_path + filename, 'w')

		# Empty string that we will fill with YAML formatted text based on data extracted from our CSV.
		yaml_text = ""
		yaml_text += "---\n"
		# Specify the layout type to be used for links
		yaml_text += "layout: link \n"

		# Loop through each cell in this row...
		for cell_index, cell in enumerate(row):

			# Compile a line of YAML text from our headings list and the text of the current cell, followed by a linebreak.
			# Heading text is converted to lowercase. Spaces are converted to underscores and hyphens are removed.
			# In the cell text, line endings are replaced with commas.
			cell_heading = data_headings[cell_index].lower().replace(" ", "_").replace("-", "_").replace("%", "percent").replace("$", "").replace(",", "")
			cell_text = cell_heading + ': "' + cell.replace("\n", ", ") + '"' + "\n"

			# Add this line of text to the current YAML string.
			yaml_text += cell_text

		# Write our YAML string to the new text file and close it.
		new_yaml.write(yaml_text + "---\n")
		new_yaml.close()

# We're done! Close the CSV file.
csvfile.close()