# Project Structure

The project is organized as a monorepo. That means frontend, backend, AI, hardware, and docs live in one GitHub repository, but each part has its own folder.

## Folders

`frontend/`

The visual part of the platform. The current HTML/CSS prototype is inside `frontend/static/`.

`backend/`

The server part. It will receive requests from the frontend, save data to the database, receive Arduino trainer data, and call the AI model.

`ai/`

Model experiments, Roboflow dataset files, Colab notebooks, and exported model weights.

`hardware/`

Arduino code for the physical trainer and notes about sensors/data format.

`database/`

Database schema, migrations, and initial test data.

`docs/`

Documentation for how the platform works.

`infra/`

Deployment and environment configuration.

## Recommended Development Order

1. Keep the static frontend organized.
2. Add Arduino code and document what data it sends.
3. Add the AI notebook/dataset files and document the model output.
4. Build a small backend API.
5. Connect frontend to backend.
6. Connect backend to AI.
7. Add database storage for users, sessions, and results.
