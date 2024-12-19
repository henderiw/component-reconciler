#[allow(warnings)]
pub mod bindings;

use bindings::{Guest, ReconcileResult, ReconcileError};

struct Component;

impl Guest for Component {
    fn reconcile(o: String) -> Result<ReconcileResult, ReconcileError> {
        Ok(ReconcileResult{requeue: false, requeue_after: 0, object: o})
    }
}

bindings::export!(Component with_types_in bindings);
