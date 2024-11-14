def get_greeting() -> str:
    """Get a greeting."""
    return "Hello, world!"


def main() -> None:
    """Main entry point."""
    print(get_greeting())  # noqa: T201


if __name__ == "__main__":
    main()
