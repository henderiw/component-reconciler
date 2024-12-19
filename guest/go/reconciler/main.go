//go:generate go run go.bytecodealliance.org/cmd/wit-bindgen-go generate --world reconciler --out gen ../../../wit
package main

import (
	"github.com/henderiw/reconciler/gen/example/reconciler/reconciler"
	"go.bytecodealliance.org/cm"
)

func init() {
	reconciler.Exports.Reconcile = func(object string) cm.Result[reconciler.ReconcileResultShape, reconciler.ReconcileResult, reconciler.ReconcileError] {
		// Example: Check if input is empty
		if object == "" {
			reconcileError := reconciler.ReconcileError{
				Code:    400,
				Message: "Input cannot be empty",
			}

			// Return an error result using cm.Err
			return cm.Err[cm.Result[reconciler.ReconcileResultShape, reconciler.ReconcileResult, reconciler.ReconcileError]](reconcileError)
		}

		// Parse input (if needed) - skipping for simplicity

		// Construct a success result
		reconcileSuccess := reconciler.ReconcileResult{
			Requeue:      false,
			RequeueAfter: 0,
			Object:       "{'first': 'wim', 'last': 'henderickx}",
		}

		// Return the success result using cm.OK
		return cm.OK[cm.Result[reconciler.ReconcileResultShape, reconciler.ReconcileResult, reconciler.ReconcileError]](reconcileSuccess)
	}
}

// main is required for the `wasi` target, even if it isn't used.
func main() {}
