# devmode

# This is used to write a "devmode" copmonent into an angular application and then remove it again.
# Similar to using git stash and apply

### Installation:
- `cd /path/to/devmode/`
- The install script needs a path to an angular project. eg. `./install.sh "path/to/angular/frontend/src"`
- The installer currently:
    1. greps for `# [*] Install Points` in the `_variables.py` file:
        `# [*] Install Points -- Run install.sh`
        `# [*] _SOURCE`
        `# [*] _TARGET`
    2. if grep returns anything, replace code above with code below:
        `# [***] _SOURCE and _TARGET were generated by "install.sh"`
        `_SOURCE = "/Users/master/bash_env/src/devmode"`
        `_TARGET = "/Users/master/some-project/frontend/src"`
    3. check exists/install python3.
    4. symlink devmode to `/usr/local/bin`.

### Available Commands:
* "i" : inject
    - runs `devmode -r` first.
    - writes necessary typescript to `app.module.ts` to import the devmode component and add its class name to the "exports" and "declarations".
    - writes the component's html tag into `app.component.html`
    - copies devmode's component and asset files into the file tree of the project.
* "r" : remove
    - removes lines in `app.module.ts` with devmode class name present
    - removes lines in `app.component.html` with devmode html tag present
    - deletes devmode's component and asset files from the file tree of the project.
* "s" : save
    - backs up and deletes the devmode devmode install location folders: "assets" and "component".
    - "assets-backup" and "component-backup" will be overwritten
    - copies `angular/src/app/components/devmode/` and `angular/src/app/assets/devmoe` into the devmode install location.
* "t" : test
    - runs `print("[***] devmode test works")`

### Install Points (put under _NAME in _variables.py)
`# [*] Install Points -- Run install.sh`
`# [*] _SOURCE`
`# [*] _TARGET`