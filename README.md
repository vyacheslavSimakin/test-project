<p align="center"><h1 align="center">TEST-PROJECT</h1></p>
<p align="center">
	<em><code>❯ Test management system. </code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/vyacheslavSimakin/test-project?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/vyacheslavSimakin/test-project?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/vyacheslavSimakin/test-project?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/vyacheslavSimakin/test-project?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

##  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Overview

This is a demo TMS project, which will include:
- Backend part, developed based on FastAPI and PostgreSQL.
- Documentation part, User stories, designs, diagrams.
- Manual testing part, test cases, test runs, bug reports.
- Automated Integration tests, developed in python with pytest and httpx.
- Deployment part, Dockerfile, Kubernetes deployment files.

---

##  Features

- Users management.
- Test cases management.
- Test runs management.
- Test executions management.
- Test suits management.

---

##  Project Structure

```sh
└── test-project/
    ├── Dockerfile
    ├── app
    │   ├── __init__.py
    │   ├── db
    │   │   ├── __init__.py
    │   │   └── postgress.py
    │   ├── dependencies.py
    │   ├── logic
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   │   ├── steps_logic.py
    │   │   ├── tc_logic.py
    │   │   └── users_logic.py
    │   ├── main.py
    │   ├── models.py
    │   └── routers
    │       ├── __init__.py
    │       ├── login.py
    │       ├── tc_router.py
    │       └── users.py
    ├── deployment
    │   ├── postgres-configmap.yaml
    │   ├── postgres-pvc.yaml
    │   └── tms-namespace.yaml
    ├── docs
    │   ├── manual tests
    │   │   ├── Bug reports.pdf
    │   │   ├── Test cases.pdf
    │   │   └── Test run.pdf
    │   └── user_stories.txt
    └── requirements.txt
```


###  Project Index
<details open>
	<summary><b><code>TEST-PROJECT/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/requirements.txt'>requirements.txt</a></b></td>
				<td><code>❯ </code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/Dockerfile'>Dockerfile</a></b></td>
				<td><code>❯ </code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- deployment Submodule -->
		<summary><b>deployment</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/deployment/postgres-pvc.yaml'>postgres-pvc.yaml</a></b></td>
				<td><code>❯ </code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/deployment/postgres-configmap.yaml'>postgres-configmap.yaml</a></b></td>
				<td><code>❯ </code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/deployment/tms-namespace.yaml'>tms-namespace.yaml</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- app Submodule -->
		<summary><b>app</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/dependencies.py'>dependencies.py</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/main.py'>main.py</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/models.py'>models.py</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
			<details>
				<summary><b>routers</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/routers/tc_router.py'>tc_router.py</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/routers/users.py'>users.py</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/routers/login.py'>login.py</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>logic</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/logic/steps_logic.py'>steps_logic.py</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/logic/users_logic.py'>users_logic.py</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/logic/auth.py'>auth.py</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/logic/tc_logic.py'>tc_logic.py</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>db</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/vyacheslavSimakin/test-project/blob/master/app/db/postgress.py'>postgress.py</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with test-project, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip
- **Container Runtime:** Docker


###  Installation

Install test-project using one of the following methods:

**Build from source:**

1. Clone the test-project repository:
```sh
❯ git clone https://github.com/vyacheslavSimakin/test-project
```

2. Navigate to the project directory:
```sh
❯ cd test-project
```

3. Install the project dependencies:


**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```


**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker build -t vyacheslavSimakin/test-project .
```




###  Usage
Run test-project using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python {entrypoint}
```


**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker run -it {image_name}
```


###  Testing
Run the test suite using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pytest
```


---
##  Project Roadmap
- [X] **`Task 0`**: <strike>Create user stories and manual test cases.</strike>
- [X] **`Task 1`**: <strike>Implement users feature.</strike>
- [ ] **`Task 2`**: Implement Test Cases feature.
- [ ] **`Task 4`**: Execute manual test cases and create bug reports if any.
- [ ] **`Task 5`**: Implement Test Automation for Users and Test Cases features.
- [ ] **`Task 5`**: Implement Test Runs feature.
- [ ] **`Task 6`**: Write Deployment part.
- [ ] **`Task 7`**: Implement Test Automation for Test Run feature.

---

