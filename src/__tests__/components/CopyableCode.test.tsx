import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { CopyableCode } from "@/components/CopyableCode";

// Mock clipboard API
const mockWriteText = jest.fn();
Object.assign(navigator, {
  clipboard: {
    writeText: mockWriteText,
  },
});

describe("CopyableCode Component", () => {
  beforeEach(() => {
    mockWriteText.mockClear();
  });

  it("renders the code snippet", () => {
    render(<CopyableCode>test-code.ts</CopyableCode>);
    expect(screen.getByText("test-code.ts")).toBeInTheDocument();
  });

  it("copies text to clipboard when clicked", async () => {
    render(<CopyableCode>test-code.ts</CopyableCode>);

    const button = screen.getByRole("button", { name: /copy code: test-code.ts/i });
    fireEvent.click(button);

    expect(mockWriteText).toHaveBeenCalledWith("test-code.ts");

    // Check for success feedback
    await waitFor(() => {
      expect(screen.getByText("Copied!")).toBeInTheDocument();
    });
  });

  it("updates aria-label on copy", async () => {
    render(<CopyableCode>test-code.ts</CopyableCode>);

    const button = screen.getByRole("button", { name: /copy code: test-code.ts/i });
    fireEvent.click(button);

    await waitFor(() => {
      expect(button).toHaveAttribute("aria-label", "Copied code");
    });
  });
});
