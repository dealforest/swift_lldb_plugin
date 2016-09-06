# LLDB Plugin for Swift


This is LLDB Plugin for Swift, requirements Swit 2.2.
It is a collection of useful commands.

I'm not going to correspond to the various Swift versions.
If it does not work different version, please fix local.

## Usage

write .lldbinit
```
command script import <path_to>/json.py --allow-reload
```
or

```
(lldb) command script import <path_to>/json.py --allow-reload
```

## LLDB Command
### json
This command is `AnyObject` convert to JSON

```
(lldb) json <AnyObject>

(lldb) po A()
<A: 0x7fa5b3e1b060>  // class...orz

(lldb) po B()
▿ B
  - string : "a"
  - int : 1
  - float : 1.0
  ▿ array : 3 elements
    - [0] : "a" { ... }
    - [1] : "b" { ... }
    - [2] : "c" { ... }

(lldb) json A()
{
  "b" : {
    "array" : [
      "a",
      "b",
      "c"
    ],
    "int" : "1",
    "float" : "1.0",
    "string" : "a"
  },
  "array" : [
    "a",
    "b",
    "c"
  ],
  "int" : "1",
  "float" : "1.0",
  "string" : "a"
}
/var/folders/63/jdd3tr3950s_0wvf5fk3_5xr0000gn/T/tmpbTHjbn.json
```

#### filtering

use [jq](https://stedolan.github.io/jq/)

```shell
$ brew install jq
$ cat /var/folders/63/jdd3tr3950s_0wvf5fk3_5xr0000gn/T/tmpbTHjbn.json | jq '.b'
{
  "array": [
    "a",
    "b",
    "c"
  ],
  "int": "1",
  "float": "1.0",
  "string": "a"
}
```

### slack
This command send the device file to slack.

Please rewrite slack `'<token>'`

```lldb
(lldb) slack <path>

(lldb) slack "Documents/deafult.realm"
```

### show_image

This command open the image in Preview.app.

```
(lldb) show_image <UIImage>
```

### ambigurous_layout

### echo

