mkdir foo
cd foo
uv venv .venv
source .venv/bin/activate
cargo install wasmtime-cli
pip install pydantic==2.5.3 componentize-py
curl -OL https://github.com/WebAssembly/wasi-cli/archive/refs/tags/v0.2.2.tar.gz
tar xf v0.2.2.tar.gz
curl -OL https://github.com/dicej/wasi-wheels/releases/download/latest/pydantic_core-wasi.tar.gz
tar xf pydantic_core-wasi.tar.gz
cat >app.py <<EOF
from command import exports
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

class Run(exports.Run):
    def run(self) -> None:
        external_data = {'id': '123', 'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}
        user = User(**external_data)
        print(user)
EOF
componentize-py -d wasi-cli-0.2.2/wit -w command componentize app -o cli.wasm
wasmtime run cli.wasm