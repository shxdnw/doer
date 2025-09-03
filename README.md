# doer

A simple script/command launcher that shows a menu and runs whatever you pick.  
It’s mostly for **personal use**, and is customizable through a JSON config file.  

---

## Example Usage

### `menu_config.json`
```json
{
  "1": {
    "name": "List files in current directory",
    "command": "ls -la"
  },
  "2": {
    "name": "Run backup script",
    "command": "./scripts/backup.sh"
  }
}
