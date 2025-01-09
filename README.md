#

## create a wit file

## guest-rust

install component machinery

```shell
cargo install cargo-component
```

create the scafolding for the component

```shell
cd guest/rust
cargo component new reconciler --lib && cd reconciler
```

update cargo.toml
- by default package is called component:reconciler -> change to the package name of the wit file
- add: [package.metadata.component.target]

```toml
[package.metadata.component]
package = "example:reconciler"

[package.metadata.component.dependencies]

[package.metadata.component.target]
path = "../../../wit/reconciler.wit"
world = "reconciler"
```

update code
- bindings is auto generated
- implement component functions

```rust
#[allow(warnings)]
mod bindings;

use bindings::Guest;

struct Component;

impl Guest for Component {
    fn reconcile(o: String) -> Result<String, String> {
       Ok(o)
    }
}

bindings::export!(Component with_types_in bindings);

```

generate the wasm file

```shell
cargo component build --release
```

location

```shell
target/wasm32-wasip1/release/reconciler.wasm
```

verification

```shell
wasm-tools component wit target/wasm32-wasip1/release/reconciler.wasm
```

## guest in go

```shell
go mod init github.com/henderiw/reconciler
go mod tidy
go get  github.com/bytecodealliance/wasm-tools-go/cmd/wit-bindgen-go
```

create main.go with go generate inside and pointing to the world and reconciler

```go
//go:generate go run github.com/bytecodealliance/wasm-tools-go/cmd/wit-bindgen-go generate --world reconciler --out gen ../../../wit/reconciler.wit
package main

// main is required for the `wasi` target, even if it isn't used.
func main() {}
```

implement main

```go
//go:generate go run github.com/bytecodealliance/wasm-tools-go/cmd/wit-bindgen-go generate --world reconciler --out gen ../../../wit/reconciler.wit
package main

func init() {
	reconciler.Exports.Reconcile = func(object string) (result cm.Result[string, string, string]) {
		type MyResult = cm.Result[string, string, string]
		return cm.OK[MyResult]("{'first': 'wim', 'last': 'henderickx}")
	}
}
// main is required for the `wasi` target, even if it isn't used.
func main() {}
```

we need to include the dependencies for go

```shell
tinygo build --target=wasip2 --wit-package ../../../wit --wit-world reconciler -o reconciler.wasm
```

## guest in python

setup virtual env

```shell
python -m venv .venv
source .venv/bin/activate
pip install componentize-py
```

build

```shell
componentize-py --wit-path ../../../wit --world reconciler bindings .
```

implement the python function in rec.py

```python
import reconciler

class Component(reconciler.Reconciler):
    def reconcile(self, object: str) -> str:
        return object
```

!!! Note:"the file name need to be called something different; I used rec here"

```shell
componentize-py --wit-path ../../../wit --world reconciler componentize reconciler -o reconciler.wasm
```


## host in rust

initialize the project

```shell
cd host/rust
cargo new reconciler --lib && cd reconciler

cargo add anyhow
cargo add wasmtime
cargo add wasmtime-wasu
```

run the code

```shell
cargo run
```


## Issues

host RUST:
- rust guest: ok
- python guest: takes looooong
- go guest: ok

python componentize.py
- very big file
- result is not interpreted
- imports all WASI, needed or not
- 