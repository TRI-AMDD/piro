import { fireEvent, render, screen } from '@testing-library/react';
import Counter from './Counter';

test('renders count', () => {
    render(<Counter />);
    const countElement = screen.getByText('Count: 0');
    expect(countElement).toBeInTheDocument();

    // clicking increment increases the counter
    const incButton = screen.getByText('Increment');
    fireEvent.click(incButton);
    screen.getByText('Count: 1');
});
