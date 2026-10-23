# HamsterPet for Windows

A tiny transparent always-on-top desktop hamster. It autonomously wanders diagonally, pauses, grooms, plays, stretches and sleeps in a randomized cycle. Left-click and drag the hamster to move it. Right-click for Talk Off/On, pause/resume, and Exit. Speech bubbles appear briefly at random; Talk Off hides them until turned back on. Exit closes the app.

## Build without installing Python

Use GitHub Actions in the repository: open **Actions → Build Windows EXE → Run workflow**. Download the `HamsterPet-Windows` artifact when the workflow finishes. The artifact is a portable Windows `.exe`.

## Local development (optional)

Install Node.js 20+, open this folder in a terminal, run `npm install`, then `npm start`. Build a portable executable with `npm run dist`.
