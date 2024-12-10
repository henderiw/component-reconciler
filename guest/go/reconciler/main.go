//go:generate go run go.bytecodealliance.org/cmd/wit-bindgen-go generate --world reconciler --out gen ../../../wit
package main

import (
	"github.com/henderiw/reconciler/gen/example/reconciler/reconciler"
)

func init() {
	reconciler.Exports.Reconcile = func(object string) (result string) {
		return "{'first': 'wim', 'last': 'henderickx}"
		//type MyResult = cm.Result[string, string, string]
		//return cm.OK[MyResult]("{'first': 'wim', 'last': 'henderickx}")
	}
}

// main is required for the `wasi` target, even if it isn't used.
func main() {}
