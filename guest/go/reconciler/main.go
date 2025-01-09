//go:generate go run go.bytecodealliance.org/cmd/wit-bindgen-go generate --world reconciler --out gen ../../../wit
package main

import (
	"encoding/json"
	"fmt"

	topov1alpha1 "github.com/henderiw/godantic_api_example/apis/topo/v1alpha1"
	"github.com/henderiw/reconciler/gen/example/reconciler/reconciler"
	"github.com/henderiw/reconciler/gen/example/reconciler/retrieve"
	"go.bytecodealliance.org/cm"
)

func returnErr(reconcileError reconciler.ReconcileError) cm.Result[reconciler.ReconcileResultShape, reconciler.ReconcileResult, reconciler.ReconcileError] {
	return cm.Err[cm.Result[reconciler.ReconcileResultShape, reconciler.ReconcileResult, reconciler.ReconcileError]](reconcileError)
}

func init() {
	reconciler.Exports.Reconcile = func(object string) cm.Result[reconciler.ReconcileResultShape, reconciler.ReconcileResult, reconciler.ReconcileError] {
		// Example: Check if input is empty
		if object == "" {
			return returnErr(reconciler.ReconcileError{
				Code:    400,
				Message: "cannot reconcile with empty input",
			})
		}

		// Parse input using jsonparser
		topo := &topov1alpha1.Topology{}
		if err := json.Unmarshal([]byte(object), topo); err != nil {
			return returnErr(reconciler.ReconcileError{
				Code:    400,
				Message: "cannot unmarshal json",
			})
		}

		if err := topov1alpha1.CustomValidator(topo); err != nil {
			return returnErr(reconciler.ReconcileError{
				Code:    400,
				Message: err.Error(),
			})
		}

		topo.ObjectMeta.Name = "wim"
		fmt.Println("topo object", topo)

		get_response := retrieve.Get("Wim")
		fmt.Println("get_response", get_response)

		b, err := json.Marshal(topo)
		if err != nil {
			return returnErr(reconciler.ReconcileError{
				Code:    400,
				Message: "cannot marshal json",
			})
		}

		// Construct a success result
		reconcileSuccess := reconciler.ReconcileResult{
			Requeue:      false,
			RequeueAfter: 0,
			Object:       string(b),
		}

		// Return the success result using cm.OK
		return cm.OK[cm.Result[reconciler.ReconcileResultShape, reconciler.ReconcileResult, reconciler.ReconcileError]](reconcileSuccess)
	}
}

// main is required for the `wasi` target, even if it isn't used.
func main() {}
