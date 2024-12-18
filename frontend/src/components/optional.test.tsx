import { describe, test } from "@jest/globals";
import "@testing-library/jest-dom";
import "@testing-library/jest-dom/jest-globals";
import { render, screen } from "@testing-library/react";
import { Optional } from "./optional";
import React from "react";
import expect from "expect";

describe("<Optional />", () => {
  test("value only", () => {
    render(<Optional value={28} />);
    expect(screen.getByText("28")).toBeInTheDocument();

    render(<Optional value={0} />);
    expect(screen.getByText("0")).toBeInTheDocument();

    render(<Optional value={undefined} />);
    expect(screen.queryByText("undefined")).not.toBeInTheDocument();

    render(<Optional value={"undefined"} />);
    expect(screen.queryByText("undefined")).toBeInTheDocument();

    render(<Optional value={[]} block={() => `empty`} />);
    expect(screen.queryByText("empty")).not.toBeInTheDocument();

    render(<Optional value={[1, 2, 3]} block={(it) => it.join("")} />);
    expect(screen.getByText("123")).toBeInTheDocument();
  });

  test("value with custom block", () => {
    render(<Optional value={28} block={(it) => `${it + 1}`} />);
    expect(screen.getByText("29")).toBeInTheDocument();
  });

  test("value with condition", () => {
    render(<Optional value={28} condition={(it) => it > 29} />);
    expect(screen.queryByText("28")).not.toBeInTheDocument();

    render(<Optional value={28} condition={(it) => it > 25} />);
    expect(screen.queryByText("28")).toBeInTheDocument();
  });
});
