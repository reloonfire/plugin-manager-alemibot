# plugin-adder-alemibot
Tool to import plugins

## Usage:
```
.import [-b branch] [-d directory] <link-repo>
```
### Info about:
> **-b** gives you the possibility to choose a specific branch<br>
(OPTIONAL, defaul will use **main**)

> **-d** Use that flag to choose a specific folder for installation.<br>**Example**: -d test_dir (*add the module to plugins/test_dir*)<br>
(OPTIONAL, default will use plugins/repo-name)

> **\<github-link>** a valid github link poiting to a repo

### Example:
```
.import -b main -d yt-downloader github.com/reloonfire/yt-downloader-alemibot.git
```

## Installation:
To install this plugin you need:
 - git

 sh:
  ```bash
     git submodule add git@github.com:reloonfire/plugin-adder-alemibot.git plugins/plugin-adder
  ```
  https:
   ```bash
     git submodule add https://github.com/reloonfire/plugin-adder-alemibot.git plugins/plugin-adder
  ```
  and just restart the bot :D