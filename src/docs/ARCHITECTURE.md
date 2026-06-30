```text
[basic execution binary] (PyInstaller Bundle)
   │
   └──> src/main.py (Runtime Entry Point)
         │
         ├───> src/config/ (Engine Bootstrapping & Memory Allocation)
         │       ├── tokenization_config  ───> Sets Lexer boundaries
         │       ├── variable_tree_config ───> Initializes Global Scope Matrix
         │       └── memory_config        ───> Pre-allocates variable to data-nodes
         │
         └───> src/parser/ (The Primary Compilation Pipeline)
                 │
                 ├───> env_parser ───> Establishes isolation for parent scopes
                 └───> parser     ───> Generates the root execution block
                        │
                        │   [AST Execution Sub-trees Dispatcher]
                        ├───────────────────┼───────────────────┤
                        ▼                   ▼                   ▼
             src/condition_tree/      src/loop_tree/       src/io_tree/
             (Control Flow Layer)    (Iteration Layer)   (I/O Pipeline Layer)
                ├── condition_parser    ├── loop_parser     ├── display_parser
                └── condition_tree      └── loop_tree       ├── get_parser
                        │                   │               ├── input_tree
                        │                   │               └── output_tree
                        │                   │                    │
                        ▼                   ▼                    ▼
         └──────────────┴───────────────────┴────────────────────┘
                                    │
                                    ▼
                        src/utils/ (Evaluation Nodes)
                           ├── condition_extractor ───> Resolves logic flags
                           ├── condition_scope     ───> Handles block scope elements
                           └── evaluator_node      ───> Orchestrates statement math
                                    │
                                    ▼
                        src/data_node/ (Type & Value Mutation Runtime)
                           ├── data_node ───────> Native data assignments
                           └── type_conversion ─> Strict type validation (Integer casting)
                                    │
                                    └───> src/library/ (Core Standard Lib)
                                            ├── maths/calculation
                                            └── random_number/random
```