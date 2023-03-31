# ICA-Scraper
Web Scraper that goes through an ICA (Swedish Supermarket) product's page and gives you the ingredients and whether it's gluten free or not by looking through the different headers, finding the one titled "Ingredienser" and then looking at the text under it. I've set up an array with key words for gluten (in Swedish as this is a Swedish website) curated by my celiac friend. If there are any other keywords you cant think of feel free to add them. If you want to use other keywords all you have to do is change the "GlutenFreeKeyWords" array to fit the words you want to search for. Keep in mind this only works with the ICA (https://handlaprivatkund.ica.se/stores/) website as I've hard coded where it should look for the headers.

# How to use
To use it all you need to do is run the program and input the URL into the GUI, in the text box. Then it'll look through the headers and output whether it's gluten free or not. It'll also output the ingredients and product name on the terminal.

# Things to come
I want to update the GUI so that it displays a picture of the product, the name of the product and the ingredients so that you can double check any ingredients. Along with that the GUI needs a rehaul to look a lot nicer because right now it looks like shit. In the far far future it would be great if you could simply scan a products barcode and it'll give the ingredients, but that's so WIP that I'm not even working on it.
