

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-teal-400 mb-4">
            WixBuddy Frontend
          </h1>
          <p className="text-gray-300 text-lg">
            Your AI-Powered Partner for Compliance, Innovation, and Growth
          </p>
        </header>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div className="card">
            <h3 className="text-xl font-semibold text-teal-400 mb-3">
              Project Setup Complete
            </h3>
            <p className="text-gray-300">
              React + TypeScript + Vite foundation is ready with Tailwind CSS configured.
            </p>
          </div>
          
          <div className="card">
            <h3 className="text-xl font-semibold text-teal-400 mb-3">
              Dependencies Installed
            </h3>
            <p className="text-gray-300">
              React Router, Axios, React Hook Form, Zod, and React Query are ready to use.
            </p>
          </div>
          
          <div className="card">
            <h3 className="text-xl font-semibold text-teal-400 mb-3">
              Ready for Development
            </h3>
            <p className="text-gray-300">
              Project structure created with components, pages, hooks, and services folders.
            </p>
          </div>
        </div>
        
        <div className="text-center mt-8">
          <button className="btn-primary mr-4">
            Get Started
          </button>
          <button className="btn-outline">
            View Documentation
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
