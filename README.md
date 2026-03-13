# LLM-Powered Prompt Router for Intent Classification

## Project Overview
This service implements an intelligent prompt router that classifies user intent and delegates requests to specialized AI personas. By using a two-step process ("Classify, then Respond"), the system delivers high-quality, context-aware responses while optimizing for speed and cost.

### Key Features
- **Intent Classification**: Uses a lightweight model to detect intent (Code, Data, Writing, Career, or Unclear).
- **Expert Personas**: Sharp, opinionated personas for each domain.
- **Graceful Error Handling**: Handles malformed LLM responses and defaults to clarification.
- **Robust Logging**: All routing decisions and responses are saved to `route_log.jsonl`.
- **Confidence Thresholding**: If the classifier is unsure (< 0.7 confidence), it asks for clarification.
- **Manual Override**: prefix messages with `@code`, `@data`, etc., to bypass the classifier.

## Project Structure
- `router.py`: Main logic for classification and routing.
- `prompts.py`: Storage for all system and classifier prompts.
- `main.py`: Entry point for testing and interactive CLI.
- `route_log.jsonl`: Logs for every request.
- `Dockerfile` & `docker-compose.yml`: Containerization support.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Docker (optional, for containerization)
- OpenAI API Key

### Local Installation
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
5. Add your `OPENAI_API_KEY` to the `.env` file.

## Usage

### Running the Test Suite
To run the 15 predefined test cases and generate the initial log:
```bash
python main.py --test
```

### Running Interactive Mode
```bash
python main.py
```

### Using Docker
```bash
docker-compose up --build
```

## Supported Experts
1. **Code Expert**: Technical, code-focused, best practices.
2. **Data Analyst**: Statistical, visualization suggestions, data-driven.
3. **Writing Coach**: Feedback-oriented, structured, constructive.
4. **Career Advisor**: Pragmatic, actionable, goal-oriented.

## Evaluation Criteria fulfilled
- [x] Four distinct expert prompts.
- [x] `classify_intent` with structured JSON output.
- [x] `route_and_respond` mapping intent to personas.
- [x] Unclear intent handling with clarification questions.
- [x] Logging to `route_log.jsonl`.
- [x] Graceful error handling for LLM output.
- [x] Dockerization.
