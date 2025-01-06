#[allow(warnings)]
pub mod bindings;

use bindings::{Guest, ReconcileResult, ReconcileError, get};

struct Component;

impl Guest for Component {
    fn reconcile(_obj: String) -> Result<ReconcileResult, ReconcileError> {
        
        //let response = get("Wim");
        //println!("get response {}", response);

        let obj = "{\"wim\": \"mieke\"}";

        Ok(ReconcileResult{requeue: false, requeue_after: 0, object: obj.to_string()})
    }
}

bindings::export!(Component with_types_in bindings);
