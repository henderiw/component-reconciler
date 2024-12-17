just := just_executable()

cargo := env_var_or_default("CARGO", "cargo")
go := env_var_or_default("GO", "go")
tinygo := env_var_or_default("TINYGO", "tinygo")
componentize-py := env_var_or_default("COMPONENTIZE_PY", "componentize-py")
uv := env_var_or_default("UV", "uv")

guest_rust_wasm_path := join(invocation_directory(), "guest/rust/reconciler/target/wasm32-wasip1/release/reconciler.wasm")
guest_python_wasm_path := join(invocation_directory(), "guest/python/reconciler/reconciler.wasm")
guest_golang_wasm_path := join(invocation_directory(), "guest/go/reconciler/reconciler.wasm")

@_default:
    {{just}} --list

# Check for required tools by subproject
@check:
    {{just}} -f guest/rust/reconciler/Justfile check
    {{just}} -f guest/go/reconciler/Justfile check
    {{just}} -f guest/python/reconciler/Justfile check

#########
# Build #
#########

# Build all
@build: build-guest

# Build guest components
@build-guest: build-guest-rust build-guest-go build-guest-python

# Build the `guest reconciler` rust WebAssembly component
@build-guest-rust:
    {{just}} -f guest/rust/reconciler/Justfile build

# Build the `guest reconciler` python WebAssembly component
@build-guest-go:
    {{just}} -f guest/go/reconciler/Justfile build

# Build the `guest reconciler` python WebAssembly component
@build-guest-python:
    {{just}} -f guest/python/reconciler/Justfile build

#########
# Run   #
#########

# Run the host
@run-all: run-guest-rust run-guest-golang run-guest-python

# Run the host with the rust guest
@run-guest-rust:
    echo "==> running rust guest component..."
    GUEST_WASM_PATH={{guest_rust_wasm_path}} {{just}} -f host/rust/reconciler/Justfile run

# Run the host with the golang guest
@run-guest-golang:
    echo "==> running golang guest component..."
    GUEST_WASM_PATH={{guest_golang_wasm_path}} {{just}} -f host/rust/reconciler/Justfile run

# Run the host with the python guest
@run-guest-python:
    echo "==> running python guest component..."
    GUEST_WASM_PATH={{guest_python_wasm_path}} {{just}} -f host/rust/reconciler/Justfile run
