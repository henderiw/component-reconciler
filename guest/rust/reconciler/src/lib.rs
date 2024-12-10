#[allow(warnings)]
mod bindings;

use bindings::Guest;

struct Component;

impl Guest for Component {
    fn reconcile(o: String) -> String {
       o
    }
}

bindings::export!(Component with_types_in bindings);
