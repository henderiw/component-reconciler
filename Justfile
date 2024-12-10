just := just_executable()
cargo := "cargo"
go := "go"
tinygo := "tinygo"
componentize-py := "componentize-py"

@_default:
    {{just}} --list

# Ensure `rust` tooling is present
@_ensure-tool-cargo:
    command -v {{cargo}} || echo "cargo is not installed, please install it (see: https://doc.rust-lang.org/cargo/getting-started/installation.html)"

# Ensure `go` tooling is present
@_ensure-tool-go:
    command -v {{go}} || echo "go is not installed, please install it (see: https://go.dev/doc/install)"

@_ensure-tool-tinygo:
    command -v {{go}} || echo "tinygo is not installed, please install it (see: https://tinygo.org/getting-started/install/)"

@_ensure-tool-componentize-py:
    command -v {{componentize-py}} || echo "componentize-py is not installed, please install it (see: pip install componentize-py)"

# Check for required tools
check: _ensure-tool-cargo _ensure-tool-go _ensure-tool-tinygo _ensure-tool-componentize-py

#########
# Build #
#########

# Build the `guest reconciler` rust WebAssembly component
build-guest-rust: _ensure-tool-cargo
    (cd guest/rust/reconciler && {{cargo}} component build --release)

# Build the `guest reconciler` python WebAssembly component
build-guest-go: _ensure-tool-go _ensure-tool-tinygo
    (cd guest/go/reconciler && {{go}} generate)
    (cd guest/go/reconciler && {{tinygo}} build --target=wasip2 --wit-package ../../../wit --wit-world reconciler -o reconciler.wasm)

# Build the `guest reconciler` python WebAssembly component
build-guest-python2: _ensure-tool-componentize-py
    (cd guest/python/reconciler && {{componentize-py}} --wit-path ../../../wit --world reconciler bindings .)
    (cd guest/python/reconciler && {{componentize-py}} --wit-path ../../../wit --world reconciler componentize rec -o reconciler.wasm)

#########
# Run   #
#########

run-host-rust: _ensure-tool-cargo
    (cd host/rust/reconciler && {{cargo}} run)
