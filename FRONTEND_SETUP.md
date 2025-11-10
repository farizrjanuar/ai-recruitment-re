# AI Recruitment System - Frontend Setup

## Overview

This is the React frontend for the AI Recruitment System. It provides a user-friendly interface for HR professionals to manage candidates, job positions, and view recruitment analytics.

## Prerequisites

- Node.js 14+ and npm
- Backend API running (default: http://localhost:5000)

## Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the root directory:
```bash
REACT_APP_API_URL=http://localhost:5000/api
```

## Running the Application

Start the development server:
```bash
npm start
```

The application will open at http://localhost:3000

## Features

### Authentication
- User registration and login
- JWT-based authentication
- Role-based access control (Admin, HR)

### Dashboard
- Statistics overview (total candidates, jobs, avg match scores)
- Visual charts for skill distribution
- Experience level distribution
- Match score distribution
- Recent candidates list

### Candidate Management
- Upload CV files (PDF, DOCX, TXT)
- View candidate list with pagination and filtering
- Detailed candidate profiles with extracted information
- View match scores for all job positions

### Job Management
- Create and edit job positions
- View job list
- View job details with matched candidates
- Filter candidates by match score and qualification status

### Navigation
- Responsive navbar with role-based menu items
- Protected routes requiring authentication
- 404 page for invalid routes

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── Login.js
│   ├── Register.js
│   ├── ProtectedRoute.js
│   ├── Navbar.js
│   └── NotFound.js
├── context/            # React context providers
│   └── AuthContext.js
├── pages/              # Page components
│   ├── Dashboard.js
│   ├── UploadCV.js
│   ├── CandidateList.js
│   ├── CandidateDetail.js
│   ├── JobList.js
│   ├── JobForm.js
│   └── JobDetail.js
├── services/           # API service modules
│   ├── api.js
│   ├── authAPI.js
│   ├── candidateAPI.js
│   ├── jobAPI.js
│   └── dashboardAPI.js
├── App.js             # Main application component
└── index.js           # Application entry point
```

## API Integration

The frontend communicates with the backend API using Axios. All API calls are configured in the `src/services/` directory:

- **api.js**: Base Axios configuration with interceptors
- **authAPI.js**: Authentication endpoints
- **candidateAPI.js**: Candidate management endpoints
- **jobAPI.js**: Job position endpoints
- **dashboardAPI.js**: Dashboard analytics endpoints

### JWT Token Management

- Tokens are stored in localStorage
- Automatically attached to requests via Axios interceptor
- Expired tokens trigger automatic logout and redirect to login

## Building for Production

Create a production build:
```bash
npm run build
```

The build files will be in the `build/` directory.

## Deployment

### Vercel (Recommended)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variable in Vercel dashboard:
   - `REACT_APP_API_URL`: Your backend API URL

### Other Platforms

The application can be deployed to any static hosting service:
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Firebase Hosting

## Environment Variables

- `REACT_APP_API_URL`: Backend API base URL (default: http://localhost:5000/api)

## Troubleshooting

### CORS Issues
Ensure the backend has CORS configured to allow requests from your frontend domain.

### API Connection Failed
- Verify the backend is running
- Check the `REACT_APP_API_URL` environment variable
- Check browser console for detailed error messages

### Authentication Issues
- Clear localStorage and try logging in again
- Verify JWT token is being sent in request headers
- Check backend authentication configuration

## Available Scripts

- `npm start`: Run development server
- `npm run build`: Create production build
- `npm test`: Run tests
- `npm run eject`: Eject from Create React App (irreversible)

## Technologies Used

- React 19.2
- React Router DOM (routing)
- Axios (HTTP client)
- Chart.js & react-chartjs-2 (data visualization)
- CSS3 (styling)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
