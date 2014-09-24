# SublimePacks

A collection of small Sublime Text 3 plugins and helper commands.

The available plugins are:  

### cmd.py
This plugin will one the cmd prompt in the directory of the current file.  
To use right click -> Cmd

### copy_line.py
This plugin will copy and paste one or more lines from the current file
To use right click -> Copy # line
Examples of inputs

  - For a single line: `25`
  - For line 25 and next 2 lines: `25:2`
  - For line 25 till 27: `25-27`


### panel_docs.py
This plugin will search in the current dir and on parent ones for a file named
`paneldocs.json` and when the `show_my_docs` command will run it will pop a panel
with the docs provided in the json file for the current word/selection.  
To run it `Ctrl+Alt+DblClick` or `right click -> Show my docs`  

Adding docs
```javascript
{
    "keys": ["get_data"], // array of words to match this docs
    "case": false, // if search should be case sensitive
    "content": "Reads a json file", // the content that will show in the panel
    "scope": "source.python" // the scope where this is valid, * for all scopes
}
```

## Install
To install go to your Packages folder and run
`git clone https://github.com/ionutvmi/sublimePacks.git`  
Or download and unzip the archive in your packages folder.

## Contributions 
If you find a bug or have suggestions open an issue [here](https://github.com/ionutvmi/SublimeMybbTplEditor/issues)

## Donate 
If you like my code you can support me by making a [donation](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5VVJJXVFMQ9ZN)


