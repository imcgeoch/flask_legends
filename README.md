# flask_legends
This is the codebase for legendshub.org, a site under cosntruction.

## LegendsHub
LegendsHub will be a web-based legends explorer for [Dwarf Fortress](http://bay12games.com/dwarves/), 
in the tradition of [Legends Browser](https://github.com/robertjanetzko/LegendsBrowser) and 
[Legends Viewer](https://github.com/Kromtec/LegendsViewer).

What makes LegendsHub different is the creation of a stream parser that reads the XML file into a relational database as a 
preprocessing step. This allows it to handle large legends files without running into memory restrictions and to serve 
many worlds at once.

The eventual goal is to add the code and storage capacity to support user accounts, uploading, and commenting, in order to 
allow the community to share and discuss their worlds. The project is as yet at an early state, and there is a considerable 
amount of work left before this is realized. 

LegendsHub is implemented in Python using Flask. 
