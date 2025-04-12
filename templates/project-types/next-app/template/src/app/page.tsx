import { Button } from '@/components/ui/Button'

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-6">
          Welcome to <span className="text-blue-600">{{projectName}}</span>
        </h1>
        
        <p className="text-lg text-gray-600 mb-8">
          Get started by editing <code className="bg-gray-100 p-1 rounded">src/app/page.tsx</code>
        </p>
        
        <div className="max-w-2xl mx-auto grid gap-8 mb-12">
          <div className="border rounded-lg p-6 text-left">
            <h2 className="text-xl font-semibold mb-2">Features</h2>
            <ul className="list-disc pl-5 space-y-1">
              <li>Next.js 14 with App Router</li>
              <li>TypeScript for type safety</li>
              <li>Tailwind CSS for styling</li>
              <li>ESLint for code quality</li>
              <li>Jest for testing</li>
            </ul>
          </div>
        </div>
        
        <div className="flex gap-4 justify-center">
          <Button variant="primary" onClick={() => console.log('Clicked!')}>
            Get Started
          </Button>
          <Button variant="outline" asChild>
            <a href="https://nextjs.org/docs" target="_blank" rel="noopener noreferrer">
              Documentation
            </a>
          </Button>
        </div>
      </div>
    </div>
  )
}
