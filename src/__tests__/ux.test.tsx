import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../app/page';

describe('Home Page UX', () => {
  it('renders links with screen reader text for new tabs', () => {
    render(<Home />);

    // Check for "Deploy now" link
    const deployLink = screen.getByRole('link', { name: /deploy now/i });
    expect(deployLink).toBeInTheDocument();
    expect(deployLink).toHaveAttribute('target', '_blank');
    // Verify sr-only text is present (querying by text includes sr-only content)
    expect(screen.getAllByText('(opens in a new tab)').length).toBeGreaterThan(0);
  });

  it('renders links with focus visibility classes', () => {
    render(<Home />);

    const deployLink = screen.getByRole('link', { name: /deploy now/i });
    expect(deployLink).toHaveClass('focus-visible:ring-2');
  });
});
