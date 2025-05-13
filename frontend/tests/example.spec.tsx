import { render, screen } from "@testing-library/react";
import App from "../src/App";

test("renders hello world", () => {
  render(<App />);
  expect(screen.getByText(/hello/i)).toBeInTheDocument();
});
