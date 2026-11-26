# RAG From Scratch

## DashScope configuration

Set `DASHSCOPE_API_KEY` in the process environment before running a demo.
Use your terminal or IDE's secret settings; do not paste the key into source
code or commit an environment file. The demos do not automatically load a
`.env` file. If you use one locally, configure your launcher to load it.

The scripts `fastapi.py`, `langchain.py`, `qwenapi.py`, and
`rag_sys_demo.py` stop with a configuration error if the variable is missing
or blank. `Llamaindex.py` also reads the same environment variable.

If a key has previously been committed, reset or revoke it in Model Studio.
Removing it from the latest version of the code does not revoke the key or
remove it from old commits.
