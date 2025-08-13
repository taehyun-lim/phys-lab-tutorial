# Viva PHYS Lab Interactive Tutorial

An interactive tutorial for PHYS lab courses, built with Streamlit. It provides hands-on simulations, guided prompts, and checks for understanding.

## Quick start (macOS)

```bash
cd "/Users/tlim/Library/CloudStorage/GoogleDrive-tlim@hamilton.edu/My Drive/Course Support/2025 Fall/Viva/tutorial"
source /Users/tlim/venv_physl/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown in the terminal.

## Structure

- `app.py`: Home page and global configuration
- `pages/01_Projectile_Motion.py`: Kinematics module with an interactive projectile simulator
- `pages/02_Oscillations.py`: Simple harmonic motion module with damping controls
- `requirements.txt`: Python dependencies

## Notes

- Python 3.11+ recommended.
- To stop the app, press `Ctrl+C` in the terminal.
- To update dependencies, edit `requirements.txt` and run `pip install -r requirements.txt` again.

