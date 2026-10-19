# 💎 Computer Vision Based Virtual Jewellery Try-On Using Deep Learning

A full-stack virtual jewellery try-on application designed to help customers visualize how jewellery may look on them before making a purchase. The project combines web development, computer vision, and deep learning concepts to explore a more interactive and convenient jewellery shopping experience.

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [How It Works](#-how-it-works)
- [Applications](#-applications)
- [Future Enhancements](#-future-enhancements)
- [Research Work](#-research-work)
- [Author](#-author)

## 🚀 Overview

Online jewellery shopping often makes it difficult for customers to visualize how earrings and necklaces will look on them. Traditional physical try-ons can also require additional handling of delicate and expensive jewellery.

**Computer Vision Based Virtual Jewellery Try-On Using Deep Learning** aims to address these challenges by developing a web-based application that explores virtual jewellery placement using computer vision and image-processing techniques.

The application is being developed with a React frontend and a FastAPI backend, with the goal of providing an intuitive interface for jewellery selection and visualization.

## 🎯 Problem Statement

Traditional online jewellery shopping generally relies on static product images, which do not provide a personalized preview of how an item might look on an individual. Physical try-ons may also involve handling risks, hygiene concerns, and additional effort for jewellery retailers.

This project explores a computer-vision-based solution that can help customers visualize jewellery and support a more engaging digital shopping experience.

## 🎯 Objectives

- Develop an interactive web application for virtual jewellery try-on.
- Explore computer vision techniques for detecting relevant facial landmarks.
- Position and scale jewellery overlays according to detected landmarks.
- Integrate a React frontend with a Python-based backend.
- Reduce dependence on repeated physical try-ons for initial product visualization.
- Explore the potential of AI-assisted jewellery visualization for online retail.

## ✨ Key Features

- **Interactive web interface:** A user-friendly frontend for jewellery visualization.
- **Jewellery visualization:** Designed to support earrings and necklaces.
- **Computer vision integration:** Uses facial landmark detection concepts for jewellery placement.
- **Full-stack architecture:** React frontend integrated with a FastAPI backend.
- **Image processing:** Supports the development of jewellery overlay and positioning workflows.
- **Extensible design:** Can be expanded to accommodate additional jewellery categories and AI-based improvements.

*Feature availability depends on the current implementation. Planned functionality may not yet be available in the running application.*

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React.js, JavaScript, HTML, CSS |
| Backend | Python, FastAPI |
| Computer Vision | OpenCV, MediaPipe |
| Image Processing | NumPy, Pillow |
| Development Tools | Git, GitHub, Visual Studio Code |

*The table lists the technologies used or explored in the project. Confirm the repository's dependency files before treating every library as a current dependency.*

## 🏗️ System Architecture

The application follows a frontend-backend architecture.

```text
              User
               |
               v
       React Frontend
               |
               v
        FastAPI Backend
               |
               v
      Computer Vision Layer
       (Landmark Detection)
               |
               v
       Jewellery Placement
        and Image Processing
               |
               v
       Processed Try-On Result
               |
               v
        React Frontend
```

The frontend handles user interaction, while the backend is responsible for processing requests and coordinating the computer vision workflow.

## 📂 Project Structure

The following is an illustrative structure. Adjust it to match the actual folders in the repository.

```text
Virtual_Jewellery_try_on/
│
├── frontend/          # React application
├── backend/           # FastAPI application
├── jewellery/         # Jewellery image assets, if present
├── README.md
└── .gitignore
```

## ⚙️ Getting Started

### Prerequisites

Install the following tools before setting up the project:

- Python 3.12, if supported by the project's dependencies
- Node.js and npm
- Git
- Visual Studio Code or another code editor

### 1. Clone the Repository

```bash
git clone https://github.com/Dhanashreesonawane/Virtual_Jewellery_try_on.git
```

Navigate to the project directory:

```bash
cd Virtual_Jewellery_try_on
```

### 2. Set Up the Backend

Open a terminal in the project root and create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies using the requirements file in the backend directory, if present:

```bash
cd backend
pip install -r requirements.txt
```

Start the FastAPI server using the actual application module and entry point in your repository. For example, if the entry point is `main.py`:

```bash
uvicorn main:app --reload --port 8000
```

### 3. Set Up the Frontend

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed in the terminal.

**Important:** The commands above assume the project contains `backend/requirements.txt`, `backend/main.py`, and `frontend/package.json`. If your actual filenames or directory structure differ, update the commands accordingly.

## 🔄 How It Works

The intended workflow is:

1. **Start the application:** Open the web interface.
2. **Choose jewellery:** Select an available jewellery item.
3. **Provide visual input:** Use the supported camera or image-input workflow.
4. **Process the input:** The backend coordinates the computer vision and image-processing operations.
5. **Position the jewellery:** Use relevant detected landmarks to calculate the placement and scale of the jewellery overlay.
6. **Display the result:** Return the processed visualization to the frontend.

The precise workflow depends on the functionality implemented in the current version.

## 🌍 Potential Applications

- Online jewellery shopping platforms
- Jewellery retail stores and digital kiosks
- Product visualization for e-commerce
- Interactive customer experiences
- Research into augmented reality and computer vision

## 🔮 Future Enhancements

- Real-time webcam-based jewellery try-on
- More stable tracking as the user's face or head moves
- Improved jewellery alignment, rotation, and scaling
- Support for rings, bracelets, and bangles using hand tracking
- More realistic rendering, lighting, and occlusion handling
- Expanded jewellery catalog and product management
- Mobile-responsive design and deployment
- Performance evaluation under different lighting and pose conditions

## 📄 Research Work

This project is also associated with research into computer vision-based virtual jewellery try-on using deep learning.

The research explores the potential of combining landmark detection, image processing, and AI techniques to improve digital jewellery visualization.

**Publication status:** Research work in progress. No publication is claimed at this stage.

## 👩‍💻 Author

**Dhanashree Sonawane**

Electronics and Telecommunication Engineering Student  
Pune Institute of Computer Technology (PICT), Pune

- GitHub: [@Dhanashreesonawane](https://github.com/Dhanashreesonawane)
- LinkedIn: [Dhanashree Sonawane](https://www.linkedin.com/)

## ⭐ Support

If you find this project interesting, consider giving the repository a star on GitHub.

---

*Developed as an academic project exploring computer vision, deep learning, and full-stack web development.*
