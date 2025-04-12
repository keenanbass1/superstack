import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button Component', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument()
  })

  it('handles click events', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    fireEvent.click(screen.getByRole('button', { name: /click me/i }))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('renders different variants', () => {
    const { rerender } = render(<Button variant="primary">Primary</Button>)
    expect(screen.getByRole('button', { name: /primary/i })).toHaveClass('bg-blue-600')
    
    rerender(<Button variant="secondary">Secondary</Button>)
    expect(screen.getByRole('button', { name: /secondary/i })).toHaveClass('bg-gray-200')
    
    rerender(<Button variant="outline">Outline</Button>)
    expect(screen.getByRole('button', { name: /outline/i })).toHaveClass('border')
    
    rerender(<Button variant="ghost">Ghost</Button>)
    expect(screen.getByRole('button', { name: /ghost/i })).not.toHaveClass('bg-blue-600')
  })

  it('renders different sizes', () => {
    const { rerender } = render(<Button size="sm">Small</Button>)
    expect(screen.getByRole('button', { name: /small/i })).toHaveClass('px-3')
    
    rerender(<Button size="md">Medium</Button>)
    expect(screen.getByRole('button', { name: /medium/i })).toHaveClass('px-4')
    
    rerender(<Button size="lg">Large</Button>)
    expect(screen.getByRole('button', { name: /large/i })).toHaveClass('px-5')
  })

  it('renders as a child element when asChild is true', () => {
    render(
      <Button asChild>
        <a href="https://example.com">Link Button</a>
      </Button>
    )
    
    const linkButton = screen.getByText(/link button/i)
    expect(linkButton.tagName).toBe('A')
    expect(linkButton).toHaveAttribute('href', 'https://example.com')
  })

  it('applies additional className when provided', () => {
    render(<Button className="custom-class">Custom Class</Button>)
    expect(screen.getByRole('button', { name: /custom class/i })).toHaveClass('custom-class')
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>)
    expect(screen.getByRole('button', { name: /disabled/i })).toBeDisabled()
  })
})
