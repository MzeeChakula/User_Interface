# MzeeChakula Frontend

Vue 3 + Vite PWA frontend for the MzeeChakula nutrition assistant.

## Features

- **Modern Vue 3** with Composition API and script setup
- **Progressive Web App (PWA)** - Install as a mobile/desktop app
- **Real-time Chat** - AI-powered nutrition assistant
- **Multilingual Support** - English, Luganda, Swahili (via Sunbird AI)
- **Offline Support** - Service worker for offline functionality
- **Responsive Design** - Mobile-first, works on all devices
- **TailwindCSS** - Modern utility-first styling

## Tech Stack

- **Framework**: Vue 3
- **Build Tool**: Vite
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios
- **Icons**: Lucide Vue Next
- **Styling**: TailwindCSS 4
- **PWA**: vite-plugin-pwa + Workbox

## Local Development

### Prerequisites

- Node.js 20+
- npm or yarn

### Setup

1. **Install dependencies**:

```bash
cd frontend
npm install
```

2.**Configure environment**:

```bash
cp .env.example .env
# Edit .env with your backend API URL
```

3.**Run development server**:

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
npm run preview
```

## API Integration

The frontend connects to the FastAPI backend through axios services located in `src/api/`:

- **auth.js** - User authentication (register, login, token management)
- **chat.js** - Chat messages with AI assistant
- **ai.js** - Translation, language detection, RAG queries
- **predict.js** - Caloric predictions and food recommendations
- **client.js** - Axios client with interceptors

### Environment Variables

- `VITE_API_BASE_URL` - Backend API URL (default: <http://localhost:8000>)

## Project Structure

```bash
frontend/
├── public/
│   └── icons/              # App icons and assets
├── src/
│   ├── api/                # API service layer
│   │   ├── client.js       # Axios client
│   │   ├── auth.js         # Auth endpoints
│   │   ├── chat.js         # Chat endpoints
│   │   ├── ai.js           # AI services
│   │   └── predict.js      # Predictions
│   ├── components/         # Reusable components
│   ├── composables/        # Vue composables
│   ├── stores/             # Pinia stores
│   │   ├── auth.js         # Authentication state
│   │   ├── chat.js         # Chat state
│   │   ├── profile.js      # User profile
│   │   └── app.js          # App settings
│   ├── views/              # Page components
│   │   ├── Auth.vue        # Login/Register
│   │   ├── Chat.vue        # Main chat interface
│   │   ├── Profile.vue     # User profile
│   │   └── Settings.vue    # App settings
│   ├── router/             # Vue Router config
│   ├── App.vue             # Root component
│   └── main.js             # App entry point
├── Dockerfile              # Production container
├── nginx.conf              # Nginx configuration
└── vite.config.js          # Vite configuration
```

## Deployment

### Docker

```bash
# Build
docker build -t mzeechakula-frontend \
  --build-arg VITE_API_BASE_URL=https://your-backend-url.com .

# Run
docker run -p 80:80 mzeechakula-frontend
```

### Render

The app is configured for deployment on Render using the `render.yaml` in the project root.

1. Push to GitHub
2. Connect repository to Render
3. Render will automatically deploy both frontend and backend services

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run generate-pwa-assets` - Generate PWA icons

## Progressive Web App

The app is installable as a PWA with:

- Offline support via service worker
- Install prompts on mobile and desktop
- App icons and manifest
- Background sync for messages (coming soon)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details
