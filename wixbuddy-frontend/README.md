# WixBuddy Frontend

A modern React + TypeScript frontend application for WixBuddy, an AI-powered assistant platform for the road transport industry.

## 🚀 Project Setup Complete

This project has been initialized with:

- ✅ **React 19** with TypeScript for type safety
- ✅ **Vite** for fast development and optimized builds
- ✅ **Tailwind CSS** with custom dark theme and teal accent colors
- ✅ **Project Structure** organized with components, pages, hooks, services, types, utils, contexts, and assets folders

## 📦 Dependencies Installed

### Core Dependencies
- `react` & `react-dom` - React framework
- `react-router-dom` - Client-side routing
- `axios` - HTTP client for API communication
- `react-hook-form` - Form handling with validation
- `@hookform/resolvers` & `zod` - Form validation schemas
- `@tanstack/react-query` - Server state management

### Development Dependencies
- `typescript` - Type checking
- `tailwindcss` - Utility-first CSS framework
- `@tailwindcss/forms` & `@tailwindcss/typography` - Tailwind plugins
- `eslint` & `prettier` - Code linting and formatting
- `@vitejs/plugin-react` - Vite React plugin

## 🎨 Styling

The project uses Tailwind CSS with a custom dark theme:
- **Background**: Dark gray tones (`bg-gray-900`, `bg-gray-800`)
- **Accent Color**: Teal (`text-teal-400`, `bg-teal-600`)
- **Typography**: Inter font family
- **Custom Components**: Pre-built button and form styles

## 🏗️ Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Basic UI components (Button, Input, etc.)
│   ├── forms/          # Form-specific components
│   └── layout/         # Layout components (Header, Sidebar, etc.)
├── pages/              # Page components
├── hooks/              # Custom React hooks
├── services/           # API service functions
├── types/              # TypeScript type definitions
├── utils/              # Utility functions
├── contexts/           # React contexts
└── assets/             # Static assets
```

## 🚀 Getting Started

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```

## 🔧 Configuration

- **Environment Variables**: Configure API endpoints in `.env`
- **Tailwind Config**: Custom theme in `tailwind.config.js`
- **TypeScript**: Strict mode enabled with path aliases (`@/*`)
- **ESLint & Prettier**: Code quality and formatting rules configured

## 📋 Next Steps

The project foundation is ready! You can now:

1. Start implementing the authentication system (Task 2-3)
2. Build core UI components (Task 4-5)
3. Create the landing page and other pages (Task 6-12)
4. Add responsive design and optimizations (Task 13-19)

## 🎯 Features to Implement

Based on the Figma designs, this frontend will include:
- User authentication and registration
- Account settings with profile management
- Landing page with hero section and features
- Training video library
- FAQ section with search functionality
- Multi-step onboarding questionnaire
- Responsive design for all devices

## 🔗 API Integration

The frontend is configured to connect to the Django backend API:
- Base URL: `http://localhost:8000/api` (configurable via environment variables)
- Authentication: JWT token-based
- Error handling: Centralized with user-friendly messages