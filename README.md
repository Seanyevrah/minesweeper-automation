# Minesweeper Automation

This repository contains the final project for **CMSC 122 (Data Structures and Algorithms)** at the **University of the Philippines Tacloban College** for the First Semester, AY 2024-2025.

## Project Overview

This project is an automated version of the classic **Minesweeper** puzzle board game. It is designed to demonstrate the effective use of data structures and algorithms in a gaming environment, specifically focusing on grid management, state persistence, and automated problem resolution.

### Key Features

* **User Interaction**: Players can manually reveal cells, flag potential mines, and track their moves.


* **In-Place Solution Building**: Users have access to all puzzle components on-screen and can replace or interact with them in real-time.


* **Automated Solver**: At any point, a user can request the program to solve the remaining puzzle based on the current configuration.


* **State Persistence**: Support for saving and loading game progress using the `pickle` module.
* **Visual Feedback**: Includes a custom reveal animation for mines upon game over or successful resolution.

---

## Technical Specifications

Technology Stack 

* **Language**: Python 3.x
* **Library**: `pygame` (Graphics and Event Handling)
* **GUI Utilities**: `tkinter` (Message boxes)
* **Data Persistence**: `pickle`

Data Structures Used 

1. **2D Array (Grid)**: Used to represent the puzzle structure and maintain the state of each `Cell` object.


2. **Double-Ended Queue (`collections.deque`)**: Utilized in the `flood_fill` algorithm to efficiently manage the queue of cells to be revealed during empty-space expansion.
3. **Objects/Classes**: Encapsulates cell properties (coordinates, mine status, neighbor count) to ensure clean operations.



Algorithm Complexity 

| Algorithm | Data Structure | Time Complexity | Space Complexity |
| --- | --- | --- | --- |
| **Flood Fill (Reveal)** | `deque` | $O(N \times M)$ | $O(N \times M)$ |
| **Puzzle Solver** | Nested Loops / Grid | $O((N \times M)^2)$ | $O(1)$ (In-place) |

---

## Installation and Execution

1. **Clone the repository**:
```bash
git clone https://github.com/YourUsername/Minesweeper-DS-Automator.git

```


2. **Install dependencies**:
```bash
pip install pygame

```


3. **Run the application**:
```bash
python main.py

```



---
