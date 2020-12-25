# plugin-adder-alemibot
Tool to manage plugins

## Usage:
ADD:
```
.plugin_add [-b branch] [-d directory] <link-repo>
```
### Info about:
> **-b** gives you the possibility to choose a specific branch<br>
(OPTIONAL, defaul will use **main**)

> **-d** Use that flag to choose a specific folder for installation.<br>**Example**: -d test_dir (*add the module to plugins/test_dir*)<br>
(OPTIONAL, default will use plugins/repo-name)

> **\<github-link>** a valid github link poiting to a repo

### Example:
```
.plugin_add -b main -d plugin_dir github.com/user/plugin.git
```
After that run **.update -force** to add the new plugins.

LIST:

```
.plugin_list
```
### Info about:
This command will print all the submodules installed 

REMOVE:

```
.plugin_remove <plugin>
```
### Info about:
This command will delete the plugin from the system

> **\<plugin>** a valid plugin installed, see the list with .plugin_list

### Example:
```
.plugin_remove plugins/plugin_dir
  ```
## Installation:
To install this plugin you need:
 - git

 sh:
  ```bash
     git submodule add git@github.com:reloonfire/plugin-manager-alemibot.git plugins/plugin-manager
  ```
  https:
   ```bash
     git submodule add https://github.com/reloonfire/plugin-manager-alemibot.git plugins/plugin-manager
  ```
  and just restart the bot :D
