import requests
import os
from typing import List, Dict
import subprocess

# First, install the Ollama Python client if not already installed
try:
    import ollama
except ImportError:
    print("Ollama Python client not found. Installing...")
    subprocess.check_call(["pip", "install", "ollama"])
    import ollama

def fetch_latest_file_urls() -> List[Dict[str, str]]:
    """Fetch the latest four file URLs from the backend service."""
    url = "https://featurebackend.onrender.com/fetchfile"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        file_urls = [{"secure_url": file["secure_url"]} for file in data]
        print(f"Successfully fetched {len(file_urls)} file URLs")
        return file_urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching file URLs: {e}")
        return []

def download_file_content(url: str) -> str:
    """Download and return the content of a file from its URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading content from {url}: {e}")
        return ""

def generate_design_instructions_with_ollama(file_contents: List[str]) -> str:
    """Generate design instructions using Ollama Python client with Llama3 8B model."""
    # Create prompt for the LLM to merge file contents into design instructions
    prompt = """
    Merge the following pieces of information into clear design instructions for wireframes suitable for a design tool like Figma or Motiff:
    Do not mention names of design tools in your response, I have provided names to for your understanding.
    """
    
    # Add each file content to the prompt
    for i, content in enumerate(file_contents, 1):
        prompt += f"\n--- FILE {i} ---\n{content}\n"
    
    prompt += """
    
    The output should include:
    - Design Objectives
    - User Interface Requirements
    - Functional Elements
    - Visual Style Guidelines
    - Interaction Flow
    
    Be clear and concise.
    """
    
    try:
        # Generate using the Ollama Python client
        response = ollama.generate(
            model="llama3:8b",
            prompt=prompt,
            options={
                "temperature": 0.3,
                "num_predict": 1500
            }
        )
        return response['response']
    except Exception as e:
        print(f"Error generating design instructions with Ollama client: {e}")
        return f"Error: Failed to generate design instructions: {e}"

def main():
    # Step 1: Fetch latest file URLs
    file_urls = fetch_latest_file_urls()
    
    if not file_urls:
        print("No file URLs found. Exiting.")
        return
    
    # Step 2: Download content from each URL
    file_contents = []
    for file_url_obj in file_urls:
        url = file_url_obj.get("secure_url")
        if url:
            content = download_file_content(url)
            if content:
                file_contents.append(content)
    
    if not file_contents:
        print("No file contents could be downloaded. Exiting.")
        return
    
    print(f"Successfully downloaded content from {len(file_contents)} files")
    
    # Step 3: Generate design instructions using Ollama with Llama3
    merged_instructions = generate_design_instructions_with_ollama(file_contents)
    
    # Step 4: Save the merged instructions to a file
    output_file_path = "final_design_instructions.txt"
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(merged_instructions)
    
    print(f"Merged design instructions successfully saved to '{output_file_path}'.")

if __name__ == "__main__":
    main()