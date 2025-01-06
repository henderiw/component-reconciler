
mod wasmtime_bindings {
    wasmtime::component::bindgen!({
        path: "../../../wit", 
        world: "reconciler",
        async: false,
        //with: {
        //    "wasi": wasmtime_wasi::bindings,
        //},
    });
}

pub use wasmtime_bindings::Reconciler;