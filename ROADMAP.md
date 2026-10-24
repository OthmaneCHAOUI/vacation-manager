# Vacation Manager roadmap

Last reviewed: 10/24/2026

This roadmap separates DONE work, active defects, product decisions, and
future improvements.

---

## 1. Persistence and data features

### DONE

- [x] Add SQLite persistence for employees and vacation requests.
- [x] Add employee and vacation tables with a foreign-key relationship.
- [x] Add indexes for employee lookups and vacation date ranges.
- [x] Initialize the schema automatically when the application starts.
- [x] Add a persistent per-user database location for packaged applications.
- [x] Seed a packaged installation from the bundled database when no user
  database exists.

### TODO

- [ ] Add explicit schema versioning and migrations instead of relying only on
  `CREATE TABLE IF NOT EXISTS` and ad hoc column checks.
- [ ] Define and enforce the data rules for names, dates, statuses, allowance
  values, carryover days, and used days.
- [ ] Add a single transaction for creating a vacation and updating the
  employee's used-day total.
- [ ] Recalculate `employee.vacation_used` from vacation records after
  deletion, editing, migration, or recovery.
- [ ] Decide whether pending, approved, and rejected requests count toward
  allowance usage, then enforce that policy consistently.
- [ ] Decide whether overlapping vacation periods are allowed and validate the
  chosen rule.
- [ ] Add database backup, restore, and export options.
- [ ] Add fixtures and a clean temporary database for automated tests.

---

## 2. Application and UI

### DONE

- [x] Set up the PyQt5 desktop application with an MVC-inspired structure.
- [x] Add the application entry point and main window.
- [x] Add Employees, Vacations, and Calendar sections.
- [x] Add employee creation, table display, inline editing, and deletion.
- [x] Add vacation creation, table display, and deletion.
- [x] Add date-range validation when creating vacations.
- [x] Add an allowance check before creating a vacation.
- [x] Add employee filtering and vacation-day highlighting in the calendar.
- [x] Add custom styling, application icon, and keyboard close shortcut.

### TODO

- [ ] Add a dedicated Today button to return the calendar to the current date.
- [ ] Add a clear empty state and refresh action for employee and vacation
  lists.
- [ ] Add loading, success, and failure feedback for all database operations.
- [ ] Replace repeated inline widget styles with reusable style resources.
- [ ] Add responsive layouts for smaller screens instead of relying on a
  maximized window.
- [ ] Add accessible labels, keyboard navigation, focus states, and consistent
  dialog behavior.
- [ ] Add confirmation and undo/recovery behavior for destructive actions.
- [ ] Add search, sorting, and filtering to employee and vacation tables.

---

## 3. Calendar and vacation workflow

### DONE

- [x] Navigate the calendar.
- [x] Highlight vacation days.
- [x] Highlight the current day.
- [x] Filter the calendar by employee.
- [x] Apply custom calendar styling.

### TODO

- [ ] Define whether the employee selector should show the nearest upcoming
  vacation, the current vacation, or all matching periods.
- [ ] Change the current selection behavior from “latest created request” to
  the documented nearest/current/upcoming vacation rule.
- [ ] Add a Today button and preserve the selected employee when navigating.
- [ ] Add a multi-day selection workflow for quickly assigning a vacation.
- [ ] Add an optional reason field to the vacation form and display it in the
  vacation table and details view.
- [ ] Add status controls for pending, approved, and rejected requests if an
  approval workflow is in scope.
- [ ] Show all vacation periods for an employee, not only one selected period.
- [ ] Add clear visual states for past, current, upcoming, and rejected
  requests.

---

## 4. Features still missing or incomplete

- [ ] Add import and export for employees and vacations, with a documented
  format such as CSV or JSON or PDF.
- [ ] Validate imported data before modifying the database and provide an
  import summary with rejected rows.
- [ ] Add vacation editing, not only creation and deletion.
- [ ] Add employee detail and vacation detail views.
- [ ] Add annual allowance rollover and year-based vacation accounting.
- [ ] Add an overview/dashboard with totals, upcoming absences, and remaining
  allowance.
- [ ] Add optional authentication and role-based access control if the
  application will be shared by multiple users.
- [ ] Clarify whether notifications, approvals, holidays, weekends, and
  regional calendars are in scope.
- [ ] Decide whether the application remains local-only or should support a
  shared/network database.

---

## 5. Reliability and logic

### DONE

- [x] Add corruption checking at startup and recreate the database after a
  detected SQLite error.
- [x] Use parameterized SQL for normal model operations.
- [x] Create the database directory before opening the database.
- [x] Use a persistent writable location for packaged application data.

### TODO

- [ ] Replace broad exception handling with specific database and file errors,
  while showing an actionable error to the user.
- [ ] Ensure a failed database write cannot leave the UI and stored data out of
  sync.
- [ ] Handle missing, unreadable, locked, or permission-denied database files
  explicitly.
- [ ] Make foreign-key enforcement explicit for every SQLite connection.
- [ ] Validate empty, malformed, negative, and non-numeric employee inputs
  before calling `int(...)`.
- [ ] Prevent invalid date ranges, invalid statuses, and negative allowance
  values at both UI and model boundaries.
- [ ] Consolidate duplicated or unused vacation model operations.
- [ ] Move business rules out of views and controllers into testable services
  or model-level helpers.
- [ ] Define logging and error-reporting behavior for production builds.

---

## 6. Structure and maintainability

