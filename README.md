# Space-Habitat-Designer
🚀 Project Artemis Habitat Design Studio
🌟 1. Project Overview
HABITAT DESIGN STUDIO is an easy-to-use, accessible visual tool designed to enable rapid prototyping and functional assessment of modular space habitat layouts for crewed missions to the Moon (Artemis) and Mars.

Built using Python and NiceGUI, this tool focuses on simplifying the iterative design process by incorporating critical mission constraints and providing immediate, rule-based feedback to the designer.

The Challenge Addressed
We aim to replace complex, time-consuming CAD workflows with a simple, web-based drag-and-drop paradigm. Our objective is to empower users to quickly:

Define a habitat volume using pre-sized modular components.

Partition the volume into necessary functional areas (life support, exercise, sleep, etc.).

Iterate and assess the design against mission-specific constraints (crew size, volume requirements).

✨ 2. Key Features
Habitat Construction and Visualization
Modular Assembly: Users can place pre-defined habitat modules (e.g., Living Quarters, Labs, Utility Cylinders) into a 3D environment.

Snap-to-Grid Placement: Modules are automatically snapped to a defined coordinate grid (GRID_SIZE = 5), simulating structured assembly and deployment constraints (like robotic placement or alignment systems).

Collision Detection: The system prevents modules from being placed at occupied grid coordinates, enforcing physical constraints immediately.

Real-Time Metrics: Continuously calculates and displays key metrics, such as the Total Habitat Volume (in cubic meters).

Future Functionality (Hackathon Goals)
Rule-Based Sizing (Planned): Implement functions to impose "rules" on minimum area/volume based on crew size and mission duration, alerting the user when a functional area is undersized.

Functional Zoning: Allow users to define specific zones (e.g., Waste Management, Exercise) within the habitat volume and check if they meet NASA's reference volume requirements.

Deployment Constraints: Add a feature to simulate a Launch Vehicle Payload Fairing (e.g., a simple bounding box) to visualize if the total habitat assembly exceeds launch limitations.

🛠️ 4. Installation and Setup
Prerequisites
Git (for cloning the repository)

Python 3.8 or higher

Step-by-Step Guide
Clone the Repository:

git clone [HTTPS URL copied from GitHub]
cd [your-repo-name]

Create and Activate Virtual Environment:

# Create the environment
python -m venv venv

# Activate the environment (Windows)
.\venv\Scripts\activate

# Activate the environment (macOS/Linux)
source venv/bin/activate

Install Dependencies:

pip install nicegui

Run the Application:

python Main.py

The application will launch in your web browser at the specified address (usually http://localhost:8080).

⚙️ 5. Application Workflow
View the Scene: The 3D scene (powered by Three.js) is on the left. You can click and drag to orbit, and use the scroll wheel to zoom.

Define Position: Use the X, Y, and Z input boxes in the control panel to set the coordinates for the new module.

Note: The values will be automatically snapped to the nearest 5-meter grid coordinate upon placement.

Place Module: Click 'Place Living Quarters' (2x2x3m box) or 'Place Lab' (Cylinder: 1.5m radius, 4m height).

Check Feedback:

If the placement is successful, the module appears in 3D.

If the coordinate is occupied, a red notification (❌ Position is already occupied!) appears, enforcing the collision rule.

Review Metrics: Check the "Habitat Statistics" section for the updated Total Volume.

🤝 6. Collaboration and Contribution
We welcome contributions! To ensure a smooth collaborative experience during the hackathon, please follow this simple workflow:

PULL the latest changes before starting work:

git pull origin main

CODE your feature or fix.

COMMIT your changes with a clear, descriptive message:

git add .
git commit -m "FEAT: Added support for module deletion logic."

PUSH your work to the main branch frequently:

git push origin main

📜 7. License and Contact
This project is licensed under the MIT License.

Role

Team Member

Project Lead

Davyani Vasta

Developer

Davyani Vasta

Developer

Parishat Tanakoor

Contact

Davyani Vasta - qwertyright26@gmail.com


