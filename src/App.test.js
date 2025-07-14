import { render, screen } from '@testing-library/react';
import App from './App';

test('renders NEXA Game Recommender title', () => {
  render(<App />);
  const titleElement = screen.getByText(/NEXA Game Recommender/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders game recommendation form', () => {
  render(<App />);
  const formElement = screen.getByRole('form');
  expect(formElement).toBeInTheDocument();
});

test('renders input field for game preferences', () => {
  render(<App />);
  const inputElement = screen.getByPlaceholderText(/Enter your game preference/i);
  expect(inputElement).toBeInTheDocument();
});

test('renders get recommendations button', () => {
  render(<App />);
  const buttonElement = screen.getByText(/Get Recommendations/i);
  expect(buttonElement).toBeInTheDocument();
}); 