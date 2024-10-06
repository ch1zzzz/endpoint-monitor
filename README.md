## Monitor Endpoints

### 1. Clone the repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/endpoint-monitor.git
cd endpoint-monitor
```

### 2. Set up a virtual environment


- On **Linux/macOS**:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- On **Windows**:

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Install dependencies

Install the required Python libraries by running:

```bash
pip install -r requirements.txt
```

### 4. Prepare the YAML configuration file

You can find a sample configuration file named `test_endpoints.yaml` in the repository.



### 5. Run the application

```bash
python monitor.py test_endpoints.yaml
```

- Replace `test_endpoints.yaml` with the path to your actual YAML configuration file, if different.

### 6. Stop the application

To stop the program, simply press `Ctrl + C` in the terminal. The program will gracefully stop the monitoring process and exit.