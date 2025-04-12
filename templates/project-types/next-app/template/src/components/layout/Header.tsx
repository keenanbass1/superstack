import Link from 'next/link'
import { Button } from '../ui/Button'

interface NavItem {
  label: string
  href: string
}

const navItems: NavItem[] = [
  { label: 'Home', href: '/' },
  { label: 'About', href: '/about' },
  { label: 'Contact', href: '/contact' },
]

export function Header() {
  return (
    <header className="bg-white shadow dark:bg-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 text-xl font-bold text-blue-600 dark:text-blue-400 no-underline">
              {{projectName}}
            </Link>
          </div>
          
          <nav className="hidden md:flex space-x-4">
            {navItems.map((item) => (
              <Link 
                key={item.href}
                href={item.href}
                className="px-3 py-2 text-gray-700 hover:text-blue-600 dark:text-gray-200 dark:hover:text-blue-400 no-underline"
              >
                {item.label}
              </Link>
            ))}
            <Button variant="primary" size="sm">
              Get Started
            </Button>
          </nav>
          
          <div className="md:hidden">
            {/* Mobile menu button would go here */}
            <button className="p-2 rounded-md text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
              <span className="sr-only">Open menu</span>
              {/* Menu icon */}
              <svg 
                className="h-6 w-6" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M4 6h16M4 12h16M4 18h16" 
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
