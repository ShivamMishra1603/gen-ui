# GenUI - AI Wireframe to Code Generator

Transform your hand-drawn wireframes into functional HTML/CSS code using AI!

## Features

- **Drag & Drop Upload**: Easy image upload interface
- **AI-Powered**: Uses Google Gemini to analyze wireframes
- **Live Preview**: See your generated UI in real-time
- **Download Code**: Get clean HTML/CSS files

## Demo

![GenUI Demo](public/videos/demo.gif)

See GenUI in action! Upload your wireframe and watch it transform into clean, functional code.


## Tech Stack

**Frontend:**
- React.js - User interface framework
- CSS3 - Styling and responsive design
- HTML5 - Markup structure

**Backend:**
- Flask - Python web framework
- Python 3.8+ - Server-side programming
- Flask-CORS - Cross-origin resource sharing

**AI Integration:**
- Google Gemini API - AI-powered code generation
- Image processing for wireframe analysis





## Quick Start

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

### 1. Clone & Setup

```bash
# Navigate to your project directory
cd gen-ui

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# In the backend folder, copy env_example.txt to create .env file
cd backend
cp env_example.txt .env

# Then edit .env file and replace with your actual API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 4. Open Your Browser

Visit `http://localhost:3000` and start generating UI from your wireframes!



## How to Use

1. **Upload**: Drag & drop or click to upload your wireframe image
2. **Generate**: Click "Generate UI Code" button
3. **Preview**: Toggle between code view and live preview
4. **Download**: Save the generated HTML file




## Troubleshooting

**"API key not found" error:**
- Make sure `.env` file exists in backend folder
- Check that `GOOGLE_API_KEY` is set correctly

**CORS errors:**
- Ensure Flask-CORS is installed: `pip install flask-cors`
- Check that backend is running on port 5000

**File upload issues:**
- Supported formats: PNG, JPG, JPEG, GIF, BMP
- Maximum file size: 16MB

## Example Wireframes

For best results, your wireframes should include:
- Clear layout structure
- Labeled sections (header, nav, content, footer)
- Basic UI elements (buttons, forms, images)
- Readable text (even if handwritten)

## Result

![Generated UI Output](public/images/output.png)

