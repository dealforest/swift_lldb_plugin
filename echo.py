#!/usr/bin/env python

import lldb

def process(debugger, command, result, internal_dict):
    lldb.debugger.HandleCommand("""
    expr -l swift --
    func $process(text: String) {
        print(text)
    }
    """.strip())
    expr = 'expr -l swift -- $process(' + command + ')'
    lldb.debugger.HandleCommand(expr)

def __lldb_init_module(debugger,internal_dict):
    debugger.HandleCommand("command script add -f echo.process echo")
    print "echo command enabled."
