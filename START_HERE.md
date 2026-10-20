# Start here: GlucoTwin Bharat

## 1. Run the app on Windows

Install Python 3.10+ and Node.js 18+ first.

1. Extract this project folder.
2. Double-click `start_backend_windows.bat`. Leave this terminal running.
3. Double-click `start_frontend_windows.bat` in a second terminal.
4. Open the local URL printed by Vite, normally `http://localhost:5173`.
5. Backend API documentation: `http://127.0.0.1:8000/docs`.

The first launch downloads Python and JavaScript dependencies, so internet access is needed. The first model forecast can take a few seconds while the synthetic Random Forest models train.

## 2. Try the proof-of-concept

- Select a virtual patient.
- Inspect the synthetic historical profile and glucose trajectory.
- Click **Update forecast**.
- Edit the meal/carbohydrate, steps, sleep, and threshold inputs.
- Click **Compare scenario**.
- Click **Advance simulated sensor by 5 minutes** to update the in-memory sensor stream.
- Use **Reset demo** to restore the seed observations.

## 3. Before submitting

- Confirm registered team name, college label and contact details.
- Run backend tests using `cd backend`, then `pip install -r requirements-dev.txt`, then `python -m pytest -q`.
- Run `npm install` and `npm run build` in `frontend` on an internet-connected machine.
- Record the actual running app and explain it using `docs/demo-script.md`; the challenge listing requires a minimum 20-minute demonstration video.
- Make the GitHub repository public and check all links in a logged-out/incognito browser.
- Submit the public GitHub URL before the challenge portal deadline.

## Safety note
All patient profiles and signals are synthetic. This project is an engineering proof-of-concept and is not for medical decisions.
