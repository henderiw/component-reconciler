use std::path::PathBuf;

use anyhow::{Context, Result};
use wasmtime::component::{bindgen, Component, Linker};
use wasmtime::{Engine, Store};
use wasmtime_wasi::{ResourceTable, WasiCtx, WasiView};
use std::time::Instant;

bindgen!({
    path: "../../../wit",
    world: "reconciler",
    async: false
});

// Import the guest's bindings
//use guest_reconciler::bindings::{ReconcileResult, ReconcileError};

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

/// load the WASM component and return the instance
fn load_reconciler_instance(
    path: PathBuf,
) -> Result<(Store<HostState>, Reconciler)> {
    // Initialize the Wasmtime engine
    let engine = Engine::default();

    // Load the WASM component
    let component = Component::from_file(&engine, &path).context("Component file not found")?;

    // Create the store to manage the state of the component
    let states = HostState::new();
    let mut store = Store::<HostState>::new(&engine, states);

    // Set up the linker for linking interfaces
    let mut linker = Linker::new(&engine);

    // Add WASI implementations to the linker for components to use
    wasmtime_wasi::add_to_linker_sync(&mut linker)?;

    // Instantiate the component
    let instance = Reconciler::instantiate(&mut store, &component, &linker)
        .context("Failed to instantiate the reconciler world")?;

    Ok((store, instance))
}

// call the reconcile function
fn call_reconcile(
    store: &mut Store<HostState>,
    instance: &Reconciler,
    input_json: String,
) -> std::result::Result<ReconcileResult, ReconcileError> {
    // Call the reconcile function
    let result = instance
        .call_reconcile(store, &input_json)
        .map_err(|e| ReconcileError {
            code: 500,
            message: format!("Failed to call reconcile: {}", e),
        })??;

    Ok(result)
}


fn main() -> Result<()> {
    let wasm_path = PathBuf::from(
        std::env::var_os("GUEST_WASM_PATH")
            .context("missing/invalid path to WebAssembly module (env: GUEST_WASM_PATH)")?,
    );

    // Input JSON
    let input_json = r#"{"apiVersion":"topo.kubenet.dev/v1alpha1","kind":"Topology","metadata":{"name":"kubenet","namespace":"default"},"spec":{"defaults":{"type":"7220ixr-d3l","provider":"srlinux.nokia.com","version":"24.7.2"},"nodes":[{"name":"node1"},{"name":"node2"}],"links":[{"endpoints":[{"node":"node1","port":1,"endpoint":1},{"node":"node2","port":1,"endpoint":1}]}]}}"#.to_string();

    //load the instance
    let (mut store, instance) = load_reconciler_instance(wasm_path)
        .map_err(|e| anyhow::anyhow!("Error loading reconciler instance: {}", e))?;

   // Measure time taken to run the instance 10 times
    let start = Instant::now();

    for i in 0..10 {
        println!("Running iteration: {}", i + 1);
         // Measure iteration time
        let iteration_start = Instant::now();
        match call_reconcile(&mut store, &instance, input_json.clone()) {
            Ok(result) => {
                let iteration_duration = iteration_start.elapsed();
                println!("Reconcile Iteration {} succeeded with output: {:#?}", i, result);
                println!("Reconcile Iteration {} elaspetime {:?}", i, iteration_duration);
            }
            Err(e) => {
                let iteration_duration = iteration_start.elapsed();
                eprintln!("Reconcile Iteration {} failed: {}", i, e);
                println!("Reconcile Iteration {} elaspetime {:?}", i, iteration_duration);
            }
        }
    }

    let duration = start.elapsed();
    println!("Time taken for 10 iterations: {:?}", duration);

    Ok(())
}
