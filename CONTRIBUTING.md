# Contribution Guide

Thank you for your interest in improving this project! Contributions of all kinds are welcome: bug reports, documentation updates, feature ideas, and code changes.

---

## How to Contribute

### 1. Ask or Propose

- **Bug reports:** Use GitHub Issues and include steps to reproduce, expected/actual behavior, and environment details.
- **Feature requests:** Describe the use case and how it benefits users. Small, focused proposals are easier to review.
- **Small fixes:** Typo fixes or small code changes can go directly into a pull request.

### 2. Fork & Branch

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/Shankar-CSE/my-lovely-sites.git
   cd my-lovely-sites
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feature/my-change
   ```

---

## Local Development

### Set up the environment

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   ```

4. Set the required variables in `.env` (see README for details), then generate an admin password hash:
   ```bash
   python scripts/hash_password.py
   ```

5. Run the app in development mode:
   ```bash
   python run.py
   ```

- Public catalog: `http://localhost:5000`
- Admin login: `http://localhost:5000/admin/login`

### Coding guidelines

- **Style:** Follow the existing code style in the repo (PEP 8 where practical).
- **Naming:** Use descriptive names for variables, functions, and templates.
- **Templates:** Keep Jinja templates simple and avoid heavy business logic in templates.
- **Security:** Never hard-code secrets or production connection strings. Use environment variables.

### Tests and checks

This project is light on formal tests, but when adding non-trivial behavior:

- Add or update tests if a testing setup is added in the future.
- At minimum, verify:
  - App starts without errors.
  - MongoDB connects successfully (check `/health`).
  - Public and admin routes you touched still work as expected.

---

## Making Changes

1. Make your changes in your feature branch.
2. Keep commits focused and meaningful. Prefer multiple small commits over a single "big bang" commit.
3. Run the app locally and manually test affected flows.

If you change behavior that users rely on, update:

- The relevant section of `README.md`.
- Any related documentation (e.g., deployment notes) when appropriate.

---

## Pull Requests

When you are ready to propose your changes:

1. Push your branch to your fork:
   ```bash
   git push origin feature/my-change
   ```

2. Open a Pull Request against the main repository:
   - Use a clear, descriptive title.
   - Explain **what** you changed and **why**.
   - Reference any related issues (e.g., `Closes #123`).
   - Mention any breaking changes or migration steps if applicable.

3. Be responsive to review comments; reviews are collaborative and meant to improve the codebase.

---

## Documentation Contributions

Improving documentation is highly appreciated:

- Clarify setup or deployment instructions.
- Add examples or screenshots of the UI.
- Fix typos, formatting, or outdated content.

For larger documentation reorganizations, please open an issue first so the direction can be agreed on.

---

## Code of Conduct

Please be respectful and constructive in all interactions. Assume good intent, be patient in reviews, and help maintain a welcoming environment for contributors of all experience levels.

If you encounter behavior that violates these principles, please contact the maintainer privately.
