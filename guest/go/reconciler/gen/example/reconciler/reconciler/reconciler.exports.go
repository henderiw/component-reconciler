// Code generated by wit-bindgen-go. DO NOT EDIT.

package reconciler

// Exports represents the caller-defined exports from "example:reconciler/reconciler@0.1.0".
var Exports struct {
	// Reconcile represents the caller-defined, exported function "reconcile".
	//
	// The `reconcile` function is the main entry point for the reconciler.
	// It takes a JSON input and returns a JSON output or an error.
	//
	//	reconcile: func(object: string) -> string
	Reconcile func(object string) (result string)
}