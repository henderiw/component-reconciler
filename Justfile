just := just_executable()

cargo := env_var_or_default("CARGO", "cargo")
go := env_var_or_default("GO", "go")
tinygo := env_var_or_default("TINYGO", "tinygo")
componentize-py := env_var_or_default("COMPONENTIZE_PY", "componentize-py")
uv := env_var_or_default("UV", "uv")

@_default:
    {{just}} --list

# Check for required tools by subproject
check:
    {{just}} -f guest/rust/reconciler/Justfile check
    {{just}} -f guest/go/reconciler/Justfile check
    {{just}} -f guest/python/reconciler/Justfile check

#########
# Build #
#########

# Build all
build: build-guest

# Build guest components
build-guest: build-guest-rust build-guest-go build-guest-python2

# Build the `guest reconciler` rust WebAssembly component
build-guest-rust:
    {{just}} -f guest/rust/reconciler/Justfile build

# Build the `guest reconciler` python WebAssembly component
build-guest-go:
    {{just}} -f guest/go/reconciler/Justfile build

# Build the `guest reconciler` python WebAssembly component
build-guest-python2:
    {{just}} -f guest/python/reconciler/Justfile build

#########
# Run   #
#########

# Run the host
run: run-host-rust

# Run a Rust host
run-host-rust:
    {{just}} -f host/rust/reconciler/Justfile run
