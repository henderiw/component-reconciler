use anyhow::{Context, Result};
use std::path::PathBuf;
use wasmtime::component::{bindgen, Component, Linker};
use wasmtime::{Engine, Store};

bindgen!({
    path: "../../../wit",
    world: "reconciler",
    async: false
});

pub struct States;

impl States {
    pub fn new() -> Self {
        States
    }
}

fn reconcile(path: PathBuf, input_json: String) -> Result<String> {
    // Construct the Wasmtime engine
    let engine = Engine::default();

    // Load the WebAssembly component
    let component = Component::from_file(&engine, path).context("Component file not found")?;

    // Create the store to manage the state of the component
    let states = States::new();
    let mut store = Store::new(&engine, states);

    // Set up the linker for linking interfaces
    let linker = Linker::new(&engine);

    // Instantiate the component
    let instance = Reconciler::instantiate(&mut store, &component, &linker)
        .context("Failed to instantiate the reconciler world")?;

    // Call the `reconcile` function
    let result = instance
        .call_reconcile(&mut store, &input_json)
        .context("Failed to call reconcile function")?;
    
    // Handle the inner result
    //result.map_err(|e| anyhow::anyhow!(e)) // Map the inner error into the outer Result
    Ok(result)
}

fn main() -> Result<()> {
    let wasm_path = PathBuf::from(std::env::var_os("GUEST_WASM_PATH").context("missing/invalid path to WebAssembly module (env: GUEST_WASM_PATH)")?);

    // Input JSON
    let input_json = r#"{"items": ["item1", "item2", "item3"]}"#.to_string();

    // Call the reconcile function
    match reconcile(wasm_path, input_json) {
        Ok(output_json) => {
            println!("Reconcile succeeded with output: {}", output_json);
        }
        Err(e) => {
            eprintln!("Reconcile failed: {}", e);
        }
    }

    Ok(())
}
