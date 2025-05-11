# Builder Agent User Examples

## Example 1: Generate Python Script

**User Input:**
"Builder Agent, I need a Python script that reads a CSV file named `data.csv`, filters rows where the 'status' column is 'completed', and saves the result to `completed_tasks.csv`."

**Agent Output (Ideal):**
```markdown
Okay, here's a Python script using the `pandas` library to achieve that. You'll need to have pandas installed (`pip install pandas`).

```python
import pandas as pd

def filter_completed_tasks(input_csv_path, output_csv_path):
    """Reads a CSV, filters for 'completed' status, and saves to a new CSV."""
    try:
        # Read the CSV file
        df = pd.read_csv(input_csv_path)

        # Filter rows where the 'status' column is 'completed'
        completed_df = df[df['status'].str.lower() == 'completed']

        # Save the filtered DataFrame to a new CSV file
        completed_df.to_csv(output_csv_path, index=False)
        print(f"Filtered data saved to {output_csv_path}")

    except FileNotFoundError:
        print(f"Error: The file {input_csv_path} was not found.")
    except KeyError:
        print(f"Error: The CSV file must contain a 'status' column.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    input_file = "data.csv"
    output_file = "completed_tasks.csv"
    filter_completed_tasks(input_file, output_file)
```

**To use this script:**
1.  Save it as a `.py` file (e.g., `filter_script.py`).
2.  Make sure you have a `data.csv` file in the same directory with a 'status' column.
3.  Run it from your terminal: `python filter_script.py`

A `completed_tasks.csv` file will be created with the filtered data.
```

## Example 2: Generate Dockerfile

**User Input:**
"Builder Agent, create a simple Dockerfile for a Python FastAPI application. The main file is `main.py` in the `app` directory, and it uses a `requirements.txt` file."

**Agent Output (Ideal):**
```markdown
Certainly! Here's a basic Dockerfile for a Python FastAPI application:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser -s /sbin/nologin -c "Docker image user" appuser

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code from the 'app' directory into the container at /app
COPY ./app /app

# Make port 80 available to the world outside this container (FastAPI default)
EXPOSE 80

# Change to non-root user
USER appuser

# Define environment variable (optional, if your app uses it)
# ENV NAME World

# Run main.py when the container launches
# Assuming uvicorn is in your requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

**Key features of this Dockerfile:**
*   Uses a slim Python base image.
*   Sets up a non-root user (`appuser`) for better security.
*   Copies `requirements.txt` and installs dependencies first to leverage Docker's build cache.
*   Copies your application code (expected to be in an `app` subdirectory relative to the Dockerfile).
*   Exposes port 80 (standard for FastAPI, adjust if your app uses a different port).
*   The `CMD` instruction starts your FastAPI application using `uvicorn`. Ensure `uvicorn` and `fastapi` are listed in your `requirements.txt`.

Place this Dockerfile in the root of your project, alongside the `app` directory and `requirements.txt`.
```
