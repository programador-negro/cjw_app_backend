# CJW Frontend

Vue.js frontend application for the CJW project.

## Requirements

- Node.js 20.x or later
- npm or yarn
- Docker and Docker Compose (for containerized deployment)

## Project Setup

### Installation

```bash
# Install dependencies
npm install
```

### Development

To run the development server:

```bash
# Start the development server
npm run dev
```

The application will be available at [http://localhost:5173](http://localhost:5173)

### Building for Production

```bash
# Build for production
npm run build
```

### Running with Docker Compose

The frontend can be run along with the backend and database services using Docker Compose:

```bash
# From the root directory
docker compose up
```

This will start:

- The Vue.js frontend on port 5173
- The backend service on port 8080
- The MySQL database on port 33061

### Environment Variables

The frontend service uses the following environment variables:

- `VITE_API_URL`: Backend API URL (default: http://localhost:8080)

## Features

- Modern Vue.js 3 with Composition API
- Vite for fast development and building
- Hot Module Replacement (HMR)
- TypeScript support
- Tailwind CSS for styling
- Axios for API requests
- Vue Router for navigation
- Pinia for state management

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── router/
│   ├── stores/
│   ├── views/
│   ├── App.vue
│   └── main.ts
├── .env
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```