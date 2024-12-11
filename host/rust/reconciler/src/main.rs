use std::path::PathBuf;

use anyhow::{Context, Result};
use wasmtime::component::{bindgen, Component, Linker};
use wasmtime::{Engine, Store};
use wasmtime_wasi::{ResourceTable, WasiCtx, WasiView};

bindgen!({
    path: "../../../wit",
    world: "reconciler",
    async: false
});

/// This state is used by the Runtime host,
/// we use it to store the WASI context (implementations of WASI)
/// and resource tables that components will use when executing
///
/// see:
/// - https://docs.rs/wasmtime-wasi/latest/wasmtime_wasi/trait.WasiView.html
/// - https://docs.rs/wasmtime-wasi/latest/wasmtime_wasi/fn.add_to_linker_sync.html
struct HostState {
    ctx: WasiCtx,
    table: ResourceTable,
}

impl HostState {
    pub fn new() -> Self {
        Self {
            ctx: WasiCtx::builder().build(),
            table: ResourceTable::default(),
        }
    }
}

/// This trait enables any T to provide a WASI context and
/// resource table, which enables usage by the Store
impl WasiView for HostState {
    fn ctx(&mut self) -> &mut WasiCtx {
        &mut self.ctx
    }
    fn table(&mut self) -> &mut ResourceTable {
        &mut self.table
    }
}

fn reconcile(path: PathBuf, input_json: String) -> Result<String> {
    // Construct the Wasmtime engine
    let engine = Engine::default();

    // Load the WebAssembly component
    let component = Component::from_file(&engine, path).context("Component file not found")?;

    // Create the store to manage the state of the component
    let states = HostState::new();
    let mut store = Store::<HostState>::new(&engine, states);

    // Set up the linker for linking interfaces
    let mut linker = Linker::new(&engine);

    // Add WASI implementations to the linker for components to use
    wasmtime_wasi::add_to_linker_sync(&mut linker)?;

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
    let wasm_path = PathBuf::from(
        std::env::var_os("GUEST_WASM_PATH")
            .context("missing/invalid path to WebAssembly module (env: GUEST_WASM_PATH)")?,
    );

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
