# Lab 5: Static Code Analysis — Flight Reservation System

**Your file:** `flight_reservation_system.py`

Follow the lab handout for the full instructions.

## About the program

An airline flight reservation and passenger manifest manager. It reserves flight seats, handles cancellations, calculates baggage surcharges, and exports flight manifests.

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to do

1. **Run it first** and read the output carefully:
   ```bash
   python flight_reservation_system.py
   ```
   It asks one question. Press Enter to use the default, then try a few inputs of your own. Not every problem in this file is something a tool will flag, so pay attention to output that looks wrong.

2. **Install the tools:**
   ```bash
   pip install pylint bandit flake8
   ```

3. **Run the analysis** and save the reports:
   ```bash
   pylint flight_reservation_system.py > pylint_report.txt
   bandit -r flight_reservation_system.py > bandit_report.txt
   flake8 flight_reservation_system.py > flake8_report.txt
   ```

4. **Document the issues** in `issues.md` using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | ... | ... | ... | ... | ... |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

6. **Reflect.** Answer the four reflection questions from the handout in `reflection.md`.

## Deliverables

1. `flight_reservation_system.py`: your cleaned version, with at least 4 issues fixed.
2. `issues.md`: the completed issue table.
3. `reflection.md`: your answers to the reflection questions.

**Target:** aim for a Pylint score above 9.5 on your final file. A perfect 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.

## Automatic quality and security checks (GitHub Actions)

The workflow in `.github/workflows/python-checks.yml` runs automatically on every
push and pull request. You can also start it manually from the **Actions** tab.
It runs three independent checks on Python 3.12:

- **Pylint** checks code quality.
- **Flake8** checks style and common programming errors.
- **Bandit** checks for common security issues.

All three checks run even if one fails. A finding causes that check to fail;
open its job in the Actions run to see the details. No repository secrets are needed.
The program currently uses only Python's standard library, so CI only installs
the analysis tools listed in `requirements-ci.txt`.

### Activate the pipeline

From the repository folder, commit and push the new configuration:

```bash
git add .github/workflows/python-checks.yml requirements-ci.txt README.md
git commit -m "Add Python quality and security CI"
git push origin main
```

These commands stage only the CI configuration and README. If your cleaned Python
file is still an uncommitted local change, review and commit it too: GitHub checks
the committed code, not your local working copy.

Open the repository on GitHub and select **Actions → Python quality and security**
to view the automatic run. For a manual run, select **Run workflow** and choose
`main`. If Actions is disabled, a repository administrator must enable it under
**Settings → Actions → General** and allow the actions used by this workflow.
Organization policy may require an administrator's help.

To require passing checks before merging, a repository administrator can add a
branch rule/ruleset for `main` under **Settings**, enable required status checks,
and select `pylint`, `flake8`, and `bandit` after their first run. Use pull requests
for subsequent changes.

### Run the same checks locally

Install into an activated virtual environment:

```bash
python -m pip install -r requirements-ci.txt
python -m pylint flight_reservation_system.py
python -m flake8 flight_reservation_system.py --count --show-source --statistics
python -m bandit -r flight_reservation_system.py
```

The existing saved reports show Pylint warnings for `total_revenue`, use of
`global`, and a missing final newline; Flake8 also reports the missing newline.
These need to be resolved for all checks to pass. The workflow does not suppress
warnings or change the application code.

This pipeline provides continuous integration (CI). Deployment (CD) would need a
deployment target; this command-line lab project currently has none configured.
