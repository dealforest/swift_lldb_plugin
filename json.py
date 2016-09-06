#!/usr/bin/env python

import lldb
import tempfile

def process(debugger, command, result, internal_dict):
    lldb.debugger.HandleCommand("""
    expr -l swift --
    func $process<T>(path: String, _ object: T) {
        func scanningArray<U>(object: U?) -> Array<AnyObject>? {
            guard let object = object else { return nil }

            let mirror = Mirror(reflecting: object)
            if mirror.children.count == 0 {
                return nil
            }

            var array = Array<AnyObject>()
            mirror.children.forEach { child in
                array.append(scan(child.value))
            }
            return array
        }

        func scanning<U>(object: U?) -> Dictionary<String, AnyObject>? {
            guard let object = object else { return nil }

            let mirror = Mirror(reflecting: object)
            if mirror.children.count == 0 {
                return nil
            }

            var dict = Dictionary<String, AnyObject>()
            mirror.children.forEach { child in
                guard let label = child.label else { return }

                dict[label] = scan(child.value)
            }
            return dict
        }

        func scan<U>(object: U) -> AnyObject {
            let mirror = Mirror(reflecting: object)
            if let label = mirror.children.first?.label where label.hasPrefix("[") && label.hasSuffix("]") {
                return scanningArray(object) ?? []
            }
            else {
                return scanning(object) ?? String(object)
            }
        }

        func json(object: AnyObject) -> String {
            if let data = try? NSJSONSerialization.dataWithJSONObject(object, options: .PrettyPrinted) {
                return String(data: data, encoding: NSUTF8StringEncoding) ?? ""
            }
            else {
                return String(object)
            }
        }

        let converted = scan(object)
        let _json = json(converted)
        print(_json)
        try! _json.writeToFile(path, atomically: true, encoding: NSUTF8StringEncoding)
        print(path)
    }
    """.strip())
    path = tempfile.mktemp() + '.json'
    lldb.debugger.HandleCommand('expr -l swift -- $process("' + path + '", ' + command + ')')

def __lldb_init_module(debugger,internal_dict):
    debugger.HandleCommand("command script add -f json.process json")
    print "json command enabled."
