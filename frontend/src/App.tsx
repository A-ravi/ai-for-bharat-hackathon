import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 2,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="app">
          <h1>Jal Sathi - जल साथी</h1>
          <p>AI-powered irrigation advisor for Indian farmers</p>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
