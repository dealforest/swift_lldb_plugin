#!/usr/bin/env python

import lldb
import commands
import tempfile

def process(debugger, command, result, internal_dict):
    lldb.debugger.HandleCommand("""
    expr -l swift --
    func $process(path: String, _ image: UIImage) {
        let data = UIImagePNGRepresentation(image)!
        data.writeToFile(path, atomically: true)
    }
    """.strip())
    path = tempfile.mktemp() + ".png"
    lldb.debugger.HandleCommand('expr -l swift -- $process("' + path + '", ' + command + ')')
    commands.getoutput("open " + path)

def __lldb_init_module(debugger,internal_dict):
    debugger.HandleCommand("command script add -f show_image.process show_image")
    print "show_image command enabled."
