This is the Milton text and template package which can be added to the Open Shakespeare project. 

INSTALL

To install, stop the Shakespeare server if running. 
Install the text package into shksprdata. You may need to rename the existing text package or add the tests to the package. You will need to rename the Shakespeare metadata.txt file if you do so or merge the files. 

Run db init to include the new package into the defined database. You may need to clean the database first. 

If you install Milton on its own, you will need to install the templates, over-writing the Shakespeare ones (or copy these if you still need Shakespeare). 

Then run the paster serve <you-config-file.ini>.

The new packages will be shown in the text index file.

REMIX

If you want to mix the texts up, then you can do this by merging the metadata.txt files which control the texts that the database knows about. You must ensure that any texts inside the metadata file are in the texts directory. 

