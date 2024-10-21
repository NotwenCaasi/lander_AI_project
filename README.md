# Documentation about the project

lander_ai_project/
│
├── environments/              # Contains planet environments and simulations
│   ├── __init__.py            # Makes this folder a package
│   ├── planet_environment.py  # Contains the PlanetEnvironment class
│   ├── terrain.py             # Terrain modeling and generation
│   └── physics.py             # Physics calculations (gravity, drag, etc.)
│
├── ai_models/                 # Contains AI models for different objectives
│   ├── __init__.py            # Makes this folder a package
│   ├── fast_landing_ai.py     # AI for fastest landing
│   ├── fuel_efficient_ai.py   # AI for fuel-efficient landing
│   └── spin_landing_ai.py     # AI for landing with spin
│
├── lander/                    # Contains lander dynamics and aero properties
│   ├── __init__.py            # Makes this folder a package
│   ├── lander.py              # Lander dynamics and state updates
│   └── aero_properties.py     # Aerodynamic properties of the lander
│
├── utils/                     # Contains utility functions (e.g., logging, plotting)
│   ├── __init__.py            # Makes this folder a package
│   ├── visualization.py       # ASCII visualization or plotting tools
│   ├── data_logger.py         # Logs data during simulation (optional)
│   └── helpers.py             # Other utility functions (e.g., terrain generation helpers)
│
├── main.py                    # Main script to run the simulation and train AI
└── README.md                  # Documentation about the project
