#!/usr/bin/env python

import lldb

def process(debugger, command, result, internal_dict):
    evaluateExpressionValue("""
    func $hasAmbiguity(view: UIView) -> Bool {
        var hasAmbiguity = false
        if view.hasAmbiguousLayout() {
            print("[AMBIGUITY LAYOUT] \(view)")
            hasAmbiguity = true
        }

        view.subviews.forEach { subview in
            if $hasAmbiguity(subview) {
                hasAmbiguity = true
            }
        }
        return hasAmbiguity
    }
    """.strip())

    evaluateExpressionValue("""
    func $exerciseAmbiguityInLayoutRepeatedly(view:UIView) {
        if $hasAmbiguity(view) {
            print("!!! found ambigurous layout: \(view)")
            NSTimer.scheduledTimerWithTimeInterval(0.5,
                                                   target: view,
                                                   selector: #selector(UIView.exerciseAmbiguityInLayout),
                                                   userInfo: nil,
                                                   repeats: true)
        }

        view.subviews.forEach { subview in
            $exerciseAmbiguityInLayoutRepeatedly(subview)
        }
    }
    """.strip())

    evaluateExpressionValue('$exerciseAmbiguityInLayoutRepeatedly(' + command + ')')

def __lldb_init_module(debugger,internal_dict):
    debugger.HandleCommand("command script add -f ambigurous_layout.process ambigurous_layout")
    print "ambigurous_layout command enabled."

def evaluateExpressionValue(expression):
    frame = lldb.debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame()
    options = lldb.SBExpressionOptions()
    options.SetLanguage(lldb.eLanguageTypeSwift)
    value = frame.EvaluateExpression(expression, options)
    error = value.GetError()

    if error.Fail():
        # When evaluating a `void` expression, the returned value has an error code named kNoResult.
      # This is not an error that should be printed. This follows what the built in `expression` command does.
      # See: https://git.io/vwpjl (UserExpression.h)
      kNoResult = 0x1001
      if error.GetError() != kNoResult:
          print error

    return value
