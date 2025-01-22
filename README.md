# insurance-contract-web3
A blockchain-based insurance application leveraging Solidity, FastAPI, and Web3.py. The repository includes:

1. Install Dependencies
Make sure you have all the required dependencies installed. In your backend/ folder, run the following command to install the necessary Python packages:

bash
Copy
Edit
pip install -r backend/requirements.txt
2. Start the FastAPI Server
Navigate to the root directory of your project (where the backend folder is located) and run the following command to start the FastAPI server:

bash
Copy
Edit
uvicorn backend.main:app --reload
backend.main:app refers to the main.py file in the backend/ folder and the app object inside it (FastAPI instance).
--reload allows the server to automatically restart whenever you make changes to the code, which is useful during development.
3. Access the Application in Your Browser
Once the server starts, open your web browser and go to:

arduino
Copy
Edit
http://127.0.0.1:8000
This will load the index.html page that contains the "Create Policy" and "Get Policies" buttons. You can interact with the buttons to call the respective functions (create_policy and get_policies) that will interact with your Ethereum smart contract.

4. Test the Application
Create Policy: Clicking the "Create Policy" button will prompt you to enter the policy name, premium, and coverage amount. The details will then be sent to the backend to interact with the Ethereum contract and create a policy.
Get Policies: Clicking the "Get Policies" button will fetch and display a list of all policies from the Ethereum contract.

project structure/
├── backend/
│   ├── main.py                 # FastAPI backend code
│   ├── .env                    # Environment variables
│   └── requirements.txt         # List of dependencies for the backend
├── templates/                   # HTML templates
│   └── index.html               # The HTML file you mentioned
├── .gitignore                   # If using git, ignore virtualenvs and unnecessary files
└── README.md                    # Optional: Documentation for your project
