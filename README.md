# M3
Hello World!

We are glad you stumbled upon the Github for M^3, the MIT Movement Map. M^3 culminates in a plotly map (https://plotly.com/~naylahcan/1/) that shows how many students are expected to be in each MIT academic building in real-time. Red dots centered at the coordinates for each academic building have their radii scaled by the student count; the bigger the red circle, the more students in that area.

All data for this map was derived from the Firehose (a popular MIT class scheduling tool & course info archive) public Github repository (https://github.com/edfan/firehose). More specifically, we cleaned full.json data to extract relevant course data such as building number, start and end time, and average enrollment. Plotly was used in conjunction with mapbox to overlay the student count data bubbles on a custom mapbox style centered at MIT. 

Although M^3 cannot be opened as a webpage due to plotly chart studio iframe issues, running M3webPy.py automatically opens current map of MIT student counts in your browser. If one wants to run M^3 for themselves, we would recommend downloading all of the repository's files and running M3webPy.py in an IDE (i.e. Spyder, VScode). See a video walkthrough of our project here (https://youtu.be/01iVJ544b0k).

Thank you, and we hope you enjoy our map!

Sincerely, 
The M^3 Creators, Naylah Canty & Muna Nwana
