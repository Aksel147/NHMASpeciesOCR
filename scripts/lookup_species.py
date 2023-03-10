import json
from nhma_species_ocr.lookup_species.lookup_species import lookup_species
from nhma_species_ocr.util.util import word_combinations, similar


grouped_images_file = "/Users/akselbirko/Documents/DASSCO/output.json"

with open(grouped_images_file) as file:
    grouped_specimen_list = json.load(file)


for index, group in enumerate(grouped_specimen_list):
    print("processing group #{0} of {1}...".format(index+1, len(grouped_specimen_list)))
    species_word_combinations = word_combinations(group['cover']['species'])
    matches = set()
    for combination in species_word_combinations:
        res = lookup_species(combination)
        if res:
            matches.add(res['scientificName'])

    best_match = (None, 0)
    for match in matches:
        similarity = similar(match.lower(), group['cover']['species_joined'].lower())
        if similarity > best_match[1]:
            best_match = (match, similarity)

    if best_match[1] > 0.5:
        group['cover']['species_match_gbif'] = best_match[0]
    else:
        group['cover']['species_match_gbif'] = None


with open(grouped_images_file, "w+") as outfile:
    outfile.write(json.dumps(grouped_specimen_list, indent=4))
#res = lookup_species("Astracantha gossypina (Fischer) Podlech")
#print(json.dumps(res))


#print(json.dumps(res['results'][0]))

