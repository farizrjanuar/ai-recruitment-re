# AI Recruitment System

An intelligent recruitment platform that automates CV screening, candidate matching, and job position management using AI and machine learning.

## Features

- **CV Upload & Parsing**: Automatically extract information from PDF, DOCX, and TXT resumes
- **Skill Analysis**: AI-powered skill extraction and categorization using NLP
- **Smart Matching**: Match candidates to job positions using ML algorithms
- **HR Dashboard**: Comprehensive analytics and candidate management interface
- **Secure Authentication**: JWT-based authentication with role-based access control

## Tech Stack

**Frontend:**
- React 19.2
- React Router
- Axios
- Chart.js

**Backend:**
- Python 3.9+ / Flask
- SQLAlchemy (PostgreSQL/SQLite)
- spaCy (NLP)
- scikit-learn (ML)

## Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)


## Local Development Setup

### Prerequisites

- Node.js 16+ and npm
- Python 3.9+
- pip

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file from example:
```bash
cp .env.example .env
```

3. Update `.env` with your backend URL:
```
REACT_APP_API_URL=http://localhost:5000
```

4. Start the development server:
```bash
npm start
```

The frontend will run on [http://localhost:3000](http://localhost:3000)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

5. Create `.env` file from example:
```bash
cp .env.example .env
```

6. Initialize database:
```bash
python init_db.py
```

7. Run the development server:
```bash
python app.py
```

The backend will run on [http://localhost:5000](http://localhost:5000)

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for both frontend and backend.

### Quick Deployment Links

- **Frontend (Vercel)**: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/ai-recruitment)
- **Backend (Render)**: Use `render.yaml` for one-click deployment
- **Backend (Railway)**: Use `railway.json` for one-click deployment

## Project Structure

```
ai-recruitment/
├── backend/                 # Flask backend
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   ├── ml/                 # ML components
│   ├── routes/             # API endpoints
│   ├── utils/              # Helper functions
│   ├── app.py              # Application entry point
│   ├── config.py           # Configuration
│   └── requirements.txt    # Python dependencies
├── src/                    # React frontend
│   ├── components/         # Reusable components
│   ├── pages/              # Page components
│   ├── services/           # API services
│   ├── context/            # React context
│   └── App.js              # Main app component
├── public/                 # Static assets
└── package.json            # Node dependencies
```

## API Documentation

The backend API provides the following endpoints:

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/candidates/upload` - Upload CV
- `GET /api/candidates` - List candidates
- `GET /api/candidates/:id` - Get candidate details
- `POST /api/jobs` - Create job position
- `GET /api/jobs` - List job positions
- `GET /api/jobs/:id` - Get job details
- `POST /api/matching/calculate/:candidate_id` - Calculate matches
- `GET /api/matching/job/:job_id` - Get candidates for job
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/dashboard/analytics` - Analytics data

For detailed API documentation, see `backend/routes/README_*.md` files.

## Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000
```

### Backend (backend/.env)
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///recruitment.db
MAX_FILE_SIZE=5242880
UPLOAD_FOLDER=uploads
CORS_ORIGINS=http://localhost:3000
```

## License

This project is licensed under the MIT License.