### Current state

- [x] Keep models, views, controllers, database code, styles, and assets in
  separate directories.
- [x] Keep the application organized as an MVC-inspired desktop project.

### TODO

- [ ] Complete the refactor of misplaced functions and logic currently handled
  by the wrong layers.
- [ ] Establish clear interfaces between views, controllers, and models.
- [ ] Remove empty constructors and unused imports or methods.
- [ ] Introduce shared types or data-transfer objects for employee and vacation
  records.
- [ ] Centralize date calculations, allowance calculations, and validation.
- [ ] Add consistent formatting, linting, and type-checking configuration.
- [ ] Document architectural boundaries and data-flow decisions.
- [ ] Keep resource paths independent of the current working directory in every
  view and service.

---

## 7. Tests and verification

### DONE

- [x] Confirm that the current Python source compiles with
  `python -m compileall -q src`.
- [x] Verify that the PyInstaller specification builds successfully.

### TODO

- [ ] Add automated model tests for employee creation, update, deletion, and
  lookup.
- [ ] Add automated model tests for vacation creation, listing, deletion, and
  employee relationships.
- [ ] Add tests for date ranges, inclusive day counts, allowance limits,
  carryover, and used-day recalculation.
- [ ] Add migration tests against both a fresh database and older schemas.
- [ ] Add controller tests for refresh behavior and failure handling.
- [ ] Add focused UI tests for form validation, selection, deletion
  confirmation, and calendar highlighting.
- [ ] Add packaging smoke tests that inspect bundled styles, icons, and the
  database seed.
- [ ] Test persistence across application restarts for source and packaged
  builds.
- [ ] Test Windows packaging and document Linux/macOS support if required.
- [ ] Add a repeatable test command and include it in the README and CI.

---

## 8. Build, documentation, and operations

### DONE

- [x] Add PyInstaller packaging configuration.
- [x] Include stylesheets, icon assets, and the database seed in the bundle.
- [x] Resolve spec paths independently of the build working directory.
- [x] Disable the console window for normal GUI packaging.
- [x] Document source execution, packaging, database locations, and project
  structure in the README.
- [x] Document that PyInstaller builds are platform-specific.

### TODO

- [ ] Add a documented release checklist covering version, database migration,
  packaging, smoke tests, and rollback.
- [ ] Add CI for compilation, tests, linting, and a packaging smoke build.
- [ ] Add application version metadata and a visible version/about dialog.
- [ ] Document upgrade behavior for existing packaged databases.
- [ ] Document backup and recovery procedures.
- [ ] Produce platform-specific artifacts only on their target operating
  systems.
- [ ] Complete README demonstrations, screenshots, UML diagrams, and usage
  examples.
- [ ] Keep generated `build/`, `dist/`, and local database files out of source
  control while tracking the reproducible build configuration.

---

## 9. Security and privacy

- [ ] Decide whether authentication is required before exposing the application
  to multiple users.
- [ ] Define roles and permissions for viewing, editing, approving, deleting,
  importing, and exporting records.
- [ ] Protect exported files and document that they may contain personal data.
- [ ] Avoid logging employee names, vacation reasons, or database contents.
- [ ] Validate imported files and reject oversized or malformed input.
- [ ] Review file permissions for the per-user database and backups.
- [ ] Review SQL, path handling, packaging, and update procedures before
  distributing releases.

---

## Issues

| Severity | Problem | Fix | State |
|---|---|---|---|
| **High** | Vacation allowance calculation reads `vac["employee_id"]`, but `get_all_vacations()` does not select `employee_id`; adding a vacation can therefore fail with a missing-column lookup. | Include the employee ID in the query or calculate usage with a dedicated employee-scoped query, then add a regression test. | **Open** |
| **High** | The calendar employee selector highlights the latest-created vacation rather than the nearest current or upcoming vacation. | Define the intended selection rule and select the current or nearest upcoming period accordingly. | **Open** |
| **High** | `HomeView` catches every exception while loading employees with vacations and displays an empty state, masking database and schema failures. | Catch specific expected errors, log the failure, and show an actionable error state to the user. | **Open** |
| **Medium** | Deleting a vacation does not recalculate the employee's `vacation_used` value. | Recompute usage from the remaining records in the same transaction as deletion. | **Open** |
| **Medium** | Numeric employee fields are converted without complete validation. | Validate required, numeric, non-negative values at the view and model boundaries. | **Open** |
| **Medium** | The database schema is changed through an inline `reason` column check without versioned migrations. | Add migration versions and tests for fresh and existing databases. | **Open** |
| **Medium** | Vacation allowance policy is not defined for pending, approved, and rejected requests. | Choose the policy and apply it consistently to validation, totals, calendar display, and reports. | **Open** |
| **Medium** | The packaged database and resource paths were previously vulnerable to missing files or working-directory differences. | Bundle the database seed and resources, resolve paths from the application/spec location, and verify the packaged archive. | **Closed** |
| **Medium** | Packaging configuration was previously undocumented or inconsistent with the source tree. | Track `vacman.spec`, remove stale hidden imports, document platform-specific builds, and keep generated output ignored. | **Closed** |
| **Low** | The local database contains non-reproducible development data. | Use clean test databases and fixtures; keep the local database ignored. | **Open** |
| **Low** | The README and roadmap previously contained stale or inconsistent references and incomplete demonstration material. | Keep documentation synchronized with the actual modules, commands, features, and release behavior. | **Open** |
